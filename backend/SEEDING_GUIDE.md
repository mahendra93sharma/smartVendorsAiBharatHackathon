# Demo Data Seeding Guide

This guide explains how to use the `seed_data.py` script to populate DynamoDB tables with demo data for the Smart Vendors hackathon submission.

## Overview

The seeding script creates realistic demo data for the Smart Vendors application:
- **5 vendors** including a demo account
- **20 transactions** distributed across vendors
- **10 market prices** from Delhi-NCR mandis
- **5 marketplace listings** for B-Grade produce

## Prerequisites

1. **AWS Infrastructure**: DynamoDB tables must be created first
   ```bash
   cd infrastructure/terraform
   terraform init
   terraform apply
   ```

2. **Python Dependencies**: Install required packages
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **AWS Credentials**: Configure AWS credentials
   ```bash
   export AWS_ACCESS_KEY_ID=your_access_key
   export AWS_SECRET_ACCESS_KEY=your_secret_key
   export AWS_REGION=ap-south-1
   ```

4. **Environment Variables**: Set DynamoDB table names (optional, defaults provided)
   ```bash
   export DYNAMODB_TABLE_VENDORS=smart-vendors-vendors-dev
   export DYNAMODB_TABLE_TRANSACTIONS=smart-vendors-transactions-dev
   export DYNAMODB_TABLE_MARKET_PRICES=smart-vendors-market-prices-dev
   export DYNAMODB_TABLE_MARKETPLACE_LISTINGS=smart-vendors-marketplace-listings-dev
   ```

## Usage

### Basic Usage

Run the script from the backend directory:

```bash
cd backend
python seed_data.py
```

### Using .env File

Create a `.env` file in the backend directory:

```bash
AWS_REGION=ap-south-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
DYNAMODB_TABLE_VENDORS=smart-vendors-vendors-dev
DYNAMODB_TABLE_TRANSACTIONS=smart-vendors-transactions-dev
DYNAMODB_TABLE_MARKET_PRICES=smart-vendors-market-prices-dev
DYNAMODB_TABLE_MARKETPLACE_LISTINGS=smart-vendors-marketplace-listings-dev
```

Then run:

```bash
python seed_data.py
```

## Demo Data Details

### Vendors

The script creates 5 vendor profiles:

1. **Demo Vendor** (for evaluator testing)
   - Phone: +919876543210
   - District: South Delhi
   - Language: Hindi
   - Trust Score: 100 (Silver tier)

2. **Rajesh Kumar**
   - Phone: +919876543211
   - District: North Delhi
   - Language: Hindi
   - Trust Score: 250 (Gold tier)

3. **Priya Sharma**
   - Phone: +919876543212
   - District: East Delhi
   - Language: English
   - Trust Score: 150 (Silver tier)

4. **Amit Singh**
   - Phone: +919876543213
   - District: West Delhi
   - Language: Hindi
   - Trust Score: 50 (Bronze tier)

5. **Sunita Devi**
   - Phone: +919876543214
   - District: Central Delhi
   - Language: Hindi
   - Trust Score: 180 (Silver tier)

### Transactions

- **Count**: 20 transactions
- **Distribution**: Randomly distributed across all vendors
- **Items**: tomatoes, potatoes, onions, leafy vegetables, cauliflower
- **Quantities**: 2-20 kg per transaction
- **Prices**: Within realistic ranges (₹10-100/kg)
- **Timestamps**: Within last 7 days
- **Recording Method**: Mix of "voice" and "manual"

### Market Prices

- **Count**: 10 price records (9 total: 3 items × 3 mandis)
- **Mandis**: 
  - Azadpur Mandi (12.5 km)
  - Ghazipur Mandi (18.3 km)
  - Okhla Mandi (15.7 km)
- **Items**: tomatoes, potatoes, onions
- **Prices**: ₹20-60/kg with realistic variations
- **Freshness**: Timestamps within last 6 hours
- **TTL**: Auto-expire after 24 hours

### Marketplace Listings

- **Count**: 5 listings
- **Condition**: All B-Grade produce
- **Weight**: 5-15 kg per listing
- **Pricing**: 40-60% discount from normal prices
- **Status**: Mix of active (70%), sold (20%), expired (10%)
- **Timestamps**: Within last 2 days
- **Mandi Credits**: 10 credits per kg
- **Buyers Notified**: 3-10 buyers per listing

## Demo Credentials

After seeding, use these credentials to test the application:

```
Username: demo_vendor
Password: hackathon2024
Phone: +919876543210
```

## Batch Write Performance

The script uses DynamoDB batch writes for optimal performance:

- **Vendors**: Batch write of 5 items
- **Transactions**: Batch write of 20 items
- **Market Prices**: Batch write of 9 items
- **Marketplace Listings**: Batch write of 5 items

Batch writes reduce API calls and improve throughput compared to individual `put_item` operations.

## Verification

After running the script, verify the data in AWS Console:

1. Go to DynamoDB → Tables
2. Select each table and click "Explore table items"
3. Verify item counts:
   - Vendors: 5 items
   - Transactions: 20 items
   - Market Prices: 9 items
   - Marketplace Listings: 5 items

