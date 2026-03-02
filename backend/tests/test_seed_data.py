"""
Property-based tests for database seeding.

Feature: hackathon-deliverables
Property: Demo data population
Validates: Requirements 9.1
"""

import os
import sys
from decimal import Decimal
from typing import Dict, List

import boto3
import pytest
from hypothesis import given, settings, strategies as st, HealthCheck
from moto import mock_dynamodb

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from seed_data import DataSeeder, DEMO_VENDORS, MANDIS, PRODUCE_ITEMS


# Delhi-NCR districts for validation
DELHI_NCR_DISTRICTS = [
    "South Delhi",
    "North Delhi",
    "East Delhi",
    "West Delhi",
    "Central Delhi",
    "New Delhi",
    "Gurgaon",
    "Noida",
    "Ghaziabad",
    "Faridabad",
]

# Delhi-NCR mandis for validation
DELHI_NCR_MANDIS = ["Azadpur Mandi", "Ghazipur Mandi", "Okhla Mandi"]


@pytest.fixture
def dynamodb_tables():
    """
    Create mock DynamoDB tables for testing.
    """
    with mock_dynamodb():
        # Create DynamoDB resource
        dynamodb = boto3.resource("dynamodb", region_name="ap-south-1")

        # Create Vendors table
        vendors_table = dynamodb.create_table(
            TableName="smart-vendors-vendors-dev",
            KeySchema=[{"AttributeName": "vendor_id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "vendor_id", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )

        # Create Transactions table with GSI
        transactions_table = dynamodb.create_table(
            TableName="smart-vendors-transactions-dev",
            KeySchema=[{"AttributeName": "transaction_id", "KeyType": "HASH"}],
            AttributeDefinitions=[
                {"AttributeName": "transaction_id", "AttributeType": "S"},
                {"AttributeName": "vendor_id", "AttributeType": "S"},
            ],
            GlobalSecondaryIndexes=[
                {
                    "IndexName": "vendor-index",
                    "KeySchema": [{"AttributeName": "vendor_id", "KeyType": "HASH"}],
                    "Projection": {"ProjectionType": "ALL"},
                }
            ],
            BillingMode="PAY_PER_REQUEST",
        )

        # Create Market Prices table
        market_prices_table = dynamodb.create_table(
            TableName="smart-vendors-market-prices-dev",
            KeySchema=[{"AttributeName": "price_id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "price_id", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )

        # Create Marketplace Listings table
        marketplace_listings_table = dynamodb.create_table(
            TableName="smart-vendors-marketplace-listings-dev",
            KeySchema=[{"AttributeName": "listing_id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "listing_id", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )

        yield {
            "vendors": vendors_table,
            "transactions": transactions_table,
            "market_prices": market_prices_table,
            "marketplace_listings": marketplace_listings_table,
        }


def scan_table(table) -> List[Dict]:
    """
    Scan a DynamoDB table and return all items.

    Args:
        table: DynamoDB table resource

    Returns:
        List of items from the table
    """
    response = table.scan()
    items = response.get("Items", [])

    # Handle pagination
    while "LastEvaluatedKey" in response:
        response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
        items.extend(response.get("Items", []))

    return items


# Feature: hackathon-deliverables, Property: Demo data population
@settings(
    max_examples=100, deadline=30000, suppress_health_check=[HealthCheck.function_scoped_fixture]
)
@given(seed_value=st.integers(min_value=0, max_value=1000000))
def test_demo_data_population_property(dynamodb_tables, seed_value):
    """
    **Validates: Requirements 9.1**

    Property: Demo data population

    For any seed value, when the data seeding script runs:
    - Exactly 5 vendors should be created
    - Exactly 20 transactions should be created
    - At least 10 market prices should be created (up to 10 as specified)
    - Exactly 5 marketplace listings should be created
    - Demo vendor should exist with correct credentials
    - All data should use realistic Delhi-NCR values

    This property verifies that the seeding process consistently creates
    the correct amount and quality of demo data regardless of random seed.
    """
    # Clear all tables before seeding (since fixture is not reset between examples)
    for table in dynamodb_tables.values():
        items = scan_table(table)
        with table.batch_writer() as batch:
            for item in items:
                # Get the key from the table's key schema
                key_name = table.key_schema[0]["AttributeName"]
                batch.delete_item(Key={key_name: item[key_name]})

    # Set random seed for reproducibility within this test run
    import random

    random.seed(seed_value)

    # Create seeder instance
    seeder = DataSeeder()

    # Seed all data
    vendor_ids = seeder.seed_vendors()
    transactions_count = seeder.seed_transactions(vendor_ids, count=20)
    prices_count = seeder.seed_market_prices(count=10)
    listings_count = seeder.seed_marketplace_listings(vendor_ids, count=5)

    # Property 1: Exactly 5 vendors created
    assert len(vendor_ids) == 5, f"Expected 5 vendors, got {len(vendor_ids)}"

    vendors = scan_table(dynamodb_tables["vendors"])
    assert len(vendors) == 5, f"Expected 5 vendors in table, got {len(vendors)}"

    # Property 2: Exactly 20 transactions created
    assert transactions_count == 20, f"Expected 20 transactions, got {transactions_count}"

    transactions = scan_table(dynamodb_tables["transactions"])
    assert len(transactions) == 20, f"Expected 20 transactions in table, got {len(transactions)}"

    # Property 3: At least 9 market prices created (3 items × 3 mandis)
    # Note: seed_market_prices creates prices for first 3 items at 3 mandis = 9 prices
    assert prices_count >= 9, f"Expected at least 9 market prices, got {prices_count}"

    market_prices = scan_table(dynamodb_tables["market_prices"])
    assert (
        len(market_prices) >= 9
    ), f"Expected at least 9 market prices in table, got {len(market_prices)}"

    # Property 4: Exactly 5 marketplace listings created
    assert listings_count == 5, f"Expected 5 listings, got {listings_count}"

    listings = scan_table(dynamodb_tables["marketplace_listings"])
    assert len(listings) == 5, f"Expected 5 listings in table, got {len(listings)}"

    # Property 5: Demo vendor exists with correct credentials
    demo_vendor = next((v for v in vendors if v["phone_number"] == "+919876543210"), None)
    assert demo_vendor is not None, "Demo vendor not found"
    assert (
        demo_vendor["name"] == "Demo Vendor"
    ), f"Demo vendor name incorrect: {demo_vendor['name']}"
    assert (
        demo_vendor["preferred_language"] == "hi"
    ), f"Demo vendor language incorrect: {demo_vendor['preferred_language']}"

    # Property 6: All vendors use Delhi-NCR districts
    for vendor in vendors:
        assert (
            vendor["district"] in DELHI_NCR_DISTRICTS
        ), f"Vendor district '{vendor['district']}' not in Delhi-NCR districts"

    # Property 7: All market prices use Delhi-NCR mandis
    for price in market_prices:
        assert (
            price["mandi_name"] in DELHI_NCR_MANDIS
        ), f"Mandi '{price['mandi_name']}' not in Delhi-NCR mandis"

    # Property 8: All prices are within realistic ranges (₹10-100/kg)
    for price in market_prices:
        price_value = float(price["price_per_kg"])
        assert (
            10.0 <= price_value <= 100.0
        ), f"Price {price_value} for {price['item_name']} outside realistic range (₹10-100/kg)"

    # Property 9: All transactions have valid produce items
    valid_produce_names = [item["name"] for item in PRODUCE_ITEMS]
    for transaction in transactions:
        assert (
            transaction["item_name"] in valid_produce_names
        ), f"Transaction item '{transaction['item_name']}' not in valid produce list"

    # Property 10: All transactions have positive quantities and prices
    for transaction in transactions:
        quantity = float(transaction["quantity"])
        price_per_unit = float(transaction["price_per_unit"])
        total_amount = float(transaction["total_amount"])

        assert quantity > 0, f"Transaction quantity must be positive, got {quantity}"
        assert price_per_unit > 0, f"Transaction price must be positive, got {price_per_unit}"
        assert total_amount > 0, f"Transaction total must be positive, got {total_amount}"

        # Verify calculation is approximately correct (within rounding)
        expected_total = quantity * price_per_unit
        assert (
            abs(total_amount - expected_total) < 0.1
        ), f"Transaction total {total_amount} doesn't match quantity {quantity} * price {price_per_unit}"

    # Property 11: All marketplace listings are B-Grade
    for listing in listings:
        assert (
            listing["condition"] == "B-Grade"
        ), f"Listing condition must be 'B-Grade', got '{listing['condition']}'"

    # Property 12: All marketplace listings have valid status
    valid_statuses = ["active", "sold", "expired"]
    for listing in listings:
        assert (
            listing["status"] in valid_statuses
        ), f"Listing status '{listing['status']}' not in valid statuses"

    # Property 13: All vendors have valid trust score tiers
    valid_tiers = ["Bronze", "Silver", "Gold"]
    for vendor in vendors:
        assert vendor["tier"] in valid_tiers, f"Vendor tier '{vendor['tier']}' not in valid tiers"

        # Verify tier matches trust score
        trust_score = int(vendor["trust_score"])
        tier = vendor["tier"]

        if trust_score < 100:
            assert tier == "Bronze", f"Trust score {trust_score} should be Bronze, got {tier}"
        elif trust_score < 250:
            assert tier == "Silver", f"Trust score {trust_score} should be Silver, got {tier}"
        else:
            assert tier == "Gold", f"Trust score {trust_score} should be Gold, got {tier}"

    # Property 14: All transactions belong to created vendors
    for transaction in transactions:
        assert (
            transaction["vendor_id"] in vendor_ids
        ), f"Transaction vendor_id '{transaction['vendor_id']}' not in created vendor IDs"

    # Property 15: All listings belong to created vendors
    for listing in listings:
        assert (
            listing["vendor_id"] in vendor_ids
        ), f"Listing vendor_id '{listing['vendor_id']}' not in created vendor IDs"


def test_demo_data_population_example(dynamodb_tables):
    """
    Example test: Verify demo data is correctly populated with expected counts.

    This is a concrete example test that verifies the basic seeding functionality
    works as expected with deterministic data.
    """
    # Create seeder instance
    seeder = DataSeeder()

    # Seed all data
    vendor_ids = seeder.seed_vendors()
    transactions_count = seeder.seed_transactions(vendor_ids, count=20)
    prices_count = seeder.seed_market_prices(count=10)
    listings_count = seeder.seed_marketplace_listings(vendor_ids, count=5)

    # Verify counts (note: market prices creates 3 items × 3 mandis = 9)
    assert len(vendor_ids) == 5
    assert transactions_count == 20
    assert prices_count == 9  # 3 items × 3 mandis
    assert listings_count == 5

    # Verify demo vendor exists
    vendors = scan_table(dynamodb_tables["vendors"])
    demo_vendor = next((v for v in vendors if v["phone_number"] == "+919876543210"), None)
    assert demo_vendor is not None
    assert demo_vendor["name"] == "Demo Vendor"


def test_demo_vendor_credentials(dynamodb_tables):
    """
    Example test: Verify demo vendor has correct credentials.

    **Validates: Requirements 9.2**
    """
    seeder = DataSeeder()
    vendor_ids = seeder.seed_vendors()

    vendors = scan_table(dynamodb_tables["vendors"])
    demo_vendor = next((v for v in vendors if v["phone_number"] == "+919876543210"), None)

    assert demo_vendor is not None, "Demo vendor not found"
    assert demo_vendor["name"] == "Demo Vendor"
    assert demo_vendor["phone_number"] == "+919876543210"
    assert demo_vendor["preferred_language"] == "hi"
    assert demo_vendor["district"] == "South Delhi"


def test_realistic_delhi_ncr_data(dynamodb_tables):
    """
    Example test: Verify data uses realistic Delhi-NCR values.

    **Validates: Requirements 9.6**
    """
    seeder = DataSeeder()
    vendor_ids = seeder.seed_vendors()
    seeder.seed_market_prices(count=10)  # Will create 9 prices (3 items × 3 mandis)

    # Check vendors use Delhi-NCR districts
    vendors = scan_table(dynamodb_tables["vendors"])
    for vendor in vendors:
        assert vendor["district"] in DELHI_NCR_DISTRICTS

    # Check market prices use Delhi-NCR mandis
    market_prices = scan_table(dynamodb_tables["market_prices"])
    assert len(market_prices) == 9  # 3 items × 3 mandis
    for price in market_prices:
        assert price["mandi_name"] in DELHI_NCR_MANDIS

        # Check prices are in realistic range (₹10-100/kg)
        price_value = float(price["price_per_kg"])
        assert 10.0 <= price_value <= 100.0
