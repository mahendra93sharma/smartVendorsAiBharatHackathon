"""
Deployment configuration for Smart Vendors backend.

Defines configuration for all Lambda functions, DynamoDB tables, S3 buckets,
and API Gateway routes.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum


class HTTPMethod(str, Enum):
    """HTTP methods for API routes."""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class AWSService(str, Enum):
    """AWS services that Lambda functions may require access to."""
    DYNAMODB = "dynamodb"
    S3 = "s3"
    BEDROCK = "bedrock"
    TRANSCRIBE = "transcribe"
    SAGEMAKER = "sagemaker"
    CLOUDWATCH_LOGS = "logs"


@dataclass
class APIRoute:
    """API Gateway route configuration."""
    path: str
    method: HTTPMethod
    lambda_function: str
    
    def __post_init__(self):
        """Validate route configuration."""
        if not self.path.startswith("/"):
            raise ValueError(f"Route path must start with '/': {self.path}")


@dataclass
class LambdaFunctionConfig:
    """Configuration for a single Lambda function."""
    name: str
    handler: str
    runtime: str = "python3.11"
    memory_mb: int = 256
    timeout_seconds: int = 30
    environment_vars: Dict[str, str] = field(default_factory=dict)
    required_permissions: List[AWSService] = field(default_factory=list)
    api_routes: List[APIRoute] = field(default_factory=list)
    
    # DynamoDB tables this function needs access to
    dynamodb_tables: List[str] = field(default_factory=list)
    
    # S3 buckets this function needs access to
    s3_buckets: List[str] = field(default_factory=list)
    
    def validate(self) -> List[str]:
        """
        Validate function configuration.
        
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        if not self.name:
            errors.append("Function name is required")
        
        if not self.handler:
            errors.append("Handler is required")
        
        if self.memory_mb < 128 or self.memory_mb > 10240:
            errors.append(f"Memory must be between 128 and 10240 MB: {self.memory_mb}")
        
        if self.timeout_seconds < 1 or self.timeout_seconds > 900:
            errors.append(f"Timeout must be between 1 and 900 seconds: {self.timeout_seconds}")
        
        # Validate that required permissions match resource access
        if self.dynamodb_tables and AWSService.DYNAMODB not in self.required_permissions:
            errors.append(f"Function {self.name} accesses DynamoDB but doesn't have DYNAMODB permission")
        
        if self.s3_buckets and AWSService.S3 not in self.required_permissions:
            errors.append(f"Function {self.name} accesses S3 but doesn't have S3 permission")
        
        return errors


@dataclass
class DynamoDBTableConfig:
    """Configuration for a DynamoDB table."""
    name: str
    partition_key: str
    partition_key_type: str = "S"  # S=String, N=Number, B=Binary
    sort_key: Optional[str] = None
    sort_key_type: str = "S"
    billing_mode: str = "PAY_PER_REQUEST"  # On-demand billing
    enable_point_in_time_recovery: bool = True
    enable_encryption: bool = True


@dataclass
class S3BucketConfig:
    """Configuration for an S3 bucket."""
    name: str
    enable_versioning: bool = True
    enable_cors: bool = True
    block_public_access: bool = True
    lifecycle_policies: List[Dict] = field(default_factory=list)


