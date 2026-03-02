# DynamoDB Table Schemas

This document describes the DynamoDB table schemas used in the Smart Vendors application.

## Overview

The application uses four DynamoDB tables with on-demand billing mode (PAY_PER_REQUEST) for cost efficiency and automatic scaling:

1. **Vendors** - Store vendor profiles and account information
2. **Transactions** - Record all sales transactions
3. **MarketPrices** - Cache market price data with TTL
4. **MarketplaceListings** - Manage B-Grade produce listings

## Table Definitions

### 1. Vendors Table

**Table Name**: `smart-vendors-vendors-{environment}`

**Purpose**: Store vendor profiles, authentication, and trust score information.

**Primary Key**:
- **Partition Key**: `vendor_id` (String) - UUID identifier

**Attributes**:
- `vendor_id` (String) - Unique vendor identifier (UUID)
- `phone_number` (String) - Vendor's phone number (unique)
- `name` (String) - Vendor's display name
- `preferred_language` (String) - Language preference (hi, en)
- `district` (String) - Delhi-NCR district location
- `trust_score` (Number) - Calculated trust score (0-1000)
- `tier` (String) - Trust tier (Bronze, Silver, Gold)
- `created_at` (String) - ISO 8601 timestamp

**Global Secondary Indexes**:
- **phone_number_index**
  - Partition Key: `phone_number` (String)
  - Projection: ALL
  - Purpose: Enable vendor lookup by phone number for authentication

