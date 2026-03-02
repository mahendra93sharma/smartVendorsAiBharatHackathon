"""
Quick deployment script - deploys Lambda functions using pre-built artifacts.
"""

import sys
import boto3
from pathlib import Path
from botocore.exceptions import ClientError

def quick_deploy():
    """Deploy Lambda functions using existing artifacts."""
    print("🚀 Quick Lambda Deployment")
    print("="*70 + "\n")
    
    region = "ap-south-1"
    environment = "dev"
    project_name = "smart-vendors"
    
    # Initialize clients
    lambda_client = boto3.client('lambda', region_name=region)
    iam_client = boto3.client('iam')
    
    # Get execution role
    role_name = f"{project_name}-lambda-execution-{environment}"
    try:
        response = iam_client.get_role(RoleName=role_name)
        execution_role_arn = response['Role']['Arn']
        print(f"✓ IAM Role: {execution_role_arn}\n")
    except ClientError:
        print(f"✗ IAM role not found: {role_name}")
        return 1
    
    # Check if layer artifact exists
    layer_path = Path("dist/lambda_layer.zip")
    if not layer_path.exists():
        print("✗ Layer artifact not found. Run build_layer.py first.")
        return 1
    
    # Deploy layer
    print("📚 Deploying Lambda layer...")
    layer_name = f"{project_name}-dependencies-{environment}"
    
    try:
        with open(layer_path, 'rb') as f:
            layer_content = f.read()
        
        response = lambda_client.publish_layer_version(
            LayerName=layer_name,
            Description="Shared dependencies",
            Content={'ZipFile': layer_content},
            CompatibleRuntimes=['python3.11', 'python3.12']
        )
        layer_arn = response['LayerVersionArn']
        print(f"✓ Layer: {layer_arn}\n")
    except Exception as e:
        print(f"✗ Layer deployment failed: {e}")
        return 1
    
    # Define functions to deploy (AWS_REGION removed - it's a reserved env var)
    functions = [
        {
            'name': f'{project_name}-voice-transcribe-{environment}',
            'handler': 'voice_transcribe.lambda_handler',
            'zip': 'dist/voice_transcribe.zip',
            'memory': 512,
            'timeout': 60,
            'env': {
                'ENVIRONMENT': environment,
                'S3_BUCKET_IMAGES': f'{project_name}-images-{environment}',
                'DYNAMODB_TABLE_TRANSACTIONS': f'{project_name}-transactions-{environment}',
            }
        },
        {
            'name': f'{project_name}-create-transaction-{environment}',
            'handler': 'create_transaction.lambda_handler',
            'zip': 'dist/create_transaction.zip',
            'memory': 256,
            'timeout': 30,
            'env': {
                'ENVIRONMENT': environment,
                'DYNAMODB_TABLE_TRANSACTIONS': f'{project_name}-transactions-{environment}',
            }
        },
        {
            'name': f'{project_name}-get-transactions-{environment}',
            'handler': 'get_transactions.lambda_handler',
            'zip': 'dist/get_transactions.zip',
            'memory': 256,
            'timeout': 15,
            'env': {
                'ENVIRONMENT': environment,
                'DYNAMODB_TABLE_TRANSACTIONS': f'{project_name}-transactions-{environment}',
            }
        },
        {
            'name': f'{project_name}-get-market-prices-{environment}',
            'handler': 'get_market_prices.lambda_handler',
            'zip': 'dist/get_market_prices.zip',
            'memory': 256,
            'timeout': 15,
            'env': {
                'ENVIRONMENT': environment,
                'DYNAMODB_TABLE_MARKET_PRICES': f'{project_name}-market-prices-{environment}',
            }
        },
        {
            'name': f'{project_name}-classify-freshness-{environment}',
            'handler': 'classify_freshness.lambda_handler',
            'zip': 'dist/classify_freshness.zip',
            'memory': 512,
            'timeout': 60,
            'env': {
                'ENVIRONMENT': environment,
                'S3_BUCKET_IMAGES': f'{project_name}-images-{environment}',
                'DEMO_MODE': 'true',
            }
        },
        {
            'name': f'{project_name}-create-marketplace-listing-{environment}',
            'handler': 'create_marketplace_listing.lambda_handler',
            'zip': 'dist/create_marketplace_listing.zip',
            'memory': 256,
            'timeout': 30,
            'env': {
                'ENVIRONMENT': environment,
                'DYNAMODB_TABLE_MARKETPLACE_LISTINGS': f'{project_name}-marketplace-listings-{environment}',
                'DYNAMODB_TABLE_VENDORS': f'{project_name}-vendors-{environment}',
            }
        },
        {
            'name': f'{project_name}-get-marketplace-buyers-{environment}',
            'handler': 'get_marketplace_buyers.lambda_handler',
            'zip': 'dist/get_marketplace_buyers.zip',
            'memory': 256,
            'timeout': 15,
            'env': {
                'ENVIRONMENT': environment,
                'DYNAMODB_TABLE_VENDORS': f'{project_name}-vendors-{environment}',
            }
        },
        {
            'name': f'{project_name}-notify-marketplace-buyers-{environment}',
            'handler': 'notify_marketplace_buyers.lambda_handler',
            'zip': 'dist/notify_marketplace_buyers.zip',
            'memory': 256,
            'timeout': 30,
            'env': {
                'ENVIRONMENT': environment,
                'DYNAMODB_TABLE_MARKETPLACE_LISTINGS': f'{project_name}-marketplace-listings-{environment}',
                'DYNAMODB_TABLE_VENDORS': f'{project_name}-vendors-{environment}',
            }
        },
        {
            'name': f'{project_name}-get-trust-score-{environment}',
            'handler': 'get_trust_score.lambda_handler',
            'zip': 'dist/get_trust_score.zip',
            'memory': 256,
            'timeout': 15,
            'env': {
                'ENVIRONMENT': environment,
                'DYNAMODB_TABLE_VENDORS': f'{project_name}-vendors-{environment}',
                'DYNAMODB_TABLE_TRANSACTIONS': f'{project_name}-transactions-{environment}',
                'DYNAMODB_TABLE_MARKETPLACE_LISTINGS': f'{project_name}-marketplace-listings-{environment}',
            }
        },
    ]
    
    # Deploy each function
    print("⚡ Deploying Lambda functions...\n")
    deployed = 0
    
    for func in functions:
        try:
            zip_path = Path(func['zip'])
            if not zip_path.exists():
                print(f"  ✗ {func['name']}: Artifact not found")
                continue
            
            with open(zip_path, 'rb') as f:
                code = f.read()
            
            # Try to update existing function
            try:
                lambda_client.update_function_code(
                    FunctionName=func['name'],
                    ZipFile=code
                )
                lambda_client.update_function_configuration(
                    FunctionName=func['name'],
                    Runtime='python3.11',
                    Role=execution_role_arn,
                    Handler=func['handler'],
                    Timeout=func['timeout'],
                    MemorySize=func['memory'],
                    Environment={'Variables': func['env']},
                    Layers=[layer_arn]
                )
                print(f"  ✓ Updated: {func['name']}")
                deployed += 1
            except ClientError as e:
                if e.response['Error']['Code'] == 'ResourceNotFoundException':
                    # Create new function
                    lambda_client.create_function(
                        FunctionName=func['name'],
                        Runtime='python3.11',
                        Role=execution_role_arn,
                        Handler=func['handler'],
                        Code={'ZipFile': code},
                        Timeout=func['timeout'],
                        MemorySize=func['memory'],
                        Environment={'Variables': func['env']},
                        Layers=[layer_arn]
                    )
                    print(f"  ✓ Created: {func['name']}")
                    deployed += 1
                else:
                    raise
        except Exception as e:
            print(f"  ✗ {func['name']}: {e}")
    
    print(f"\n✓ Deployed {deployed}/{len(functions)} functions")
    print("="*70 + "\n")
    
    return 0 if deployed == len(functions) else 1


if __name__ == "__main__":
    sys.exit(quick_deploy())
