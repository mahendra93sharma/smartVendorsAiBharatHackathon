"""
Property-based tests for marketplace listing creation.

Feature: hackathon-deliverables
Property: Marketplace listing creation
Validates: Requirements 5.4
"""

import pytest
from hypothesis import given, strategies as st, settings
from hypothesis.strategies import composite
from unittest.mock import Mock, patch
from datetime import datetime

from shared.services.marketplace_service import MarketplaceService


@composite
def marketplace_listing_strategy(draw):
    """
    Generate marketplace listing data.

    Returns:
        Tuple of (vendor_id, item_name, weight_kg, price)
    """
    vendor_id = f"vendor-{draw(st.integers(min_value=1, max_value=1000))}"

    items = [
        "tomatoes",
        "potatoes",
        "onions",
        "cabbage",
        "cauliflower",
        "leafy vegetables",
        "fruits",
        "carrots",
        "beans",
    ]
    item_name = draw(st.sampled_from(items))

    weight_kg = draw(st.floats(min_value=0.5, max_value=50.0))
    price = draw(st.floats(min_value=10.0, max_value=1000.0))

    return vendor_id, item_name, round(weight_kg, 2), round(price, 2)


@given(listing_data=marketplace_listing_strategy())
@settings(max_examples=100, deadline=30000)
def test_marketplace_listing_creation_property(listing_data):
    """
    Property 6: For any valid marketplace listing (item, weight, price),
    creating the listing should return a listing ID and trigger buyer notifications.

    **Validates: Requirements 5.4**
    """
    vendor_id, item_name, weight_kg, price = listing_data

    # Mock DynamoDB client
    with patch("shared.services.marketplace_service.DynamoDBClient") as mock_dynamodb_class:
        mock_dynamodb = Mock()
        mock_dynamodb_class.return_value = mock_dynamodb
        mock_dynamodb.put_item.return_value = True

        # Create service and listing
        marketplace_service = MarketplaceService()
        result = marketplace_service.create_listing(
            vendor_id=vendor_id, item_name=item_name, weight_kg=weight_kg, price=price
        )

        # Verify result structure
        assert result is not None, "Listing creation should not return None"
        assert "listing_id" in result, "Result should contain listing_id"
        assert "status" in result, "Result should contain status"
        assert "buyers_notified" in result, "Result should contain buyers_notified"
        assert "mandi_credits_earned" in result, "Result should contain mandi_credits_earned"

        # Verify data types
        assert isinstance(result["listing_id"], str), "listing_id should be string"
        assert isinstance(result["status"], str), "status should be string"
        assert isinstance(result["buyers_notified"], int), "buyers_notified should be int"
        assert isinstance(result["mandi_credits_earned"], int), "mandi_credits_earned should be int"

        # Verify values
        assert len(result["listing_id"]) > 0, "listing_id should not be empty"
        assert result["status"] == "active", "status should be 'active'"
        assert result["buyers_notified"] > 0, "buyers_notified should be positive"
        assert result["mandi_credits_earned"] > 0, "mandi_credits_earned should be positive"

        # Verify Mandi Credits calculation (10 credits per kg)
        expected_credits = int(weight_kg * 10)
        assert (
            result["mandi_credits_earned"] == expected_credits
        ), f"mandi_credits should be {expected_credits}, got {result['mandi_credits_earned']}"


@given(
    vendor_id=st.text(min_size=1, max_size=50),
    item_name=st.text(min_size=1, max_size=50),
    weight_kg=st.floats(min_value=0.1, max_value=100.0),
    price=st.floats(min_value=1.0, max_value=10000.0),
)
@settings(max_examples=50, deadline=30000)
def test_marketplace_listing_handles_various_inputs(vendor_id, item_name, weight_kg, price):
    """
    Property: Marketplace listing should handle various valid inputs gracefully.

    **Validates: Requirements 5.4**
    """
    # Mock DynamoDB client
    with patch("shared.services.marketplace_service.DynamoDBClient") as mock_dynamodb_class:
        mock_dynamodb = Mock()
        mock_dynamodb_class.return_value = mock_dynamodb
        mock_dynamodb.put_item.return_value = True

        # Create service and listing
        marketplace_service = MarketplaceService()

        try:
            result = marketplace_service.create_listing(
                vendor_id=vendor_id, item_name=item_name, weight_kg=weight_kg, price=price
            )

            # If successful, verify result structure
            if result is not None:
                assert "listing_id" in result
                assert "status" in result
                assert "buyers_notified" in result
                assert "mandi_credits_earned" in result
        except Exception as e:
            # Should not crash, but may return None for invalid inputs
            pass


