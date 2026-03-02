"""
Property-based tests for market price queries.

Feature: hackathon-deliverables
Property: Market price query returns multiple mandis
Validates: Requirements 5.2
"""

import pytest
from hypothesis import given, strategies as st, settings
from hypothesis.strategies import composite
from unittest.mock import Mock, patch
from datetime import datetime

from shared.services.price_service import PriceService
from shared.models.market_price import MarketPrice


@composite
def produce_item_strategy(draw):
    """
    Generate produce item names.

    Returns:
        Produce item name
    """
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
        "peas",
    ]
    return draw(st.sampled_from(items))


@composite
def market_price_strategy(draw, item_name):
    """
    Generate market price data.

    Args:
        item_name: Name of the produce item

    Returns:
        MarketPrice object
    """
    mandis = ["Azadpur", "Ghazipur", "Okhla"]
    mandi_name = draw(st.sampled_from(mandis))
    price_per_kg = draw(st.floats(min_value=10.0, max_value=100.0))
    distance_km = draw(st.floats(min_value=0.5, max_value=20.0))

    return MarketPrice(
        price_id=f"price-{draw(st.integers(min_value=1, max_value=1000))}",
        item_name=item_name,
        mandi_name=mandi_name,
        price_per_kg=round(price_per_kg, 2),
        distance_km=round(distance_km, 2),
        timestamp=datetime.now(),
    )


@given(item_name=produce_item_strategy())
@settings(max_examples=100, deadline=30000)
def test_price_query_returns_multiple_mandis(item_name):
    """
    Property 4: For any produce item query, the price API should return
    data from at least 3 mandis with distance and price information.

    **Validates: Requirements 5.2**
    """
    # Generate mock price data for 3 mandis
    mock_prices = [
        MarketPrice(
            price_id=f"price-{i}",
            item_name=item_name,
            mandi_name=mandi,
            price_per_kg=30.0 + (i * 5),
            distance_km=2.0 + (i * 2),
            timestamp=datetime.now(),
        )
        for i, mandi in enumerate(["Azadpur", "Ghazipur", "Okhla"])
    ]

    # Mock DynamoDB client
    with patch("shared.services.price_service.DynamoDBClient") as mock_dynamodb_class:
        mock_dynamodb = Mock()
        mock_dynamodb_class.return_value = mock_dynamodb

        # Mock scan to return price data
        mock_dynamodb.scan.return_value = [p.to_dynamodb_item() for p in mock_prices]

        # Create service and query prices
        price_service = PriceService()
        prices = price_service.get_market_prices(item_name=item_name, limit=3)

        # Verify result structure
        assert prices is not None, "Price query should not return None"
        assert isinstance(prices, list), "Prices should be a list"
        assert len(prices) >= 3, f"Should return at least 3 mandis, got {len(prices)}"

        # Verify each price has required fields
        for price in prices:
            assert hasattr(price, "item_name"), "Price should have item_name"
            assert hasattr(price, "mandi_name"), "Price should have mandi_name"
            assert hasattr(price, "price_per_kg"), "Price should have price_per_kg"
            assert hasattr(price, "distance_km"), "Price should have distance_km"
            assert hasattr(price, "timestamp"), "Price should have timestamp"

            # Verify data types
            assert isinstance(price.item_name, str), "item_name should be string"
            assert isinstance(price.mandi_name, str), "mandi_name should be string"
            assert isinstance(price.price_per_kg, (int, float)), "price_per_kg should be numeric"
            assert isinstance(price.distance_km, (int, float)), "distance_km should be numeric"

            # Verify values
            assert price.item_name == item_name, "item_name should match query"
            assert price.price_per_kg > 0, "price_per_kg should be positive"
            assert price.distance_km >= 0, "distance_km should be non-negative"


@given(item_name=produce_item_strategy(), limit=st.integers(min_value=1, max_value=10))
@settings(max_examples=50, deadline=30000)
def test_price_query_respects_limit(item_name, limit):
    """
    Property: Price query should respect the limit parameter.

    **Validates: Requirements 5.2**
    """
    # Generate more mock prices than the limit
    all_mock_prices = [
        MarketPrice(
            price_id=f"price-{i}",
            item_name=item_name,
            mandi_name=f"Mandi-{i}",
            price_per_kg=30.0 + (i * 5),
            distance_km=2.0 + (i * 2),
            timestamp=datetime.now(),
        )
        for i in range(10)
    ]

    # Mock DynamoDB client
    with patch("shared.services.price_service.DynamoDBClient") as mock_dynamodb_class:
        mock_dynamodb = Mock()
        mock_dynamodb_class.return_value = mock_dynamodb

        # Mock scan to respect limit parameter
        def mock_scan(table_name, limit=None):
            prices_to_return = all_mock_prices[:limit] if limit else all_mock_prices
            return [p.to_dynamodb_item() for p in prices_to_return]

        mock_dynamodb.scan.side_effect = mock_scan

        # Create service and query prices
        price_service = PriceService()
        prices = price_service.get_market_prices(item_name=item_name, limit=limit)

        # Verify limit is respected
        assert len(prices) <= limit, f"Should return at most {limit} prices, got {len(prices)}"


@given(item_name=produce_item_strategy())
@settings(max_examples=50, deadline=30000)
def test_price_query_handles_no_data(item_name):
    """
    Property: Price query should handle gracefully when no data is available.

    **Validates: Requirements 5.2**
    """
    # Mock DynamoDB client to return empty data
    with patch("shared.services.price_service.DynamoDBClient") as mock_dynamodb_class:
        mock_dynamodb = Mock()
        mock_dynamodb_class.return_value = mock_dynamodb
        mock_dynamodb.scan.return_value = []

        # Create service and query prices
        price_service = PriceService()
        prices = price_service.get_market_prices(item_name=item_name, limit=3)

        # Should return empty list, not None or crash
        assert prices is not None, "Should return empty list, not None"
        assert isinstance(prices, list), "Should return a list"
        assert len(prices) == 0, "Should return empty list when no data"


def test_price_query_example():
    """
    Example test: Verify specific price query works correctly.

    **Validates: Requirements 5.2**
    """
    # Mock price data
    mock_prices = [
        MarketPrice(
            price_id="price-1",
            item_name="tomatoes",
            mandi_name="Azadpur",
            price_per_kg=35.0,
            distance_km=5.0,
            timestamp=datetime.now(),
        ),
        MarketPrice(
            price_id="price-2",
            item_name="tomatoes",
            mandi_name="Ghazipur",
            price_per_kg=32.0,
            distance_km=8.0,
            timestamp=datetime.now(),
        ),
        MarketPrice(
            price_id="price-3",
            item_name="tomatoes",
            mandi_name="Okhla",
            price_per_kg=38.0,
            distance_km=3.0,
            timestamp=datetime.now(),
        ),
    ]

    # Mock DynamoDB client
    with patch("shared.services.price_service.DynamoDBClient") as mock_dynamodb_class:
        mock_dynamodb = Mock()
        mock_dynamodb_class.return_value = mock_dynamodb
        mock_dynamodb.scan.return_value = [p.to_dynamodb_item() for p in mock_prices]

        price_service = PriceService()
        prices = price_service.get_market_prices(item_name="tomatoes", limit=3)

        assert len(prices) == 3
        assert all(p.item_name == "tomatoes" for p in prices)
        assert all(p.price_per_kg > 0 for p in prices)
