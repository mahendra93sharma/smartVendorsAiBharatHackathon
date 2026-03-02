#!/usr/bin/env python3
"""
Demo data seeding script for DynamoDB tables.

This script populates the DynamoDB tables with realistic demo data for the
Smart Vendors hackathon submission. It creates:
- 5 vendor profiles (including demo_vendor account)
- 20 transactions across vendors
- 10 market prices from Delhi-NCR mandis
- 5 marketplace listings

Usage:
    python seed_data.py

Environment Variables:
    AWS_REGION: AWS region (default: ap-south-1)
    DYNAMODB_TABLE_VENDORS: Vendors table name
    DYNAMODB_TABLE_TRANSACTIONS: Transactions table name
    DYNAMODB_TABLE_MARKET_PRICES: Market prices table name
    DYNAMODB_TABLE_MARKETPLACE_LISTINGS: Marketplace listings table name
"""

import os
import sys
import uuid
import time
from datetime import datetime, timedelta
from decimal import Decimal
from typing import List
import random

import boto3
from botocore.exceptions import ClientError

# Add shared directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "shared"))

from models import Vendor, Transaction, MarketPrice, MarketplaceListing


# Delhi-NCR mandis
MANDIS = [
    {"name": "Azadpur Mandi", "distance_km": 12.5},
    {"name": "Ghazipur Mandi", "distance_km": 18.3},
    {"name": "Okhla Mandi", "distance_km": 15.7},
]

# Common produce items with typical price ranges (₹/kg)
PRODUCE_ITEMS = [
    {"name": "tomatoes", "price_range": (20, 50)},
    {"name": "potatoes", "price_range": (15, 35)},
    {"name": "onions", "price_range": (25, 60)},
    {"name": "leafy vegetables", "price_range": (10, 30)},
    {"name": "cauliflower", "price_range": (30, 70)},
]

# Demo vendor data
DEMO_VENDORS = [
    {
        "name": "Demo Vendor",
        "phone_number": "+919876543210",
        "district": "South Delhi",
        "preferred_language": "hi",
        "trust_score": 100,
        "tier": "Silver",
    },
    {
        "name": "Rajesh Kumar",
        "phone_number": "+919876543211",
        "district": "North Delhi",
        "preferred_language": "hi",
        "trust_score": 250,
        "tier": "Gold",
    },
    {
        "name": "Priya Sharma",
        "phone_number": "+919876543212",
        "district": "East Delhi",
        "preferred_language": "en",
        "trust_score": 150,
        "tier": "Silver",
    },
    {
        "name": "Amit Singh",
        "phone_number": "+919876543213",
        "district": "West Delhi",
        "preferred_language": "hi",
        "trust_score": 50,
        "tier": "Bronze",
    },
    {
        "name": "Sunita Devi",
        "phone_number": "+919876543214",
        "district": "Central Delhi",
        "preferred_language": "hi",
        "trust_score": 180,
        "tier": "Silver",
    },
]


