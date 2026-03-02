"""
Lambda function for notifying marketplace buyers.

Handles POST /marketplace/notify endpoint.
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
    Lambda handler for notifying buyers about new listings.

    Simulates buyer notifications using SNS.

    Args:
        event: API Gateway event
        context: Lambda context

    Returns:
        API Gateway response
    """
    try:
        logger.info("Processing marketplace buyer notification request")

        # Parse request body
        body = json.loads(event.get("body", "{}"))

        # Get notification data
        listing_id = body.get("listing_id")
        buyer_ids = body.get("buyer_ids", [])

        # Validate inputs
        if not listing_id:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Missing listing_id parameter"}),
            }

        # Notify buyers
        marketplace_service = MarketplaceService()
        result = marketplace_service.notify_buyers(listing_id=listing_id, buyer_ids=buyer_ids)

        logger.info(f"Notified {result['notified_count']} buyers for listing {listing_id}")

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(
                {
                    "listing_id": listing_id,
                    "notified_count": result["notified_count"],
                    "status": result["status"],
                }
            ),
        }

    except Exception as e:
        logger.error(f"Error in marketplace notification handler: {e}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Internal server error"}),
        }
