"""
Lambda function for retrieving nearby marketplace buyers.

Handles GET /marketplace/buyers endpoint.
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

from shared.services.marketplace_service import MarketplaceService


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda handler for retrieving nearby buyers.

    Returns list of buyers interested in B-Grade produce.

    Args:
        event: API Gateway event
        context: Lambda context

    Returns:
        API Gateway response
    """
    try:
        logger.info("Processing get marketplace buyers request")

        # Get query parameters
        query_params = event.get("queryStringParameters") or {}
        item_name = query_params.get("item")
        radius_km = float(query_params.get("radius_km", "10"))

        # Validate inputs
        if not item_name:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Missing item parameter"}),
            }

        # Get buyers from service
        marketplace_service = MarketplaceService()
        buyers = marketplace_service.find_nearby_buyers(item_name=item_name, radius_km=radius_km)

        logger.info(f"Found {len(buyers)} buyers for {item_name}")

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"item": item_name, "buyers": buyers, "count": len(buyers)}),
        }

    except Exception as e:
        logger.error(f"Error in get marketplace buyers handler: {e}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Internal server error"}),
        }
