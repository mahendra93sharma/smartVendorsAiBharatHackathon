# Smart Vendors - Database ER Diagram

## Entity-Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         SMART VENDORS DATABASE SCHEMA                        │
│                              DynamoDB Tables (4)                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────┐
│         VENDORS                  │
├──────────────────────────────────┤
│ PK: vendor_id (String)           │
├──────────────────────────────────┤
│ name (String)                    │
│ phone (String)                   │
│ location (String)                │
│ business_type (String)           │
│ registration_date (String)       │
│ trust_score (Number)             │
│ total_transactions (Number)      │
│ total_revenue (Number)           │
│ language_preference (String)     │
│ status (String)                  │
│ created_at (String)              │
│ updated_at (String)              │
└──────────────────────────────────┘
         │
         │ 1
         │
         │ has many
         │
         │ N
         ▼
┌──────────────────────────────────┐
│      TRANSACTIONS                │
├──────────────────────────────────┤
│ PK: vendor_id (String)           │
│ SK: timestamp (String)           │
├──────────────────────────────────┤
│ transaction_id (String)          │
│ items (List)                     │
│   ├─ item_name (String)          │
│   ├─ quantity (Number)           │
│   ├─ unit (String)               │
│   ├─ price_per_unit (Number)     │
│   └─ total_price (Number)        │
│ total_amount (Number)            │
│ payment_method (String)          │
│ customer_type (String)           │
│ transcription_text (String)      │
│ language_code (String)           │
│ created_at (String)              │
│ updated_at (String)              │
└──────────────────────────────────┘


┌──────────────────────────────────┐
│      MARKET_PRICES               │
├──────────────────────────────────┤
│ PK: item_name (String)           │
│ SK: timestamp (String)           │
├──────────────────────────────────┤
│ price_id (String)                │
│ market_name (String)             │
│ location (String)                │
│ price_per_kg (Number)            │
│ min_price (Number)               │
│ max_price (Number)               │
│ avg_price (Number)               │
│ quality_grade (String)           │
│ availability (String)            │
│ source (String)                  │
│ date (String)                    │
│ created_at (String)              │
│ updated_at (String)              │
└──────────────────────────────────┘


┌──────────────────────────────────┐
│   MARKETPLACE_LISTINGS           │
├──────────────────────────────────┤
│ PK: listing_id (String)          │
│ SK: timestamp (String)           │
├──────────────────────────────────┤
│ vendor_id (String) ───────┐      │
│ item_name (String)        │      │
│ quantity (Number)         │      │
│ unit (String)             │      │
│ grade (String)            │      │
│ original_price (Number)   │      │
│ discounted_price (Number) │      │
│ discount_percentage (Number)     │
│ freshness_score (Number)  │      │
│ expiry_date (String)      │      │
│ location (String)         │      │
│ images (List<String>)     │      │
│ description (String)      │      │
│ status (String)           │      │
│ views (Number)            │      │
│ interested_buyers (List)  │      │
│ created_at (String)       │      │
│ updated_at (String)       │      │
└───────────────────────────┼──────┘
                            │
                            │ references
                            │
                            └──────────────┐
                                          │
                                          ▼
                            ┌──────────────────────────────┐
                            │         VENDORS              │
                            └──────────────────────────────┘
