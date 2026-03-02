"""
Lambda function for retrieving vendor transactions.

Handles GET /transactions/{vendor_id} endpoint.
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

from shared.aws.dynamodb_client import DynamoDBClient
from shared.config import Config


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda handler for retrieving vendor transactions.

    Queries DynamoDB for all transactions for a given vendor.

    Args:
        event: API Gateway event
        context: Lambda context

    Returns:
        API Gateway response
    """
    try:
        logger.info("Processing get transactions request")

        # Get vendor_id from path parameters
        path_params = event.get("pathParameters", {})
        vendor_id = path_params.get("vendor_id")

        if not vendor_id:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Missing vendor_id parameter"}),
            }

        # Get query parameters for pagination
        query_params = event.get("queryStringParameters") or {}
        limit = int(query_params.get("limit", "20"))

        # Query transactions from DynamoDB
        dynamodb_client = DynamoDBClient()
        transactions = dynamodb_client.query_transactions_by_vendor(
            vendor_id=vendor_id, limit=limit
        )

        # Convert to response format
        transactions_data = [
            {
                "transaction_id": t["transaction_id"],
                "vendor_id": t["vendor_id"],
                "item_name": t["item_name"],
                "quantity": t["quantity"],
                "unit": t["unit"],
                "price_per_unit": t["price_per_unit"],
                "total_amount": t["total_amount"],
                "timestamp": t["timestamp"],
                "recorded_via": t.get("recorded_via", "voice"),
            }
            for t in transactions
        ]

        logger.info(f"Found {len(transactions_data)} transactions for vendor {vendor_id}")

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(
                {
                    "vendor_id": vendor_id,
                    "transactions": transactions_data,
                    "count": len(transactions_data),
                }
            ),
        }

    except Exception as e:
        logger.error(f"Error in get transactions handler: {e}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Internal server error"}),
        }