@dataclass
class DeploymentConfiguration:
    """Complete deployment configuration for Smart Vendors backend."""
    aws_region: str
    environment: str  # dev, staging, prod
    project_name: str
    lambda_functions: List[LambdaFunctionConfig]
    dynamodb_tables: List[DynamoDBTableConfig]
    s3_buckets: List[S3BucketConfig]
    
    def validate(self) -> List[str]:
        """
        Validate entire deployment configuration.
        
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        if not self.aws_region:
            errors.append("AWS region is required")
        
        if self.environment not in ["dev", "staging", "prod"]:
            errors.append(f"Environment must be dev, staging, or prod: {self.environment}")
        
        if not self.project_name:
            errors.append("Project name is required")
        
        # Validate all Lambda functions
        for func in self.lambda_functions:
            func_errors = func.validate()
            errors.extend(func_errors)
        
        # Check for duplicate function names
        func_names = [f.name for f in self.lambda_functions]
        if len(func_names) != len(set(func_names)):
            errors.append("Duplicate Lambda function names found")
        
        # Check for duplicate table names
        table_names = [t.name for t in self.dynamodb_tables]
        if len(table_names) != len(set(table_names)):
            errors.append("Duplicate DynamoDB table names found")
        
        # Check for duplicate bucket names
        bucket_names = [b.name for b in self.s3_buckets]
        if len(bucket_names) != len(set(bucket_names)):
            errors.append("Duplicate S3 bucket names found")
        
        return errors


def get_deployment_config(environment: str = "dev", aws_region: str = "ap-south-1") -> DeploymentConfiguration:
    """
    Get deployment configuration for Smart Vendors backend.
    
    Args:
        environment: Deployment environment (dev, staging, prod)
        aws_region: AWS region for deployment
    
    Returns:
        Complete deployment configuration
    """
    project_name = "smart-vendors"
    
    # Define DynamoDB tables
    dynamodb_tables = [
        DynamoDBTableConfig(
            name=f"{project_name}-vendors-{environment}",
            partition_key="vendor_id",
            partition_key_type="S",
        ),
        DynamoDBTableConfig(
            name=f"{project_name}-transactions-{environment}",
            partition_key="vendor_id",
            partition_key_type="S",
            sort_key="timestamp",
            sort_key_type="N",
        ),
        DynamoDBTableConfig(
            name=f"{project_name}-market-prices-{environment}",
            partition_key="item_name",
            partition_key_type="S",
            sort_key="timestamp",
            sort_key_type="N",
        ),
        DynamoDBTableConfig(
            name=f"{project_name}-marketplace-listings-{environment}",
            partition_key="listing_id",
            partition_key_type="S",
            sort_key="timestamp",
            sort_key_type="N",
        ),
    ]
    
    # Define S3 buckets
    s3_buckets = [
        S3BucketConfig(
            name=f"{project_name}-images-{environment}",
            enable_versioning=True,
            enable_cors=True,
            block_public_access=True,
            lifecycle_policies=[
                {
                    "id": "transition-old-images",
                    "status": "Enabled",
                    "transitions": [
                        {"days": 90, "storage_class": "STANDARD_IA"},
                        {"days": 180, "storage_class": "GLACIER"},
                    ],
                }
            ],
        ),
        S3BucketConfig(
            name=f"{project_name}-static-{environment}",
            enable_versioning=True,
            enable_cors=True,
            block_public_access=False,  # Static assets may be public
        ),
        S3BucketConfig(
            name=f"{project_name}-ml-models-{environment}",
            enable_versioning=True,
            enable_cors=False,
            block_public_access=True,
        ),
    ]
    
    # Common environment variables for all functions
    common_env_vars = {
        "AWS_REGION": aws_region,
        "ENVIRONMENT": environment,
        "LOG_LEVEL": "INFO",
    }
    
    # Define Lambda functions
    lambda_functions = [
        # 1. Voice Transcribe
        LambdaFunctionConfig(
            name=f"{project_name}-voice-transcribe-{environment}",
            handler="voice_transcribe.lambda_handler",
            memory_mb=512,
            timeout_seconds=60,
            environment_vars={
                **common_env_vars,
                "S3_BUCKET_IMAGES": f"{project_name}-images-{environment}",
                "DYNAMODB_TABLE_TRANSACTIONS": f"{project_name}-transactions-{environment}",
            },
            required_permissions=[
                AWSService.TRANSCRIBE,
                AWSService.BEDROCK,
                AWSService.S3,
                AWSService.DYNAMODB,
                AWSService.CLOUDWATCH_LOGS,
            ],
            dynamodb_tables=[f"{project_name}-transactions-{environment}"],
            s3_buckets=[f"{project_name}-images-{environment}"],
            api_routes=[
                APIRoute(path="/voice/transcribe", method=HTTPMethod.POST, lambda_function="voice_transcribe")
            ],
        ),
        
        # 2. Create Transaction
        LambdaFunctionConfig(
            name=f"{project_name}-create-transaction-{environment}",
            handler="create_transaction.lambda_handler",
            memory_mb=256,
            timeout_seconds=30,
            environment_vars={
                **common_env_vars,
                "DYNAMODB_TABLE_TRANSACTIONS": f"{project_name}-transactions-{environment}",
            },
            required_permissions=[
                AWSService.BEDROCK,
                AWSService.DYNAMODB,
                AWSService.CLOUDWATCH_LOGS,
            ],
            dynamodb_tables=[f"{project_name}-transactions-{environment}"],
            api_routes=[
                APIRoute(path="/transactions", method=HTTPMethod.POST, lambda_function="create_transaction")
            ],
        ),
        
        # 3. Get Transactions
        LambdaFunctionConfig(
            name=f"{project_name}-get-transactions-{environment}",
            handler="get_transactions.lambda_handler",
            memory_mb=256,
            timeout_seconds=15,
            environment_vars={
                **common_env_vars,
                "DYNAMODB_TABLE_TRANSACTIONS": f"{project_name}-transactions-{environment}",
            },
            required_permissions=[
                AWSService.DYNAMODB,
                AWSService.CLOUDWATCH_LOGS,
            ],
            dynamodb_tables=[f"{project_name}-transactions-{environment}"],
            api_routes=[
                APIRoute(path="/transactions/{vendor_id}", method=HTTPMethod.GET, lambda_function="get_transactions")
            ],
        ),
        
        # 4. Get Market Prices
        LambdaFunctionConfig(
            name=f"{project_name}-get-market-prices-{environment}",
            handler="get_market_prices.lambda_handler",
            memory_mb=256,
            timeout_seconds=15,
            environment_vars={
                **common_env_vars,
                "DYNAMODB_TABLE_MARKET_PRICES": f"{project_name}-market-prices-{environment}",
            },
            required_permissions=[
                AWSService.DYNAMODB,
                AWSService.CLOUDWATCH_LOGS,
            ],
            dynamodb_tables=[f"{project_name}-market-prices-{environment}"],
            api_routes=[
                APIRoute(path="/prices/{item}", method=HTTPMethod.GET, lambda_function="get_market_prices")
            ],
        ),
        
        # 5. Classify Freshness
        LambdaFunctionConfig(
            name=f"{project_name}-classify-freshness-{environment}",
            handler="classify_freshness.lambda_handler",
            memory_mb=512,
            timeout_seconds=60,
            environment_vars={
                **common_env_vars,
                "S3_BUCKET_IMAGES": f"{project_name}-images-{environment}",
                "SAGEMAKER_ENDPOINT_NAME": "produce-freshness-classifier",
                "DEMO_MODE": "true",  # Use demo mode by default
            },
            required_permissions=[
                AWSService.SAGEMAKER,
                AWSService.S3,
                AWSService.CLOUDWATCH_LOGS,
            ],
            s3_buckets=[f"{project_name}-images-{environment}"],
            api_routes=[
                APIRoute(path="/freshness/classify", method=HTTPMethod.POST, lambda_function="classify_freshness")
            ],
        ),
        
        # 6. Create Marketplace Listing
        LambdaFunctionConfig(
            name=f"{project_name}-create-marketplace-listing-{environment}",
            handler="create_marketplace_listing.lambda_handler",
            memory_mb=256,
            timeout_seconds=30,
            environment_vars={
                **common_env_vars,
                "DYNAMODB_TABLE_MARKETPLACE_LISTINGS": f"{project_name}-marketplace-listings-{environment}",
                "DYNAMODB_TABLE_VENDORS": f"{project_name}-vendors-{environment}",
            },
            required_permissions=[
                AWSService.DYNAMODB,
                AWSService.CLOUDWATCH_LOGS,
            ],
            dynamodb_tables=[
                f"{project_name}-marketplace-listings-{environment}",
                f"{project_name}-vendors-{environment}",
            ],
            api_routes=[
                APIRoute(path="/marketplace/listings", method=HTTPMethod.POST, lambda_function="create_marketplace_listing")
            ],
        ),
        
        # 7. Get Marketplace Buyers
        LambdaFunctionConfig(
            name=f"{project_name}-get-marketplace-buyers-{environment}",
            handler="get_marketplace_buyers.lambda_handler",
            memory_mb=256,
            timeout_seconds=15,
            environment_vars={
                **common_env_vars,
                "DYNAMODB_TABLE_VENDORS": f"{project_name}-vendors-{environment}",
            },
            required_permissions=[
                AWSService.DYNAMODB,
                AWSService.CLOUDWATCH_LOGS,
            ],
            dynamodb_tables=[f"{project_name}-vendors-{environment}"],
            api_routes=[
                APIRoute(path="/marketplace/buyers", method=HTTPMethod.GET, lambda_function="get_marketplace_buyers")
            ],
        ),
        
        # 8. Notify Marketplace Buyers
        LambdaFunctionConfig(
            name=f"{project_name}-notify-marketplace-buyers-{environment}",
            handler="notify_marketplace_buyers.lambda_handler",
            memory_mb=256,
            timeout_seconds=30,
            environment_vars={
                **common_env_vars,
                "DYNAMODB_TABLE_MARKETPLACE_LISTINGS": f"{project_name}-marketplace-listings-{environment}",
                "DYNAMODB_TABLE_VENDORS": f"{project_name}-vendors-{environment}",
            },
            required_permissions=[
                AWSService.DYNAMODB,
                AWSService.CLOUDWATCH_LOGS,
            ],
            dynamodb_tables=[
                f"{project_name}-marketplace-listings-{environment}",
                f"{project_name}-vendors-{environment}",
            ],
            api_routes=[
                APIRoute(path="/marketplace/notify", method=HTTPMethod.POST, lambda_function="notify_marketplace_buyers")
            ],
        ),
        
        # 9. Get Trust Score
        LambdaFunctionConfig(
            name=f"{project_name}-get-trust-score-{environment}",
            handler="get_trust_score.lambda_handler",
            memory_mb=256,
            timeout_seconds=15,
            environment_vars={
                **common_env_vars,
                "DYNAMODB_TABLE_VENDORS": f"{project_name}-vendors-{environment}",
                "DYNAMODB_TABLE_TRANSACTIONS": f"{project_name}-transactions-{environment}",
                "DYNAMODB_TABLE_MARKETPLACE_LISTINGS": f"{project_name}-marketplace-listings-{environment}",
            },
            required_permissions=[
                AWSService.DYNAMODB,
                AWSService.CLOUDWATCH_LOGS,
            ],
            dynamodb_tables=[
                f"{project_name}-vendors-{environment}",
                f"{project_name}-transactions-{environment}",
                f"{project_name}-marketplace-listings-{environment}",
            ],
            api_routes=[
                APIRoute(path="/trust-score/{vendor_id}", method=HTTPMethod.GET, lambda_function="get_trust_score")
            ],
        ),
    ]
    
    return DeploymentConfiguration(
        aws_region=aws_region,
        environment=environment,
        project_name=project_name,
        lambda_functions=lambda_functions,
        dynamodb_tables=dynamodb_tables,
        s3_buckets=s3_buckets,
    )
