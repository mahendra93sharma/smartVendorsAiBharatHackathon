"""
Main deployment orchestrator for Smart Vendors backend.

Handles complete deployment workflow: packaging, infrastructure setup,
Lambda deployment, API Gateway configuration, and validation.
"""

import sys
import time
import json
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import boto3
from botocore.exceptions import ClientError

from config import get_deployment_config, DeploymentConfiguration
from build_layer import LambdaLayerBuilder
from package_functions import LambdaFunctionPackager


@dataclass
class DeploymentResult:
    """Result of deployment operation."""
    success: bool
    deployed_functions: List[str]
    api_endpoint_url: Optional[str]
    resource_arns: Dict[str, str]
    errors: List[str]
    deployment_duration_seconds: float


class DeploymentOrchestrator:
    """Orchestrates complete deployment workflow."""
    
    def __init__(self, config: DeploymentConfiguration):
        """
        Initialize deployment orchestrator.
        
        Args:
            config: Deployment configuration
        """
        self.config = config
        self.start_time = time.time()
        self.errors: List[str] = []
        self.resource_arns: Dict[str, str] = {}
        
        # Initialize AWS clients
        self.lambda_client = boto3.client('lambda', region_name=config.aws_region)
        self.iam_client = boto3.client('iam', region_name=config.aws_region)
        self.dynamodb_client = boto3.client('dynamodb', region_name=config.aws_region)
        self.s3_client = boto3.client('s3', region_name=config.aws_region)
        self.apigateway_client = boto3.client('apigatewayv2', region_name=config.aws_region)
    
    def deploy(self) -> DeploymentResult:
        """
        Execute complete deployment workflow.
        
        Returns:
            DeploymentResult with deployment status
        """
        print("🚀 Starting Smart Vendors Backend Deployment")
        print(f"   Environment: {self.config.environment}")
        print(f"   Region: {self.config.aws_region}")
        print("="*70 + "\n")
        
        try:
            # Step 1: Build Lambda layer
            self._build_lambda_layer()
            
            # Step 2: Package Lambda functions
            self._package_lambda_functions()
            
            # Step 3: Create IAM execution role
            self._create_iam_role()
            
            # Step 4: Create DynamoDB tables
            self._create_dynamodb_tables()
            
            # Step 5: Create S3 buckets
            self._create_s3_buckets()
            
            # Step 6: Deploy Lambda layer
            self._deploy_lambda_layer()
            
            # Step 7: Deploy Lambda functions
            deployed_functions = self._deploy_lambda_functions()
            
            # Step 8: Create API Gateway
            api_url = self._create_api_gateway()
            
            # Step 9: Validate deployment
            self._validate_deployment()
            
            duration = time.time() - self.start_time
            
            print("\n" + "="*70)
            print("✓ DEPLOYMENT SUCCESSFUL")
            print("="*70)
            print(f"Duration: {duration:.2f} seconds")
            print(f"API Endpoint: {api_url}")
            print(f"Deployed Functions: {len(deployed_functions)}")
            print("="*70 + "\n")
            
            return DeploymentResult(
                success=True,
                deployed_functions=deployed_functions,
                api_endpoint_url=api_url,
                resource_arns=self.resource_arns,
                errors=self.errors,
                deployment_duration_seconds=duration
            )
            
        except Exception as e:
            duration = time.time() - self.start_time
            error_msg = f"Deployment failed: {e}"
            self.errors.append(error_msg)
            
            print("\n" + "="*70)
            print("✗ DEPLOYMENT FAILED")
            print("="*70)
            print(f"Error: {error_msg}")
            print(f"Duration: {duration:.2f} seconds")
            print("="*70 + "\n")
            
            return DeploymentResult(
                success=False,
                deployed_functions=[],
                api_endpoint_url=None,
                resource_arns=self.resource_arns,
                errors=self.errors,
                deployment_duration_seconds=duration
            )
    
    def _build_lambda_layer(self):
        """Build Lambda layer with shared dependencies."""
        print("📦 Step 1: Building Lambda layer...")
        
        builder = LambdaLayerBuilder(workspace_dir=".")
        artifact = builder.build_layer()
        
        self.layer_artifact_path = artifact.zip_path
        print(f"   ✓ Layer built: {artifact.zip_path}\n")
    
    def _package_lambda_functions(self):
        """Package all Lambda functions."""
        print("📦 Step 2: Packaging Lambda functions...")
        
        packager = LambdaFunctionPackager(workspace_dir=".")
        artifacts = packager.package_all_functions(include_shared=True)
        
        self.function_artifacts = {a.function_name: a for a in artifacts}
        print(f"   ✓ Packaged {len(artifacts)} functions\n")
    
    def _create_iam_role(self):
        """Create IAM execution role for Lambda functions."""
        print("🔐 Step 3: Creating IAM execution role...")
        
        role_name = f"{self.config.project_name}-lambda-execution-{self.config.environment}"
        
        # Check if role already exists
        try:
            response = self.iam_client.get_role(RoleName=role_name)
            role_arn = response['Role']['Arn']
            print(f"   ✓ Using existing role: {role_arn}")
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchEntity':
                # Create new role
                trust_policy = {
                    "Version": "2012-10-17",
                    "Statement": [{
                        "Effect": "Allow",
                        "Principal": {"Service": "lambda.amazonaws.com"},
                        "Action": "sts:AssumeRole"
                    }]
                }
                
                response = self.iam_client.create_role(
                    RoleName=role_name,
                    AssumeRolePolicyDocument=json.dumps(trust_policy),
                    Description=f"Execution role for {self.config.project_name} Lambda functions"
                )
                role_arn = response['Role']['Arn']
                
                # Attach managed policies
                policies = [
                    'arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole',
                    'arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess',
                    'arn:aws:iam::aws:policy/AmazonS3FullAccess',
                ]
                
                for policy_arn in policies:
                    self.iam_client.attach_role_policy(
                        RoleName=role_name,
                        PolicyArn=policy_arn
                    )
                
                print(f"   ✓ Created role: {role_arn}")
                
                # Wait for role to be available
                print("   ⏳ Waiting for role to propagate...")
                time.sleep(10)
            else:
                raise
        
        self.execution_role_arn = role_arn
        self.resource_arns['iam_role'] = role_arn
        print()
    
    def _create_dynamodb_tables(self):
        """Create DynamoDB tables."""
        print("🗄️  Step 4: Creating DynamoDB tables...")
        
        for table_config in self.config.dynamodb_tables:
            try:
                # Check if table exists
                self.dynamodb_client.describe_table(TableName=table_config.name)
                print(f"   ✓ Table exists: {table_config.name}")
            except ClientError as e:
                if e.response['Error']['Code'] == 'ResourceNotFoundException':
                    # Create table
                    key_schema = [
                        {'AttributeName': table_config.partition_key, 'KeyType': 'HASH'}
                    ]
                    attribute_definitions = [
                        {'AttributeName': table_config.partition_key, 'AttributeType': table_config.partition_key_type}
                    ]
                    
                    if table_config.sort_key:
                        key_schema.append({'AttributeName': table_config.sort_key, 'KeyType': 'RANGE'})
                        attribute_definitions.append({
                            'AttributeName': table_config.sort_key,
                            'AttributeType': table_config.sort_key_type
                        })
                    
                    self.dynamodb_client.create_table(
                        TableName=table_config.name,
                        KeySchema=key_schema,
                        AttributeDefinitions=attribute_definitions,
                        BillingMode=table_config.billing_mode,
                        SSESpecification={'Enabled': table_config.enable_encryption}
                    )
                    
                    print(f"   ✓ Created table: {table_config.name}")
                    
                    # Wait for table to be active
                    waiter = self.dynamodb_client.get_waiter('table_exists')
                    waiter.wait(TableName=table_config.name)
                else:
                    raise
        
        print()
    
    def _create_s3_buckets(self):
        """Create S3 buckets."""
        print("🪣 Step 5: Creating S3 buckets...")
        
        for bucket_config in self.config.s3_buckets:
            try:
                # Check if bucket exists
                self.s3_client.head_bucket(Bucket=bucket_config.name)
                print(f"   ✓ Bucket exists: {bucket_config.name}")
            except ClientError as e:
                if e.response['Error']['Code'] == '404':
                    # Create bucket
                    if self.config.aws_region == 'us-east-1':
                        self.s3_client.create_bucket(Bucket=bucket_config.name)
                    else:
                        self.s3_client.create_bucket(
                            Bucket=bucket_config.name,
                            CreateBucketConfiguration={'LocationConstraint': self.config.aws_region}
                        )
                    
                    # Enable versioning if configured
                    if bucket_config.enable_versioning:
                        self.s3_client.put_bucket_versioning(
                            Bucket=bucket_config.name,
                            VersioningConfiguration={'Status': 'Enabled'}
                        )
                    
                    # Configure CORS if needed
                    if bucket_config.enable_cors:
                        cors_config = {
                            'CORSRules': [{
                                'AllowedHeaders': ['*'],
                                'AllowedMethods': ['GET', 'PUT', 'POST', 'DELETE', 'HEAD'],
                                'AllowedOrigins': ['*'],
                                'ExposeHeaders': ['ETag'],
                                'MaxAgeSeconds': 3000
                            }]
                        }
                        self.s3_client.put_bucket_cors(
                            Bucket=bucket_config.name,
                            CORSConfiguration=cors_config
                        )
                    
                    print(f"   ✓ Created bucket: {bucket_config.name}")
                else:
                    raise
        
        print()
    
    def _deploy_lambda_layer(self):
        """Deploy Lambda layer to AWS."""
        print("📚 Step 6: Deploying Lambda layer...")
        
        layer_name = f"{self.config.project_name}-dependencies-{self.config.environment}"
        
        with open(self.layer_artifact_path, 'rb') as f:
            layer_content = f.read()
        
        response = self.lambda_client.publish_layer_version(
            LayerName=layer_name,
            Description="Shared dependencies for Smart Vendors Lambda functions",
            Content={'ZipFile': layer_content},
            CompatibleRuntimes=['python3.11', 'python3.12']
        )
        
        self.layer_arn = response['LayerVersionArn']
        self.resource_arns['lambda_layer'] = self.layer_arn
        
        print(f"   ✓ Layer deployed: {self.layer_arn}\n")
    
    def _deploy_lambda_functions(self) -> List[str]:
        """Deploy all Lambda functions."""
        print("⚡ Step 7: Deploying Lambda functions...")
        
        deployed = []
        
        for func_config in self.config.lambda_functions:
            try:
                # Get function artifact
                function_name = func_config.handler.split('.')[0]
                artifact = self.function_artifacts.get(function_name)
                
                if not artifact:
                    print(f"   ✗ Artifact not found for {func_config.name}")
                    continue
                
                # Read function code
                with open(artifact.zip_path, 'rb') as f:
                    function_code = f.read()
                
                # Check if function exists
                try:
                    self.lambda_client.get_function(FunctionName=func_config.name)
                    # Update existing function
                    self.lambda_client.update_function_code(
                        FunctionName=func_config.name,
                        ZipFile=function_code
                    )
                    print(f"   ✓ Updated: {func_config.name}")
                except ClientError as e:
                    if e.response['Error']['Code'] == 'ResourceNotFoundException':
                        # Create new function
                        response = self.lambda_client.create_function(
                            FunctionName=func_config.name,
                            Runtime=func_config.runtime,
                            Role=self.execution_role_arn,
                            Handler=func_config.handler,
                            Code={'ZipFile': function_code},
                            Timeout=func_config.timeout_seconds,
                            MemorySize=func_config.memory_mb,
                            Environment={'Variables': func_config.environment_vars},
                            Layers=[self.layer_arn]
                        )
                        print(f"   ✓ Created: {func_config.name}")
                        self.resource_arns[f"lambda_{function_name}"] = response['FunctionArn']
                    else:
                        raise
                
                deployed.append(func_config.name)
                
            except Exception as e:
                error_msg = f"Failed to deploy {func_config.name}: {e}"
                print(f"   ✗ {error_msg}")
                self.errors.append(error_msg)
        
        print()
        return deployed
    
    def _create_api_gateway(self) -> Optional[str]:
        """Create API Gateway and configure routes."""
        print("🌐 Step 8: Creating API Gateway...")
        
        api_name = f"{self.config.project_name}-api-{self.config.environment}"
        
        # Create HTTP API
        response = self.apigateway_client.create_api(
            Name=api_name,
            ProtocolType='HTTP',
            CorsConfiguration={
                'AllowOrigins': ['*'],
                'AllowMethods': ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
                'AllowHeaders': ['*'],
                'MaxAge': 300
            }
        )
        
        api_id = response['ApiId']
        self.resource_arns['api_gateway'] = api_id
        
        print(f"   ✓ Created API: {api_id}")
        
        # Create routes for each Lambda function
        for func_config in self.config.lambda_functions:
            for route in func_config.api_routes:
                try:
                    # Create integration
                    function_arn = f"arn:aws:lambda:{self.config.aws_region}:{self._get_account_id()}:function:{func_config.name}"
                    
                    integration_response = self.apigateway_client.create_integration(
                        ApiId=api_id,
                        IntegrationType='AWS_PROXY',
                        IntegrationUri=function_arn,
                        PayloadFormatVersion='2.0'
                    )
                    
                    integration_id = integration_response['IntegrationId']
                    
                    # Create route
                    self.apigateway_client.create_route(
                        ApiId=api_id,
                        RouteKey=f"{route.method} {route.path}",
                        Target=f"integrations/{integration_id}"
                    )
                    
                    # Grant API Gateway permission to invoke Lambda
                    try:
                        self.lambda_client.add_permission(
                            FunctionName=func_config.name,
                            StatementId=f"apigateway-{api_id}-{route.method}-{route.path.replace('/', '-')}",
                            Action='lambda:InvokeFunction',
                            Principal='apigateway.amazonaws.com',
                            SourceArn=f"arn:aws:execute-api:{self.config.aws_region}:{self._get_account_id()}:{api_id}/*/*"
                        )
                    except ClientError as e:
                        if e.response['Error']['Code'] != 'ResourceConflictException':
                            raise
                    
                    print(f"   ✓ Route: {route.method} {route.path} -> {func_config.name}")
                    
                except Exception as e:
                    error_msg = f"Failed to create route {route.path}: {e}"
                    print(f"   ✗ {error_msg}")
                    self.errors.append(error_msg)
        
        # Create default stage
        self.apigateway_client.create_stage(
            ApiId=api_id,
            StageName='$default',
            AutoDeploy=True
        )
        
        api_url = f"https://{api_id}.execute-api.{self.config.aws_region}.amazonaws.com"
        print(f"   ✓ API URL: {api_url}\n")
        
        return api_url
    
    def _validate_deployment(self):
        """Validate deployment."""
        print("✅ Step 9: Validating deployment...")
        
        # Check Lambda functions are active
        for func_config in self.config.lambda_functions:
            try:
                response = self.lambda_client.get_function(FunctionName=func_config.name)
                state = response['Configuration']['State']
                if state == 'Active':
                    print(f"   ✓ {func_config.name}: Active")
                else:
                    print(f"   ⚠️  {func_config.name}: {state}")
            except Exception as e:
                print(f"   ✗ {func_config.name}: {e}")
        
        print()
    
    def _get_account_id(self) -> str:
        """Get AWS account ID."""
        sts = boto3.client('sts')
        return sts.get_caller_identity()['Account']


def main():
    """Main entry point for deployment."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Deploy Smart Vendors backend to AWS")
    parser.add_argument(
        "--environment",
        default="dev",
        choices=["dev", "staging", "prod"],
        help="Deployment environment (default: dev)"
    )
    parser.add_argument(
        "--region",
        default="ap-south-1",
        help="AWS region (default: ap-south-1)"
    )
    
    args = parser.parse_args()
    
    # Get deployment configuration
    config = get_deployment_config(
        environment=args.environment,
        aws_region=args.region
    )
    
    # Validate configuration
    errors = config.validate()
    if errors:
        print("❌ Configuration validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    
    # Execute deployment
    orchestrator = DeploymentOrchestrator(config)
    result = orchestrator.deploy()
    
    # Save deployment result
    result_file = Path("deployment_result.json")
    with open(result_file, 'w') as f:
        json.dump(asdict(result), f, indent=2)
    
    print(f"📄 Deployment result saved to: {result_file}")
    
    return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(main())
