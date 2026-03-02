"""
Lambda function for creating marketplace listings.

Handles POST /marketplace/listings endpoint.
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
    Lambda handler for creating marketplace listings.

    Creates B-Grade produce listing and notifies buyers.

    Args:
        event: API Gateway event
        context: Lambda context

    Returns:
        API Gateway response
    """
    try:
        logger.info("Processing marketplace listing creation")

        # Parse request body
        body = json.loads(event.get("body", "{}"))

        # Get listing data
        vendor_id = body.get("vendor_id")
        item_name = body.get("item_name")
        weight_kg = body.get("weight_kg")
        price = body.get("price")

        # Validate inputs
        if not all([vendor_id, item_name, weight_kg, price]):
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Missing required fields"}),
            }

        # Create listing
        marketplace_service = MarketplaceService()
        result = marketplace_service.create_listing(
            vendor_id=vendor_id, item_name=item_name, weight_kg=float(weight_kg), price=float(price)
        )

        if not result:
            return {
                "statusCode": 500,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Failed to create listing"}),
            }

        logger.info(f"Successfully created listing: {result['listing_id']}")

        return {
            "statusCode": 201,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(
                {
                    "listing_id": result["listing_id"],
                    "status": result["status"],
                    "buyers_notified": result["buyers_notified"],
                    "mandi_credits_earned": result["mandi_credits_earned"],
                }
            ),
        }

    except Exception as e:
        logger.error(f"Error in marketplace listing handler: {e}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Internal server error"}),
        }
