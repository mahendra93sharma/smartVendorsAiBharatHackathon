"""
Lambda function for market price queries.

Handles GET /prices/{item} endpoint.
"""

import json
import logging
from typing import Dict, Any

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Import shared modules
import sys

sys.path.append("/opt/python")  # Lambda layer path

from shared.services.price_service import PriceService


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda handler for market price queries.

    Returns prices from multiple mandis for a given item.

    Args:
        event: API Gateway event
        context: Lambda context

    Returns:
        API Gateway response
    """
    try:
        logger.info("Processing market price query")

        # Get item from path parameters
        path_params = event.get("pathParameters", {})
        item_name = path_params.get("item")

        if not item_name:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Missing item parameter"}),
            }

        # Get prices from service
        price_service = PriceService()
        prices = price_service.get_market_prices(item_name=item_name, limit=3)

        # Convert to response format
        prices_data = [
            {
                "item_name": p.item_name,
                "mandi_name": p.mandi_name,
                "price_per_kg": p.price_per_kg,
                "distance_km": p.distance_km,
                "timestamp": p.timestamp.isoformat(),
            }
            for p in prices
        ]

        logger.info(f"Found {len(prices)} prices for {item_name}")

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(
                {"item": item_name, "prices": prices_data, "count": len(prices_data)}
            ),
        }

    except Exception as e:
        logger.error(f"Error in market price handler: {e}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Internal server error"}),
        }