```

---

## Detailed Entity Descriptions

### 1. VENDORS Table

**Purpose**: Store vendor profile information and business metrics

**Primary Key**: `vendor_id` (Partition Key)

**Attributes**:
- `vendor_id` (String, PK): Unique identifier for vendor
- `name` (String): Vendor's full name
- `phone` (String): Contact phone number
- `location` (String): Business location/address
- `business_type` (String): Type of business (e.g., "vegetable", "fruit", "grocery")
- `registration_date` (String): Date when vendor registered
- `trust_score` (Number): Reputation score (0-100)
- `total_transactions` (Number): Count of all transactions
- `total_revenue` (Number): Cumulative revenue in rupees
- `language_preference` (String): Preferred language code (e.g., "hi-IN", "en-IN")
- `status` (String): Account status ("active", "inactive", "suspended")
- `created_at` (String): ISO timestamp of creation
- `updated_at` (String): ISO timestamp of last update

**Relationships**:
- One-to-Many with TRANSACTIONS
- One-to-Many with MARKETPLACE_LISTINGS

**Indexes**:
- GSI on `location` for location-based queries
- GSI on `trust_score` for ranking vendors

---

### 2. TRANSACTIONS Table

**Purpose**: Store all sales transactions with detailed item information

**Primary Key**: 
- Partition Key: `vendor_id` (String)
- Sort Key: `timestamp` (String)

**Attributes**:
- `vendor_id` (String, PK): Reference to vendor
- `timestamp` (String, SK): ISO timestamp of transaction
- `transaction_id` (String): Unique transaction identifier
- `items` (List): Array of items sold
  - `item_name` (String): Name of produce/item
  - `quantity` (Number): Quantity sold
  - `unit` (String): Unit of measurement ("kg", "piece", "dozen")
  - `price_per_unit` (Number): Price per unit in rupees
  - `total_price` (Number): Total price for this item
- `total_amount` (Number): Total transaction amount in rupees
- `payment_method` (String): Payment type ("cash", "upi", "card")
- `customer_type` (String): Customer category ("retail", "wholesale", "restaurant")
- `transcription_text` (String): Original voice input text
- `language_code` (String): Language used for voice input
- `created_at` (String): ISO timestamp of creation
- `updated_at` (String): ISO timestamp of last update

**Relationships**:
- Many-to-One with VENDORS

**Indexes**:
- GSI on `transaction_id` for direct transaction lookup
- LSI on `total_amount` for revenue analysis

**Query Patterns**:
- Get all transactions for a vendor: Query by `vendor_id`
- Get transactions in date range: Query by `vendor_id` + filter on `timestamp`
- Get daily/weekly/monthly revenue: Aggregate by `vendor_id` + date range

---

### 3. MARKET_PRICES Table

**Purpose**: Store real-time market price data from various sources

**Primary Key**:
- Partition Key: `item_name` (String)
- Sort Key: `timestamp` (String)

**Attributes**:
- `item_name` (String, PK): Name of produce/commodity
- `timestamp` (String, SK): ISO timestamp of price record
- `price_id` (String): Unique price record identifier
- `market_name` (String): Name of mandi/market
- `location` (String): Market location
- `price_per_kg` (Number): Current price per kg in rupees
- `min_price` (Number): Minimum price in market
- `max_price` (Number): Maximum price in market
- `avg_price` (Number): Average price across markets
- `quality_grade` (String): Quality grade ("A", "B", "C")
- `availability` (String): Stock status ("high", "medium", "low")
- `source` (String): Data source ("government_api", "manual", "scraper")
- `date` (String): Date of price (YYYY-MM-DD)
- `created_at` (String): ISO timestamp of creation
- `updated_at` (String): ISO timestamp of last update

**Relationships**:
- No direct relationships (reference data)

**Indexes**:
- GSI on `location` for location-based price queries
- GSI on `date` for historical price analysis

**Query Patterns**:
- Get latest price for item: Query by `item_name` + sort by `timestamp` DESC
- Get price history: Query by `item_name` + date range filter
- Compare prices across markets: Query by `item_name` + group by `market_name`

---

### 4. MARKETPLACE_LISTINGS Table

**Purpose**: Store B-grade produce listings for marketplace

**Primary Key**:
- Partition Key: `listing_id` (String)
- Sort Key: `timestamp` (String)

**Attributes**:
- `listing_id` (String, PK): Unique listing identifier
- `timestamp` (String, SK): ISO timestamp of listing creation
- `vendor_id` (String): Reference to vendor (FK)
- `item_name` (String): Name of produce
- `quantity` (Number): Available quantity
- `unit` (String): Unit of measurement
- `grade` (String): Quality grade ("B", "C")
- `original_price` (Number): Original A-grade price
- `discounted_price` (Number): Discounted B-grade price
- `discount_percentage` (Number): Discount percentage (0-100)
- `freshness_score` (Number): AI-calculated freshness (0-100)
- `expiry_date` (String): Expected expiry date
- `location` (String): Pickup location
- `images` (List<String>): Array of image URLs
- `description` (String): Additional details
- `status` (String): Listing status ("active", "sold", "expired")
- `views` (Number): Number of views
- `interested_buyers` (List): Array of buyer IDs who showed interest
- `created_at` (String): ISO timestamp of creation
- `updated_at` (String): ISO timestamp of last update

**Relationships**:
- Many-to-One with VENDORS

**Indexes**:
- GSI on `vendor_id` for vendor's listings
- GSI on `item_name` for item-based search
- GSI on `status` + `timestamp` for active listings
- GSI on `location` for location-based search

**Query Patterns**:
- Get all active listings: Query by `status` = "active"
- Get vendor's listings: Query by `vendor_id`
- Search by item: Query by `item_name`
- Get listings near location: Query by `location`

---

## Relationships Summary

```
VENDORS (1) ──────< (N) TRANSACTIONS
   │
   │
   └──────< (N) MARKETPLACE_LISTINGS

