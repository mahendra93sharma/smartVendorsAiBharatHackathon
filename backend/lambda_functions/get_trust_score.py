"""
Lambda function for trust score queries.

Handles GET /trust-score/{vendor_id} endpoint.
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

from shared.services.trust_score_service import TrustScoreService


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda handler for trust score queries.

    Returns vendor's trust score and tier information.

    Args:
        event: API Gateway event
        context: Lambda context

    Returns:
        API Gateway response
    """
    try:
        logger.info("Processing trust score query")

        # Get vendor_id from path parameters
        path_params = event.get("pathParameters", {})
        vendor_id = path_params.get("vendor_id")

        if not vendor_id:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Missing vendor_id parameter"}),
            }

        # Get trust score
        trust_score_service = TrustScoreService()
        result = trust_score_service.get_vendor_trust_score(vendor_id)

        if not result:
            return {
                "statusCode": 404,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Vendor not found"}),
            }

        logger.info(f"Retrieved trust score for vendor {vendor_id}")

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(result),
        }

    except Exception as e:
        logger.error(f"Error in trust score handler: {e}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Internal server error"}),
        }