**Example Item**:
```json
{
  "vendor_id": "550e8400-e29b-41d4-a716-446655440000",
  "phone_number": "+919876543210",
  "name": "Rajesh Kumar",
  "preferred_language": "hi",
  "district": "South Delhi",
  "trust_score": 150,
  "tier": "Silver",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Access Patterns**:
- Get vendor by ID: `GetItem` on `vendor_id`
- Find vendor by phone: `Query` on `phone_number_index`
- Update trust score: `UpdateItem` on `vendor_id`

---

### 2. Transactions Table

**Table Name**: `smart-vendors-transactions-{environment}`

**Purpose**: Record all sales transactions for vendors.

**Primary Key**:
- **Partition Key**: `transaction_id` (String) - UUID identifier

**Attributes**:
- `transaction_id` (String) - Unique transaction identifier (UUID)
- `vendor_id` (String) - Reference to vendor
- `item_name` (String) - Produce item name
- `quantity` (Number) - Quantity sold
- `unit` (String) - Unit of measurement (kg, piece, dozen)
- `price_per_unit` (Number) - Price per unit in rupees
- `total_amount` (Number) - Total transaction amount
- `timestamp` (String) - ISO 8601 timestamp
- `recorded_via` (String) - Recording method (voice, manual)

**Global Secondary Indexes**:
- **vendor_id_index**
  - Partition Key: `vendor_id` (String)
  - Sort Key: `timestamp` (String)
  - Projection: ALL
  - Purpose: Query all transactions for a vendor, sorted by time

**Example Item**:
```json
{
  "transaction_id": "660e8400-e29b-41d4-a716-446655440001",
  "vendor_id": "550e8400-e29b-41d4-a716-446655440000",
  "item_name": "tomatoes",
  "quantity": 5.0,
  "unit": "kg",
  "price_per_unit": 40.0,
  "total_amount": 200.0,
  "timestamp": "2024-01-15T14:30:00Z",
  "recorded_via": "voice"
}
```

**Access Patterns**:
- Get transaction by ID: `GetItem` on `transaction_id`
- Get vendor's transactions: `Query` on `vendor_id_index` with `vendor_id`
- Get recent transactions: `Query` on `vendor_id_index` with `vendor_id` and timestamp range

---

### 3. MarketPrices Table

**Table Name**: `smart-vendors-market-prices-{environment}`

**Purpose**: Cache market price data from various mandis with automatic expiration.

**Primary Key**:
- **Partition Key**: `item_name` (String) - Produce item name
- **Sort Key**: `timestamp` (String) - ISO 8601 timestamp

**Attributes**:
- `item_name` (String) - Produce item name (normalized)
- `timestamp` (String) - ISO 8601 timestamp
- `mandi_name` (String) - Market name (Azadpur, Ghazipur, Okhla)
- `price_per_kg` (Number) - Price per kilogram in rupees
- `distance_km` (Number) - Distance from reference point
- `ttl` (Number) - Unix timestamp for TTL expiration (24 hours)

**TTL Configuration**:
- **Attribute**: `ttl`
- **Enabled**: Yes
- **Expiration**: 24 hours after creation
- **Purpose**: Automatically remove stale price data

**Example Item**:
```json
{
  "item_name": "tomatoes",
  "timestamp": "2024-01-15T06:00:00Z",
  "mandi_name": "Azadpur Mandi",
  "price_per_kg": 35.0,
  "distance_km": 12.5,
  "ttl": 1705392000
}
```

**Access Patterns**:
- Get latest prices for item: `Query` on `item_name` with `ScanIndexForward=false` and `Limit=10`
- Get prices from specific time: `Query` on `item_name` with timestamp range

**TTL Calculation**:
```python
import time
ttl = int(time.time()) + (24 * 60 * 60)  # Current time + 24 hours
```

---

### 4. MarketplaceListings Table

**Table Name**: `smart-vendors-marketplace-listings-{environment}`

**Purpose**: Manage B-Grade produce listings for the waste marketplace.

**Primary Key**:
- **Partition Key**: `listing_id` (String) - UUID identifier

**Attributes**:
- `listing_id` (String) - Unique listing identifier (UUID)
- `vendor_id` (String) - Reference to vendor
- `item_name` (String) - Produce item name
- `weight_kg` (Number) - Weight in kilograms
- `condition` (String) - Produce condition (B-Grade, Waste)
- `price` (Number) - Listing price in rupees
- `status` (String) - Listing status (active, sold, expired)
- `created_at` (String) - ISO 8601 timestamp
- `buyers_notified` (Number) - Count of buyers notified
- `mandi_credits_earned` (Number) - Credits earned from sale

**Global Secondary Indexes**:
- **vendor_id_index**
  - Partition Key: `vendor_id` (String)
  - Sort Key: `created_at` (String)
  - Projection: ALL
  - Purpose: Query all listings for a vendor, sorted by creation time

**Example Item**:
```json
{
  "listing_id": "770e8400-e29b-41d4-a716-446655440002",
  "vendor_id": "550e8400-e29b-41d4-a716-446655440000",
  "item_name": "tomatoes",
  "weight_kg": 10.0,
  "condition": "B-Grade",
  "price": 250.0,
  "status": "active",
  "created_at": "2024-01-15T16:00:00Z",
  "buyers_notified": 5,
  "mandi_credits_earned": 100
}
```

**Access Patterns**:
- Get listing by ID: `GetItem` on `listing_id`
- Get vendor's listings: `Query` on `vendor_id_index` with `vendor_id`
- Get active listings: `Query` on `vendor_id_index` with filter on `status=active`

---

## Billing Mode

All tables use **PAY_PER_REQUEST** (on-demand) billing mode:

**Benefits**:
- No capacity planning required
- Automatic scaling based on traffic
- Cost-effective for variable workloads
- Pay only for actual reads/writes

**Cost Structure**:
- Write Request Units (WRU): $1.25 per million writes
- Read Request Units (RRU): $0.25 per million reads
- Storage: $0.25 per GB-month

---

## Data Types and Constraints

### String Formats

- **UUID**: Standard UUID v4 format (e.g., `550e8400-e29b-41d4-a716-446655440000`)
- **Phone Number**: E.164 format with country code (e.g., `+919876543210`)
- **Timestamp**: ISO 8601 format (e.g., `2024-01-15T10:30:00Z`)
- **TTL**: Unix timestamp (seconds since epoch)

### Numeric Ranges

- **trust_score**: 0 to 1000
- **quantity**: 0.1 to 1000.0
- **price_per_unit**: 1.0 to 10000.0
- **distance_km**: 0.0 to 100.0

### Enumerations

- **preferred_language**: `hi`, `en`
- **tier**: `Bronze`, `Silver`, `Gold`
- **unit**: `kg`, `piece`, `dozen`, `bundle`
- **recorded_via**: `voice`, `manual`
- **condition**: `Fresh`, `B-Grade`, `Waste`
- **status**: `active`, `sold`, `expired`

---

## Terraform Configuration

The tables are defined in `infrastructure/terraform/main.tf`:

```hcl
resource "aws_dynamodb_table" "vendors" {
  name           = "${var.project_name}-vendors-${var.environment}"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "vendor_id"
  
  attribute {
    name = "vendor_id"
    type = "S"
  }
  
  attribute {
    name = "phone_number"
    type = "S"
  }
  
  global_secondary_index {
    name            = "phone_number_index"
    hash_key        = "phone_number"
    projection_type = "ALL"
  }
}
```

**Deployment**:
```bash
cd infrastructure/terraform
terraform init
terraform plan
terraform apply
```

---

## IAM Permissions

Lambda functions require the following DynamoDB permissions:

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
    "arn:aws:dynamodb:*:*:table/smart-vendors-*",
    "arn:aws:dynamodb:*:*:table/smart-vendors-*/index/*"
  ]
}
```