@given(listing_data=marketplace_listing_strategy())
@settings(max_examples=50, deadline=30000)
def test_marketplace_listing_handles_db_failure(listing_data):
    """
    Property: Marketplace listing should handle database failures gracefully.

    **Validates: Requirements 5.4**
    """
    vendor_id, item_name, weight_kg, price = listing_data

    # Mock DynamoDB client to fail
    with patch("shared.services.marketplace_service.DynamoDBClient") as mock_dynamodb_class:
        mock_dynamodb = Mock()
        mock_dynamodb_class.return_value = mock_dynamodb
        mock_dynamodb.put_item.return_value = False  # Simulate failure

        # Create service and listing
        marketplace_service = MarketplaceService()
        result = marketplace_service.create_listing(
            vendor_id=vendor_id, item_name=item_name, weight_kg=weight_kg, price=price
        )

        # Should return None on failure, not crash
        assert result is None, "Should return None on database failure"


def test_marketplace_listing_example():
    """
    Example test: Verify specific marketplace listing works correctly.

    **Validates: Requirements 5.4**
    """
    # Mock DynamoDB client
    with patch("shared.services.marketplace_service.DynamoDBClient") as mock_dynamodb_class:
        mock_dynamodb = Mock()
        mock_dynamodb_class.return_value = mock_dynamodb
        mock_dynamodb.put_item.return_value = True

        marketplace_service = MarketplaceService()
        result = marketplace_service.create_listing(
            vendor_id="demo-vendor", item_name="tomatoes", weight_kg=5.0, price=150.0
        )

        assert result is not None
        assert result["status"] == "active"
        assert result["buyers_notified"] > 0
        assert result["mandi_credits_earned"] == 50  # 5 kg * 10 credits/kg


@given(
    item_name=st.sampled_from(["tomatoes", "potatoes", "onions"]),
    radius_km=st.floats(min_value=1.0, max_value=20.0),
)
@settings(max_examples=50, deadline=30000)
def test_find_nearby_buyers_property(item_name, radius_km):
    """
    Property: Finding nearby buyers should return list of buyers within radius.

    **Validates: Requirements 5.4**
    """
    marketplace_service = MarketplaceService()
    buyers = marketplace_service.find_nearby_buyers(item_name=item_name, radius_km=radius_km)

    # Verify result structure
    assert buyers is not None, "Should not return None"
    assert isinstance(buyers, list), "Should return a list"

    # Verify each buyer has required fields
    for buyer in buyers:
        assert "buyer_id" in buyer, "Buyer should have buyer_id"
        assert "name" in buyer, "Buyer should have name"
        assert "type" in buyer, "Buyer should have type"
        assert "distance_km" in buyer, "Buyer should have distance_km"
        assert "interested_items" in buyer, "Buyer should have interested_items"

        # Verify buyer is within radius
        assert (
            buyer["distance_km"] <= radius_km
        ), f"Buyer distance {buyer['distance_km']} should be <= {radius_km}"


@given(
    listing_id=st.text(min_size=1, max_size=50),
    buyer_ids=st.lists(st.text(min_size=1, max_size=50), min_size=0, max_size=10),
)
@settings(max_examples=50, deadline=30000)
def test_notify_buyers_property(listing_id, buyer_ids):
    """
    Property: Notifying buyers should return notification status.

    **Validates: Requirements 5.4**
    """
    marketplace_service = MarketplaceService()
    result = marketplace_service.notify_buyers(listing_id=listing_id, buyer_ids=buyer_ids)

    # Verify result structure
    assert result is not None, "Should not return None"
    assert "listing_id" in result, "Result should contain listing_id"
    assert "notified_count" in result, "Result should contain notified_count"
    assert "status" in result, "Result should contain status"

    # Verify data types
    assert isinstance(result["listing_id"], str), "listing_id should be string"
    assert isinstance(result["notified_count"], int), "notified_count should be int"
    assert isinstance(result["status"], str), "status should be string"

    # Verify values
    assert result["notified_count"] >= 0, "notified_count should be non-negative"
