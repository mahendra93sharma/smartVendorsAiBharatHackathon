# Task 2.2 Verification: DynamoDB Table Schemas

## Task Summary

**Task**: Define DynamoDB table schemas and create infrastructure  
**Status**: ✅ Complete  
**Date**: 2024-01-15

## Requirements Verification

### ✅ Requirement 1: Design DynamoDB Tables

All four required tables have been designed with appropriate keys and indexes:

#### 1. Vendors Table
- **Partition Key**: `vendor_id` (String) ✅
- **GSI**: `phone_number_index` on `phone_number` ✅
- **Purpose**: Store vendor profiles and authentication data
- **Location**: `infrastructure/terraform/main.tf` lines 91-115

#### 2. Transactions Table
- **Partition Key**: `transaction_id` (String) ✅
- **GSI**: `vendor_id_index` on `vendor_id` with sort key `timestamp` ✅
- **Purpose**: Record all sales transactions
- **Location**: `infrastructure/terraform/main.tf` lines 117-147

#### 3. MarketPrices Table
- **Partition Key**: `item_name` (String) ✅
- **Sort Key**: `timestamp` (String) ✅
- **TTL**: Configured on `ttl` attribute ✅
- **Purpose**: Cache market price data with automatic expiration
- **Location**: `infrastructure/terraform/main.tf` lines 149-173

#### 4. MarketplaceListings Table
- **Partition Key**: `listing_id` (String) ✅
- **GSI**: `vendor_id_index` on `vendor_id` with sort key `created_at` ✅
- **Purpose**: Manage B-Grade produce listings
- **Location**: `infrastructure/terraform/main.tf` lines 175-205

### ✅ Requirement 2: Create Tables Using Terraform

All tables are defined in Terraform configuration:

- **File**: `infrastructure/terraform/main.tf`
- **Billing Mode**: `PAY_PER_REQUEST` (on-demand capacity) ✅
- **Resource Type**: `aws_dynamodb_table` ✅
- **Naming Convention**: `${var.project_name}-{table}-${var.environment}` ✅

**Benefits of On-Demand Capacity**:
- No capacity planning required
- Automatic scaling based on traffic
- Cost-effective for variable workloads
- Ideal for hackathon demo with unpredictable load

### ✅ Requirement 3: Configure TTL for MarketPrices

TTL configuration verified in `market_prices` table:

```hcl
ttl {
  attribute_name = "ttl"
  enabled        = true
}
```

- **Attribute**: `ttl` (Unix timestamp) ✅
- **Enabled**: `true` ✅
- **Expiration**: 24 hours after creation ✅
- **Purpose**: Automatically remove stale price data

**TTL Implementation**:
```python
import time
ttl = int(time.time()) + (24 * 60 * 60)  # Current time + 24 hours
```

## Infrastructure Verification

### Terraform Configuration Files

1. **main.tf** ✅
   - 4 DynamoDB tables defined
   - All required attributes and indexes configured
   - IAM roles and policies for Lambda access
   - S3 buckets, CloudFront, and API Gateway

2. **variables.tf** ✅
   - `aws_region`: ap-south-1 (Mumbai)
   - `project_name`: smart-vendors
   - `environment`: dev

3. **outputs.tf** ✅
   - All DynamoDB table names exported
   - Lambda execution role ARN
   - API Gateway and CloudFront endpoints

### IAM Permissions

Lambda execution role includes DynamoDB permissions:

```json
{
  "Effect": "Allow",
  "Action": [
    "dynamodb:GetItem",
    "dynamodb:PutItem",
    "dynamodb:UpdateItem",
    "dynamodb:DeleteItem",
    "dynamodb:Query",
    "dynamodb:Scan",
    "dynamodb:BatchWriteItem"
  ],
  "Resource": [
    "arn:aws:dynamodb:*:*:table/smart-vendors-vendors-dev",
    "arn:aws:dynamodb:*:*:table/smart-vendors-transactions-dev",
    "arn:aws:dynamodb:*:*:table/smart-vendors-market-prices-dev",
    "arn:aws:dynamodb:*:*:table/smart-vendors-marketplace-listings-dev",
    "arn:aws:dynamodb:*:*:table/smart-vendors-*/index/*"
  ]
}
```

## Documentation Created

### 1. DYNAMODB_SCHEMAS.md ✅

Comprehensive documentation including:

