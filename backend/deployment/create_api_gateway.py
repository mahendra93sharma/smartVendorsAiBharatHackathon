"""
Create API Gateway and configure routes for Lambda functions.
"""

import sys
import boto3
from botocore.exceptions import ClientError

from config import get_deployment_config


def create_api_gateway():
    """Create API Gateway with routes."""
    print("🌐 Creating API Gateway")
    print("="*70 + "\n")
    
    region = "ap-south-1"
    environment = "dev"
    
    # Get config
    config = get_deployment_config(environment=environment, aws_region=region)
    
    # Initialize AWS clients
    apigateway_client = boto3.client('apigatewayv2', region_name=region)
    lambda_client = boto3.client('lambda', region_name=region)
    sts = boto3.client('sts')
    account_id = sts.get_caller_identity()['Account']
    
    # Create HTTP API
    api_name = f"{config.project_name}-api-{environment}"
    
    print(f"Creating API: {api_name}...")
    
    response = apigateway_client.create_api(
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
    print(f"✓ Created API: {api_id}\n")
    
    # Create routes for each Lambda function
    print("Creating routes...")
    
    for func_config in config.lambda_functions:
        for route in func_config.api_routes:
            try:
                # Create integration
                function_arn = f"arn:aws:lambda:{region}:{account_id}:function:{func_config.name}"
                
                integration_response = apigateway_client.create_integration(
                    ApiId=api_id,
                    IntegrationType='AWS_PROXY',
                    IntegrationUri=function_arn,
                    PayloadFormatVersion='2.0'
                )
                
                integration_id = integration_response['IntegrationId']
                
                # Create route
                apigateway_client.create_route(
                    ApiId=api_id,
                    RouteKey=f"{str(route.method.value)} {route.path}",
                    Target=f"integrations/{integration_id}"
                )
                
                # Grant API Gateway permission to invoke Lambda
                try:
                    lambda_client.add_permission(
                        FunctionName=func_config.name,
                        StatementId=f"apigateway-{api_id}-{str(route.method.value)}-{route.path.replace('/', '-').replace('{', '').replace('}', '')}",
                        Action='lambda:InvokeFunction',
                        Principal='apigateway.amazonaws.com',
                        SourceArn=f"arn:aws:execute-api:{region}:{account_id}:{api_id}/*/*"
                    )
                except ClientError as e:
                    if e.response['Error']['Code'] != 'ResourceConflictException':
                        raise
                
                print(f"  ✓ {str(route.method.value):6} {route.path:40} -> {func_config.name}")
                
            except Exception as e:
                print(f"  ✗ Failed to create route {route.path}: {e}")
    
    # Create default stage
    print("\nCreating default stage...")
    apigateway_client.create_stage(
        ApiId=api_id,
        StageName='$default',
        AutoDeploy=True
    )
    
    api_url = f"https://{api_id}.execute-api.{region}.amazonaws.com"
    
    print(f"\n✓ API Gateway created successfully!")
    print(f"  API ID: {api_id}")
    print(f"  API URL: {api_url}")
    print("\n" + "="*70)
    print("\n📝 Test your API:")
    print(f"\n  # Get transactions")
    print(f"  curl {api_url}/transactions/vendor-123")
    print(f"\n  # Get market prices")
    print(f"  curl {api_url}/prices/tomatoes")
    print(f"\n  # Get trust score")
    print(f"  curl {api_url}/trust-score/vendor-123")
    print("\n" + "="*70 + "\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(create_api_gateway())
