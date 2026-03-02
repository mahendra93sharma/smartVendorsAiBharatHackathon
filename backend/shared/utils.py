"""
Utility functions for Lambda functions.
"""

import json
from typing import Any, Dict
from decimal import Decimal


class DecimalEncoder(json.JSONEncoder):
    """
    JSON encoder that handles Decimal types from DynamoDB.
    """

    def default(self, obj: Any) -> Any:
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


def create_response(
    status_code: int, body: Dict[str, Any], headers: Dict[str, str] = None
) -> Dict[str, Any]:
    """
    Create API Gateway response.

    Args:
        status_code: HTTP status code
        body: Response body dict
        headers: Optional headers

    Returns:
        API Gateway response dict
    """
    default_headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS",
    }

    if headers:
        default_headers.update(headers)

    return {
        "statusCode": status_code,
        "headers": default_headers,
        "body": json.dumps(body, cls=DecimalEncoder),
    }


def parse_request_body(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse request body from API Gateway event.

    Args:
        event: API Gateway event

    Returns:
        Parsed body dict
    """
    body = event.get("body", "{}")
    if isinstance(body, str):
        return json.loads(body)
    return body
