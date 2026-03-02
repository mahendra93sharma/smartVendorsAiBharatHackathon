"""
Deploy only Lambda functions (infrastructure already exists).
"""

import sys
import time
import json
from pathlib import Path
import boto3
from botocore.exceptions import ClientError

from config import get_deployment_config
from build_layer import LambdaLayerBuilder
from package_functions import LambdaFunctionPackager


def deploy_lambdas():
    """Deploy Lambda functions only."""
    print("🚀 Deploying Lambda Functions")
    print("="*70 + "\n")
    
    region = "ap-south-1"
    environment = "dev"
    
    # Get config
    config = get_deployment_config(environment=environment, aws_region=region)
    
    # Initialize AWS clients
    lambda_client = boto3.client('lambda', region_name=region)
    iam_client = boto3.client('iam')
    
    # Get execution role ARN
    role_name = f"{config.project_name}-lambda-execution-{environment}"
    try:
        response = iam_client.get_role(RoleName=role_name)
        execution_role_arn = response['Role']['Arn']
        print(f"✓ Using IAM role: {execution_role_arn}\n")
    except ClientError as e:
        print(f"✗ IAM role not found: {role_name}")
        print("  Run full deployment first to create infrastructure")
        return 1
    
    # Build layer
    print("📚 Building Lambda layer...")
    builder = LambdaLayerBuilder(workspace_dir=".")
    layer_artifact = builder.build_layer()
    print()
    
    # Deploy layer
    print("📚 Deploying Lambda layer...")
    layer_name = f"{config.project_name}-dependencies-{environment}"
    
    with open(layer_artifact.zip_path, 'rb') as f:
        layer_content = f.read()
    
    response = lambda_client.publish_layer_version(
        LayerName=layer_name,
        Description="Shared dependencies for Smart Vendors Lambda functions",
        Content={'ZipFile': layer_content},
        CompatibleRuntimes=['python3.11', 'python3.12']
    )
    
    layer_arn = response['LayerVersionArn']
    print(f"✓ Layer deployed: {layer_arn}\n")
    
    # Package functions
    print("📦 Packaging Lambda functions...")
    packager = LambdaFunctionPackager(workspace_dir=".")
    artifacts = packager.package_all_functions(include_shared=True)
    function_artifacts = {a.function_name: a for a in artifacts}
    print()
    
    # Deploy functions
    print("⚡ Deploying Lambda functions...")
    deployed = []
    
    for func_config in config.lambda_functions:
        try:
            # Get function artifact
            function_name = func_config.handler.split('.')[0]
            artifact = function_artifacts.get(function_name)
            
            if not artifact:
                print(f"  ✗ Artifact not found for {func_config.name}")
                continue
            
            # Read function code
            with open(artifact.zip_path, 'rb') as f:
                function_code = f.read()
            
            # Check if function exists
            try:
                lambda_client.get_function(FunctionName=func_config.name)
                # Update existing function
                lambda_client.update_function_code(
                    FunctionName=func_config.name,
                    ZipFile=function_code
                )
                print(f"  ✓ Updated: {func_config.name}")
            except ClientError as e:
                if e.response['Error']['Code'] == 'ResourceNotFoundException':
                    # Create new function
                    lambda_client.create_function(
                        FunctionName=func_config.name,
                        Runtime=func_config.runtime,
                        Role=execution_role_arn,
                        Handler=func_config.handler,
                        Code={'ZipFile': function_code},
                        Timeout=func_config.timeout_seconds,
                        MemorySize=func_config.memory_mb,
                        Environment={'Variables': func_config.environment_vars},
                        Layers=[layer_arn]
                    )
                    print(f"  ✓ Created: {func_config.name}")
                else:
                    raise
            
            deployed.append(func_config.name)
            
        except Exception as e:
            print(f"  ✗ Failed to deploy {func_config.name}: {e}")
    
    print(f"\n✓ Deployed {len(deployed)} functions")
    print("="*70)
    
    return 0


if __name__ == "__main__":
    sys.exit(deploy_lambdas())