class DataSeeder:
    """Handles seeding of demo data into DynamoDB tables."""

    def __init__(self):
        """Initialize DynamoDB client and table names."""
        self.region = os.getenv("AWS_REGION", "ap-south-1")
        self.dynamodb = boto3.resource("dynamodb", region_name=self.region)

        # Get table names from environment
        self.vendors_table_name = os.getenv("DYNAMODB_TABLE_VENDORS", "smart-vendors-vendors-dev")
        self.transactions_table_name = os.getenv(
            "DYNAMODB_TABLE_TRANSACTIONS", "smart-vendors-transactions-dev"
        )
        self.market_prices_table_name = os.getenv(
            "DYNAMODB_TABLE_MARKET_PRICES", "smart-vendors-market-prices-dev"
        )
        self.marketplace_listings_table_name = os.getenv(
            "DYNAMODB_TABLE_MARKETPLACE_LISTINGS", "smart-vendors-marketplace-listings-dev"
        )

        # Get table references
        self.vendors_table = self.dynamodb.Table(self.vendors_table_name)
        self.transactions_table = self.dynamodb.Table(self.transactions_table_name)
        self.market_prices_table = self.dynamodb.Table(self.market_prices_table_name)
        self.marketplace_listings_table = self.dynamodb.Table(self.marketplace_listings_table_name)

        self.vendor_ids = []

    def verify_tables_exist(self) -> bool:
        """
        Verify that all required DynamoDB tables exist.

        Returns:
            True if all tables exist, False otherwise
        """
        print("Verifying DynamoDB tables...")
        tables_to_check = [
            self.vendors_table_name,
            self.transactions_table_name,
            self.market_prices_table_name,
            self.marketplace_listings_table_name,
        ]

        try:
            client = boto3.client("dynamodb", region_name=self.region)
            existing_tables = client.list_tables()["TableNames"]

            for table_name in tables_to_check:
                if table_name not in existing_tables:
                    print(f"❌ Table not found: {table_name}")
                    return False
                print(f"✓ Found table: {table_name}")

            return True
        except ClientError as e:
            print(f"❌ Error checking tables: {e}")
            return False

    def seed_vendors(self) -> List[str]:
        """
        Seed vendor data into DynamoDB using batch writes.

        Returns:
            List of created vendor IDs
        """
        print("\n📝 Seeding vendors...")
        vendor_ids = []

        # Prepare batch write items
        with self.vendors_table.batch_writer() as batch:
            for vendor_data in DEMO_VENDORS:
                vendor_id = str(uuid.uuid4())
                vendor = Vendor(
                    vendor_id=vendor_id,
                    phone_number=vendor_data["phone_number"],
                    name=vendor_data["name"],
                    preferred_language=vendor_data["preferred_language"],
                    district=vendor_data["district"],
                    trust_score=vendor_data["trust_score"],
                    tier=vendor_data["tier"],
                    created_at=datetime.utcnow(),
                )

                try:
                    batch.put_item(Item=vendor.to_dynamodb_item())
                    vendor_ids.append(vendor_id)
                    print(f"  ✓ Created vendor: {vendor.name} (ID: {vendor_id[:8]}...)")
                except ClientError as e:
                    print(f"  ❌ Error creating vendor {vendor.name}: {e}")

        print(f"✅ Created {len(vendor_ids)} vendors")
        return vendor_ids

    def seed_transactions(self, vendor_ids: List[str], count: int = 20) -> int:
        """
        Seed transaction data into DynamoDB using batch writes.

        Args:
            vendor_ids: List of vendor IDs to create transactions for
            count: Number of transactions to create

        Returns:
            Number of transactions created
        """
        print(f"\n📝 Seeding {count} transactions...")
        created_count = 0

        # Prepare batch write items
        with self.transactions_table.batch_writer() as batch:
            for i in range(count):
                vendor_id = random.choice(vendor_ids)
                produce = random.choice(PRODUCE_ITEMS)

                # Random quantity between 2-20 kg
                quantity = round(random.uniform(2.0, 20.0), 1)

                # Random price within the item's typical range
                price_per_unit = round(random.uniform(*produce["price_range"]), 2)
                total_amount = round(quantity * price_per_unit, 2)

                # Random timestamp within last 7 days
                days_ago = random.randint(0, 7)
                hours_ago = random.randint(0, 23)
                timestamp = datetime.utcnow() - timedelta(days=days_ago, hours=hours_ago)

                transaction = Transaction(
                    transaction_id=str(uuid.uuid4()),
                    vendor_id=vendor_id,
                    item_name=produce["name"],
                    quantity=quantity,
                    unit="kg",
                    price_per_unit=price_per_unit,
                    total_amount=total_amount,
                    timestamp=timestamp,
                    recorded_via=random.choice(["voice", "manual"]),
                )

                try:
                    batch.put_item(Item=transaction.to_dynamodb_item())
                    created_count += 1
                    if (i + 1) % 5 == 0:
                        print(f"  ✓ Created {i + 1}/{count} transactions...")
                except ClientError as e:
                    print(f"  ❌ Error creating transaction: {e}")

        print(f"✅ Created {created_count} transactions")
        return created_count

    def seed_market_prices(self, count: int = 10) -> int:
        """
        Seed market price data into DynamoDB using batch writes.

        Args:
            count: Number of price records to create

        Returns:
            Number of price records created
        """
        print(f"\n📝 Seeding {count} market prices...")
        created_count = 0

        # Prepare batch write items
        with self.market_prices_table.batch_writer() as batch:
            # Create prices for each produce item at each mandi
            for produce in PRODUCE_ITEMS[:3]:  # Use first 3 items
                for mandi in MANDIS:
                    # Base price with some variation
                    base_price = sum(produce["price_range"]) / 2
                    price_variation = random.uniform(-5, 5)
                    price_per_kg = round(base_price + price_variation, 2)

                    # Timestamp within last 6 hours (fresh data)
                    hours_ago = random.randint(0, 6)
                    timestamp = datetime.utcnow() - timedelta(hours=hours_ago)

                    # TTL: 24 hours from now
                    ttl = int(time.time()) + (24 * 60 * 60)

                    market_price = MarketPrice(
                        price_id=str(uuid.uuid4()),
                        item_name=produce["name"],
                        mandi_name=mandi["name"],
                        price_per_kg=price_per_kg,
                        distance_km=mandi["distance_km"],
                        timestamp=timestamp,
                    )

                    try:
                        item = market_price.to_dynamodb_item()
                        item["ttl"] = ttl  # Add TTL attribute
                        batch.put_item(Item=item)
                        created_count += 1
                        print(
                            f"  ✓ Created price: {produce['name']} at {mandi['name']} - ₹{price_per_kg}/kg"
                        )
                    except ClientError as e:
                        print(f"  ❌ Error creating market price: {e}")

                    if created_count >= count:
                        break
                if created_count >= count:
                    break

        print(f"✅ Created {created_count} market prices")
        return created_count

    def seed_marketplace_listings(self, vendor_ids: List[str], count: int = 5) -> int:
        """
        Seed marketplace listing data into DynamoDB using batch writes.

        Args:
            vendor_ids: List of vendor IDs to create listings for
            count: Number of listings to create

        Returns:
            Number of listings created
        """
        print(f"\n📝 Seeding {count} marketplace listings...")
        created_count = 0

        # Prepare batch write items
        with self.marketplace_listings_table.batch_writer() as batch:
            for i in range(count):
                vendor_id = random.choice(vendor_ids)
                produce = random.choice(PRODUCE_ITEMS)

                # B-Grade produce: 5-15 kg
                weight_kg = round(random.uniform(5.0, 15.0), 1)

                # B-Grade price: 40-60% of normal price
                normal_price = sum(produce["price_range"]) / 2
                discount_factor = random.uniform(0.4, 0.6)
                price = round(weight_kg * normal_price * discount_factor, 2)

                # Random timestamp within last 2 days
                days_ago = random.randint(0, 2)
                hours_ago = random.randint(0, 23)
                created_at = datetime.utcnow() - timedelta(days=days_ago, hours=hours_ago)

                # Random status (mostly active)
                status = random.choices(["active", "sold", "expired"], weights=[0.7, 0.2, 0.1])[0]

                listing = MarketplaceListing(
                    listing_id=str(uuid.uuid4()),
                    vendor_id=vendor_id,
                    item_name=produce["name"],
                    weight_kg=weight_kg,
                    condition="B-Grade",
                    price=price,
                    status=status,
                    created_at=created_at,
                )

                try:
                    item = listing.to_dynamodb_item()
                    # Add additional fields for marketplace
                    item["buyers_notified"] = random.randint(3, 10)
                    item["mandi_credits_earned"] = int(weight_kg * 10)  # 10 credits per kg

                    batch.put_item(Item=item)
                    created_count += 1
                    print(
                        f"  ✓ Created listing: {weight_kg}kg {produce['name']} - ₹{price} ({status})"
                    )
                except ClientError as e:
                    print(f"  ❌ Error creating marketplace listing: {e}")

        print(f"✅ Created {created_count} marketplace listings")
        return created_count

    def run(self):
        """Execute the complete data seeding process."""
        print("=" * 60)
        print("Smart Vendors - Demo Data Seeding Script")
        print("=" * 60)

        # Verify tables exist
        if not self.verify_tables_exist():
            print("\n❌ Cannot proceed: Required tables not found")
            print("Please run Terraform to create the infrastructure first:")
            print("  cd infrastructure/terraform")
            print("  terraform init")
            print("  terraform apply")
            sys.exit(1)

        # Seed data
        vendor_ids = self.seed_vendors()
        if not vendor_ids:
            print("\n❌ Failed to create vendors. Aborting.")
            sys.exit(1)

        self.seed_transactions(vendor_ids, count=20)
        self.seed_market_prices(count=10)
        self.seed_marketplace_listings(vendor_ids, count=5)

        # Summary
        print("\n" + "=" * 60)
        print("✅ Data Seeding Complete!")
        print("=" * 60)
        print(f"\nDemo Credentials:")
        print(f"  Username: demo_vendor")
        print(f"  Password: hackathon2024")
        print(f"  Phone: +919876543210")
        print(f"\nVendor IDs created:")
        for i, vid in enumerate(vendor_ids, 1):
            vendor_name = DEMO_VENDORS[i - 1]["name"]
            print(f"  {i}. {vendor_name}: {vid}")
        print("\n" + "=" * 60)


def main():
    """Main entry point."""
    # Load environment variables from .env file if it exists
    try:
        from dotenv import load_dotenv

        load_dotenv()
    except ImportError:
        print("Note: python-dotenv not installed. Using system environment variables.")

    seeder = DataSeeder()
    seeder.run()


if __name__ == "__main__":
    main()