MARKET_PRICES (Independent reference data)
```

### Relationship Details:

1. **VENDORS → TRANSACTIONS** (One-to-Many)
   - One vendor can have many transactions
   - Foreign Key: `vendor_id` in TRANSACTIONS
   - Cascade: Delete vendor → Archive transactions

2. **VENDORS → MARKETPLACE_LISTINGS** (One-to-Many)
   - One vendor can have many marketplace listings
   - Foreign Key: `vendor_id` in MARKETPLACE_LISTINGS
   - Cascade: Delete vendor → Delete listings

3. **MARKET_PRICES** (No relationships)
   - Independent reference data
   - Used for price intelligence across the platform

---

## DynamoDB Design Patterns

### 1. Single-Table Design Considerations

While we use 4 separate tables for clarity, this could be optimized into a single table:

```
PK                    SK                      Entity Type
─────────────────────────────────────────────────────────
VENDOR#123           METADATA                VENDOR
VENDOR#123           TRANSACTION#2024-03-03  TRANSACTION
VENDOR#123           LISTING#456             LISTING
ITEM#tomatoes        PRICE#2024-03-03        MARKET_PRICE
```

### 2. Access Patterns

**Vendor Operations**:
- Get vendor profile: `GetItem(vendor_id)`
- Update trust score: `UpdateItem(vendor_id, trust_score)`
- List all vendors: `Scan` (with pagination)

**Transaction Operations**:
- Get vendor transactions: `Query(vendor_id)`
- Get transactions by date: `Query(vendor_id, timestamp BETWEEN)`
- Get single transaction: `Query(vendor_id, timestamp)`

**Market Price Operations**:
- Get latest price: `Query(item_name, timestamp DESC, Limit=1)`
- Get price history: `Query(item_name, timestamp BETWEEN)`
- Get all items: `Scan` (with pagination)

**Marketplace Operations**:
- Get active listings: `Query(GSI: status='active')`
- Get vendor listings: `Query(GSI: vendor_id)`
- Search by item: `Query(GSI: item_name)`
- Get listing details: `GetItem(listing_id)`

---

## Data Flow Diagram

```
┌─────────────────┐
│  Voice Input    │
│  "2 kg tomatoes"│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ AWS Transcribe  │
│ + Bedrock       │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────┐
│  Extract Transaction Data       │
│  {                              │
│    vendor_id: "V123",           │
│    items: [{                    │
│      item_name: "tomatoes",     │
│      quantity: 2,               │
│      unit: "kg",                │
│      price: 50                  │
│    }]                           │
│  }                              │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  Write to TRANSACTIONS table    │
│  PK: vendor_id                  │
│  SK: timestamp                  │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  Update VENDORS table           │
│  - Increment total_transactions │
│  - Add to total_revenue         │
│  - Update trust_score           │
└─────────────────────────────────┘
```

---

## Sample Data

### VENDORS Table
```json
{
  "vendor_id": "V001",
  "name": "Ramesh Kumar",
  "phone": "+91-9876543210",
  "location": "Dadar Market, Mumbai",
  "business_type": "vegetable",
  "registration_date": "2024-01-15",
  "trust_score": 85,
  "total_transactions": 1247,
  "total_revenue": 156780,
  "language_preference": "hi-IN",
  "status": "active",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-03-03T14:22:00Z"
}
```

### TRANSACTIONS Table
```json
{
  "vendor_id": "V001",
  "timestamp": "2024-03-03T14:22:00Z",
  "transaction_id": "TXN-20240303-001",
  "items": [
    {
      "item_name": "tomatoes",
      "quantity": 2,
      "unit": "kg",
      "price_per_unit": 25,
      "total_price": 50
    },
    {
      "item_name": "onions",
      "quantity": 1,
      "unit": "kg",
      "price_per_unit": 30,
      "total_price": 30
    }
  ],
  "total_amount": 80,
  "payment_method": "cash",
  "customer_type": "retail",
  "transcription_text": "2 kg tomatoes 50 rupees, 1 kg onions 30 rupees",
  "language_code": "en-IN",
  "created_at": "2024-03-03T14:22:00Z",
  "updated_at": "2024-03-03T14:22:00Z"
}
```

### MARKET_PRICES Table
```json
{
  "item_name": "tomatoes",
  "timestamp": "2024-03-03T06:00:00Z",
  "price_id": "PRICE-20240303-001",
  "market_name": "Vashi APMC",
  "location": "Navi Mumbai",
  "price_per_kg": 28,
  "min_price": 22,
  "max_price": 35,
  "avg_price": 28,
  "quality_grade": "A",
  "availability": "high",
  "source": "government_api",
  "date": "2024-03-03",
  "created_at": "2024-03-03T06:00:00Z",
  "updated_at": "2024-03-03T06:00:00Z"
}
```

### MARKETPLACE_LISTINGS Table
```json
{
  "listing_id": "LIST-20240303-001",
  "timestamp": "2024-03-03T15:00:00Z",
  "vendor_id": "V001",
  "item_name": "tomatoes",
  "quantity": 5,
  "unit": "kg",
  "grade": "B",
  "original_price": 140,
  "discounted_price": 100,
  "discount_percentage": 28.57,
  "freshness_score": 75,
  "expiry_date": "2024-03-05",
  "location": "Dadar Market, Mumbai",
  "images": [
    "s3://smart-vendors-images/V001/tomatoes-001.jpg"
  ],
  "description": "Slightly soft but perfect for cooking",
  "status": "active",
  "views": 12,
  "interested_buyers": ["B001", "B003"],
  "created_at": "2024-03-03T15:00:00Z",
  "updated_at": "2024-03-03T15:30:00Z"
}
```

---

## Database Statistics

### Current Deployment (Production)

| Table | Partition Key | Sort Key | GSIs | Estimated Size |
|-------|--------------|----------|------|----------------|
| vendors | vendor_id | - | 2 | ~10 KB per vendor |
| transactions | vendor_id | timestamp | 2 | ~2 KB per transaction |
| market_prices | item_name | timestamp | 2 | ~1 KB per price record |
| marketplace_listings | listing_id | timestamp | 4 | ~5 KB per listing |

### Capacity Planning

**For 10,000 vendors**:
- Vendors table: ~100 MB
- Transactions (avg 10/day): ~7.3 GB/year
- Market prices (100 items, daily): ~36.5 MB/year
- Marketplace listings (avg 2/vendor): ~100 MB

**Total estimated storage**: ~8 GB/year

**Read/Write Capacity**:
- On-demand pricing (pay per request)
- Estimated cost: $1-5/month for 10K vendors

---

## Backup and Recovery

### Backup Strategy
- **Point-in-Time Recovery (PITR)**: Enabled on all tables
- **Retention**: 35 days
- **Daily Backups**: Automated via AWS Backup
- **Cross-Region Replication**: Planned for production

### Data Retention Policy
- **Transactions**: Retain forever (financial records)
- **Market Prices**: Retain 2 years (historical analysis)
- **Marketplace Listings**: Archive after 30 days if expired
- **Vendors**: Soft delete (mark as inactive)

---

## Security

### Encryption
- **At Rest**: AES-256 encryption enabled
- **In Transit**: TLS 1.2+ for all connections
- **Key Management**: AWS KMS managed keys

### Access Control
- **IAM Roles**: Lambda execution role with least privilege
- **Fine-Grained Access**: Item-level permissions planned
- **Audit Logging**: CloudTrail enabled for all table operations

---

## Performance Optimization

### Indexing Strategy
1. **GSI on location**: Fast location-based queries
2. **GSI on status**: Quick active listing retrieval
3. **LSI on timestamp**: Efficient date range queries
4. **GSI on trust_score**: Vendor ranking and filtering

### Caching Strategy
- **DAX (DynamoDB Accelerator)**: Planned for read-heavy operations
- **Application-level caching**: Redis for market prices
- **TTL**: 5 minutes for market prices, 1 hour for vendor profiles

### Query Optimization
- Use `ProjectionExpression` to fetch only needed attributes
- Implement pagination for large result sets
- Use batch operations for bulk reads/writes
- Leverage parallel scans for analytics

---

**Last Updated**: March 3, 2026  
**Database Version**: 1.0  
**Region**: ap-south-1 (Mumbai)  
**Environment**: Production
