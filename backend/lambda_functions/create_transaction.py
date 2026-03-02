"""
Lambda function for creating transactions.

Handles POST /transactions endpoint.
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

from shared.services.voice_service import VoiceService


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda handler for creating transactions from transcribed text.

    Extracts transaction details using Bedrock and stores in DynamoDB.

    Args:
        event: API Gateway event
        context: Lambda context

    Returns:
        API Gateway response
    """
    try:
        logger.info("Processing transaction creation request")

        # Parse request body
        body = json.loads(event.get("body", "{}"))

        # Get transaction data
        text = body.get("text")
        vendor_id = body.get("vendor_id")
        language_code = body.get("language_code", "en-IN")

        # Validate inputs
        if not text:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Missing text parameter"}),
            }

        if not vendor_id:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Missing vendor_id parameter"}),
            }

        # Extract and create transaction
        voice_service = VoiceService()
        result = voice_service.extract_and_store_transaction(
            text=text, vendor_id=vendor_id, language_code=language_code
        )

        if not result:
            return {
                "statusCode": 500,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Failed to create transaction"}),
            }

        logger.info(f"Successfully created transaction: {result['transaction_id']}")

        return {
            "statusCode": 201,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(
                {
                    "transaction_id": result["transaction_id"],
                    "vendor_id": result["vendor_id"],
                    "item_name": result["item_name"],
                    "quantity": result["quantity"],
                    "unit": result["unit"],
                    "price_per_unit": result["price_per_unit"],
                    "total_amount": result["total_amount"],
                    "extracted_successfully": result["extracted_successfully"],
                }
            ),
        }

    except Exception as e:
        logger.error(f"Error in transaction creation handler: {e}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Internal server error"}),
        }
