"""
Lambda function for produce freshness classification.

Handles POST /freshness/classify endpoint.
"""

import json
import logging
import base64
from typing import Dict, Any

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Import shared modules
import sys

sys.path.append("/opt/python")  # Lambda layer path

from shared.services.freshness_service import FreshnessService


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda handler for freshness classification.

    Accepts produce image, classifies using SageMaker.

    Args:
        event: API Gateway event
        context: Lambda context

    Returns:
        API Gateway response
    """
    try:
        logger.info("Processing freshness classification request")

        # Parse request body
        body = json.loads(event.get("body", "{}"))

        # Get image data (base64 encoded)
        image_base64 = body.get("image")
        vendor_id = body.get("vendor_id")

        # Validate inputs
        if not image_base64:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Missing image data"}),
            }

        if not vendor_id:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Missing vendor_id"}),
            }

        # Decode image
        image_bytes = base64.b64decode(image_base64)

        # Classify produce
        freshness_service = FreshnessService()
        result = freshness_service.classify_produce(image_bytes=image_bytes, vendor_id=vendor_id)

        if not result:
            return {
                "statusCode": 500,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Failed to classify produce"}),
            }

        logger.info(f"Successfully classified produce: {result['category']}")

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(
                {
                    "category": result["category"],
                    "confidence": result["confidence"],
                    "shelf_life_hours": result.get("shelf_life_hours"),
                    "suggestions": result.get("suggestions", []),
                }
            ),
        }

    except Exception as e:
        logger.error(f"Error in freshness classification handler: {e}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Internal server error"}),
        }