## Troubleshooting

### Table Not Found Error

```
❌ Table not found: smart-vendors-vendors-dev
```

**Solution**: Run Terraform to create the infrastructure first:
```bash
cd infrastructure/terraform
terraform apply
```

### AWS Credentials Error

```
❌ Error checking tables: Unable to locate credentials
```

**Solution**: Configure AWS credentials:
```bash
aws configure
# OR
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
```

### Permission Denied Error

```
❌ Error creating vendor: AccessDeniedException
```

**Solution**: Ensure your IAM user/role has DynamoDB permissions:
- `dynamodb:PutItem`
- `dynamodb:BatchWriteItem`
- `dynamodb:ListTables`

### Import Error

```
ModuleNotFoundError: No module named 'boto3'
```

**Solution**: Install dependencies:
```bash
pip install -r requirements.txt
```

## Re-running the Script

The script can be run multiple times. Each run will:
- Create new vendor IDs (duplicates allowed, different IDs)
- Add new transactions (accumulates)
- Add new market prices (old ones expire via TTL)
- Add new marketplace listings (accumulates)

To start fresh, delete all items from the tables first:

```bash
# Using AWS CLI
aws dynamodb scan --table-name smart-vendors-vendors-dev --attributes-to-get vendor_id --output json | \
  jq -r '.Items[].vendor_id.S' | \
  xargs -I {} aws dynamodb delete-item --table-name smart-vendors-vendors-dev --key '{"vendor_id":{"S":"{}"}}'
```

Or use the AWS Console to delete items manually.

## Script Output

Expected output when running successfully:

```
============================================================
Smart Vendors - Demo Data Seeding Script
============================================================
Verifying DynamoDB tables...
✓ Found table: smart-vendors-vendors-dev
✓ Found table: smart-vendors-transactions-dev
✓ Found table: smart-vendors-market-prices-dev
✓ Found table: smart-vendors-marketplace-listings-dev

📝 Seeding vendors...
  ✓ Created vendor: Demo Vendor (ID: 550e8400...)
  ✓ Created vendor: Rajesh Kumar (ID: 660e8400...)
  ✓ Created vendor: Priya Sharma (ID: 770e8400...)
  ✓ Created vendor: Amit Singh (ID: 880e8400...)
  ✓ Created vendor: Sunita Devi (ID: 990e8400...)
✅ Created 5 vendors

📝 Seeding 20 transactions...
  ✓ Created 5/20 transactions...
  ✓ Created 10/20 transactions...
  ✓ Created 15/20 transactions...
  ✓ Created 20/20 transactions...
✅ Created 20 transactions

📝 Seeding 10 market prices...
  ✓ Created price: tomatoes at Azadpur Mandi - ₹35.0/kg
  ✓ Created price: tomatoes at Ghazipur Mandi - ₹38.0/kg
  ✓ Created price: tomatoes at Okhla Mandi - ₹33.0/kg
  ✓ Created price: potatoes at Azadpur Mandi - ₹23.0/kg
  ✓ Created price: potatoes at Ghazipur Mandi - ₹26.0/kg
  ✓ Created price: potatoes at Okhla Mandi - ₹24.0/kg
  ✓ Created price: onions at Azadpur Mandi - ₹44.0/kg
  ✓ Created price: onions at Ghazipur Mandi - ₹41.0/kg
  ✓ Created price: onions at Okhla Mandi - ₹46.0/kg
✅ Created 9 market prices

📝 Seeding 5 marketplace listings...
  ✓ Created listing: 8.5kg tomatoes - ₹127.5 (active)
  ✓ Created listing: 12.3kg potatoes - ₹153.75 (active)
  ✓ Created listing: 6.7kg onions - ₹142.8 (sold)
  ✓ Created listing: 10.2kg leafy vegetables - ₹102.0 (active)
  ✓ Created listing: 14.8kg cauliflower - ₹370.0 (active)
✅ Created 5 marketplace listings

============================================================
✅ Data Seeding Complete!
============================================================

Demo Credentials:
  Username: demo_vendor
  Password: hackathon2024
  Phone: +919876543210

Vendor IDs created:
  1. Demo Vendor: 550e8400-e29b-41d4-a716-446655440000
  2. Rajesh Kumar: 660e8400-e29b-41d4-a716-446655440001
  3. Priya Sharma: 770e8400-e29b-41d4-a716-446655440002
  4. Amit Singh: 880e8400-e29b-41d4-a716-446655440003
  5. Sunita Devi: 990e8400-e29b-41d4-a716-446655440004

============================================================
```

## Next Steps

After seeding the data:

1. **Test the API**: Use the demo credentials to test Lambda functions
2. **Verify Frontend**: Check that the frontend displays the seeded data
3. **Demo Video**: Use the demo account for recording the hackathon video
4. **Documentation**: Include demo credentials in README.md

## References

- [DynamoDB Batch Operations](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/batch-operations.html)
- [DynamoDB TTL](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html)
- [Boto3 DynamoDB](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html)