---

## Best Practices

### 1. Partition Key Design
- Use high-cardinality keys (UUID) to distribute load evenly
- Avoid hot partitions by not using sequential IDs

### 2. GSI Usage
- Use GSIs for alternate access patterns
- Project only needed attributes to reduce storage costs
- Consider eventual consistency for GSI queries

### 3. TTL Configuration
- Use TTL for time-sensitive data (market prices)
- Set TTL attribute as Unix timestamp
- DynamoDB deletes expired items within 48 hours

### 4. Batch Operations
- Use `BatchWriteItem` for seeding data (up to 25 items)
- Use `BatchGetItem` for reading multiple items
- Handle unprocessed items with retry logic

### 5. Query Optimization
- Use `Query` instead of `Scan` when possible
- Add filters after query to reduce data transfer
- Use pagination with `LastEvaluatedKey` for large result sets

---

## Data Seeding

Demo data is populated using `backend/seed_data.py`:

```python
import boto3
from datetime import datetime, timedelta
import uuid

dynamodb = boto3.resource('dynamodb')
vendors_table = dynamodb.Table('smart-vendors-vendors-dev')

# Create demo vendor
vendors_table.put_item(Item={
    'vendor_id': str(uuid.uuid4()),
    'phone_number': '+919876543210',
    'name': 'Demo Vendor',
    'preferred_language': 'hi',
    'district': 'South Delhi',
    'trust_score': 100,
    'tier': 'Silver',
    'created_at': datetime.utcnow().isoformat() + 'Z'
})
```

---

## Monitoring and Maintenance

### CloudWatch Metrics
- `ConsumedReadCapacityUnits`
- `ConsumedWriteCapacityUnits`
- `UserErrors` (throttling, validation errors)
- `SystemErrors` (service errors)

### Alarms
- Set alarms for high error rates
- Monitor TTL deletion lag
- Track GSI throttling

### Backup Strategy
- Enable Point-in-Time Recovery (PITR) for production
- Use on-demand backups before major changes
- Test restore procedures regularly

---

## References

- [DynamoDB Best Practices](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html)
- [DynamoDB TTL](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html)
- [DynamoDB GSI](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GSI.html)
- [Terraform AWS DynamoDB](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/dynamodb_table)