- **Overview**: All 4 tables with purpose and billing mode
- **Table Definitions**: Detailed schema for each table
  - Primary keys and sort keys
  - All attributes with data types
  - Global Secondary Indexes
  - Example items in JSON format
  - Access patterns
- **TTL Configuration**: Detailed explanation and code examples
- **Data Types and Constraints**: String formats, numeric ranges, enumerations
- **Terraform Configuration**: Code snippets and deployment commands
- **IAM Permissions**: Required permissions for Lambda functions
- **Best Practices**: Partition key design, GSI usage, query optimization
- **Data Seeding**: Example code for populating demo data
- **Monitoring**: CloudWatch metrics and alarms

**Location**: `docs/DYNAMODB_SCHEMAS.md`

## Schema Design Validation

### Access Pattern Analysis

#### Vendors Table
- ✅ Get vendor by ID: `GetItem` on `vendor_id`
- ✅ Find vendor by phone: `Query` on `phone_number_index`
- ✅ Update trust score: `UpdateItem` on `vendor_id`

#### Transactions Table
- ✅ Get transaction by ID: `GetItem` on `transaction_id`
- ✅ Get vendor's transactions: `Query` on `vendor_id_index`
- ✅ Get recent transactions: `Query` with timestamp range

#### MarketPrices Table
- ✅ Get latest prices for item: `Query` on `item_name` with descending sort
- ✅ Get prices from specific time: `Query` with timestamp range
- ✅ Automatic expiration: TTL removes stale data after 24 hours

#### MarketplaceListings Table
- ✅ Get listing by ID: `GetItem` on `listing_id`
- ✅ Get vendor's listings: `Query` on `vendor_id_index`
- ✅ Get active listings: `Query` with filter on `status`

### Data Model Validation

All tables follow DynamoDB best practices:

1. **High-Cardinality Partition Keys** ✅
   - Using UUIDs for `vendor_id`, `transaction_id`, `listing_id`
   - Ensures even distribution across partitions
   - Avoids hot partition issues

2. **Efficient GSI Design** ✅
   - GSIs support alternate access patterns
   - Projection type ALL for flexibility
   - Sort keys enable range queries

3. **Appropriate Data Types** ✅
   - Strings for IDs, timestamps, text
   - Numbers for quantities, prices, scores
   - Consistent timestamp format (ISO 8601)

4. **TTL for Time-Sensitive Data** ✅
   - Market prices expire after 24 hours
   - Reduces storage costs
   - Ensures data freshness

## Deployment Status

### Infrastructure Created in Task 1 ✅

The Terraform infrastructure was already created in Task 1:

- S3 buckets for images, static assets, ML models
- DynamoDB tables (all 4 tables)
- Lambda execution role with permissions
- CloudFront distribution for frontend
- API Gateway for Lambda routing

### Verification Commands

To verify the infrastructure:

```bash
# Check Terraform state
cd infrastructure/terraform
terraform show

# List DynamoDB tables
aws dynamodb list-tables --region ap-south-1

# Describe specific table
aws dynamodb describe-table \
  --table-name smart-vendors-vendors-dev \
  --region ap-south-1

# Check TTL configuration
aws dynamodb describe-time-to-live \
  --table-name smart-vendors-market-prices-dev \
  --region ap-south-1
```

## Next Steps

Task 2.2 is complete. The next task is:

**Task 2.3**: Implement demo data seeding script for DynamoDB
- Create `seed_data.py` script
- Populate 5 vendors, 20 transactions, 10 market prices, 5 listings
- Use realistic Delhi-NCR data
- Include demo vendor account credentials

## Validates Requirements

This task validates **Requirement 8.6**:

> "WHEN the repository includes database schemas, THE GitHub_Repository SHALL provide migration scripts or schema definition files"

✅ Schema definition files provided:
- Terraform configuration: `infrastructure/terraform/main.tf`
- Documentation: `docs/DYNAMODB_SCHEMAS.md`
- Verification: `docs/TASK_2.2_VERIFICATION.md`

## Summary

All requirements for Task 2.2 have been met:

1. ✅ Four DynamoDB tables designed with correct keys and indexes
2. ✅ Tables created using Terraform with on-demand capacity
3. ✅ TTL configured for market_prices table (24-hour expiration)
4. ✅ Comprehensive documentation created
5. ✅ IAM permissions configured for Lambda access
6. ✅ Best practices followed for schema design

The DynamoDB infrastructure is ready for the demo data seeding script (Task 2.3).
