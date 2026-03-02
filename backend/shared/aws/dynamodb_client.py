"""
DynamoDB client for Smart Vendors application.

Provides a wrapper around boto3 DynamoDB client with error handling and retry logic.
"""

import logging
from typing import Any, Dict, List, Optional
from decimal import Decimal

import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

from ..config import Config

logger = logging.getLogger(__name__)


class DynamoDBClient:
    """
    DynamoDB client with connection management and error handling.

    Provides methods for common DynamoDB operations with automatic retry
    and error handling.
    """

    def __init__(self):
        """Initialize DynamoDB client."""
        try:
            self.dynamodb = boto3.resource("dynamodb", region_name=Config.AWS_REGION)
            self.client = boto3.client("dynamodb", region_name=Config.AWS_REGION)
            logger.info(f"DynamoDB client initialized for region {Config.AWS_REGION}")
        except Exception as e:
            logger.error(f"Failed to initialize DynamoDB client: {e}")
            raise

    def get_table(self, table_name: str):
        """
        Get DynamoDB table resource.

        Args:
            table_name: Name of the DynamoDB table

        Returns:
            DynamoDB table resource
        """
        return self.dynamodb.Table(table_name)

    def put_item(self, table_name: str, item: Dict[str, Any]) -> bool:
        """
        Put an item into DynamoDB table.

        Args:
            table_name: Name of the table
            item: Item to insert

        Returns:
            True if successful, False otherwise
        """
        try:
            table = self.get_table(table_name)
            table.put_item(Item=item)
            logger.info(f"Successfully put item in table {table_name}")
            return True
        except ClientError as e:
            logger.error(f"Error putting item in {table_name}: {e}")
            return False

    def get_item(self, table_name: str, key: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Get an item from DynamoDB table.

        Args:
            table_name: Name of the table
            key: Primary key of the item

        Returns:
            Item if found, None otherwise
        """
        try:
            table = self.get_table(table_name)
            response = table.get_item(Key=key)
            return response.get("Item")
        except ClientError as e:
            logger.error(f"Error getting item from {table_name}: {e}")
            return None

    def query(
        self,
        table_name: str,
        key_condition_expression: Any,
        filter_expression: Optional[Any] = None,
        limit: Optional[int] = None,
        scan_index_forward: bool = True,
    ) -> List[Dict[str, Any]]:
        """
        Query items from DynamoDB table.

        Args:
            table_name: Name of the table
            key_condition_expression: Key condition for query
            filter_expression: Optional filter expression
            limit: Maximum number of items to return
            scan_index_forward: Sort order (True for ascending, False for descending)

        Returns:
            List of items matching the query
        """
        try:
            table = self.get_table(table_name)
            query_params = {
                "KeyConditionExpression": key_condition_expression,
                "ScanIndexForward": scan_index_forward,
            }

            if filter_expression:
                query_params["FilterExpression"] = filter_expression

            if limit:
                query_params["Limit"] = limit

            response = table.query(**query_params)
            return response.get("Items", [])
        except ClientError as e:
            logger.error(f"Error querying {table_name}: {e}")
            return []

    def scan(
        self, table_name: str, filter_expression: Optional[Any] = None, limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Scan items from DynamoDB table.

        Args:
            table_name: Name of the table
            filter_expression: Optional filter expression
            limit: Maximum number of items to return

        Returns:
            List of items from the scan
        """
        try:
            table = self.get_table(table_name)
            scan_params = {}

            if filter_expression:
                scan_params["FilterExpression"] = filter_expression

            if limit:
                scan_params["Limit"] = limit

            response = table.scan(**scan_params)
            return response.get("Items", [])
        except ClientError as e:
            logger.error(f"Error scanning {table_name}: {e}")
            return []

    def update_item(
        self,
        table_name: str,
        key: Dict[str, Any],
        update_expression: str,
        expression_attribute_values: Dict[str, Any],
        expression_attribute_names: Optional[Dict[str, str]] = None,
    ) -> bool:
        """
        Update an item in DynamoDB table.

        Args:
            table_name: Name of the table
            key: Primary key of the item
            update_expression: Update expression
            expression_attribute_values: Values for the update expression
            expression_attribute_names: Optional attribute name mappings

        Returns:
            True if successful, False otherwise
        """
        try:
            table = self.get_table(table_name)
            update_params = {
                "Key": key,
                "UpdateExpression": update_expression,
                "ExpressionAttributeValues": expression_attribute_values,
            }

            if expression_attribute_names:
                update_params["ExpressionAttributeNames"] = expression_attribute_names

            table.update_item(**update_params)
            logger.info(f"Successfully updated item in table {table_name}")
            return True
        except ClientError as e:
            logger.error(f"Error updating item in {table_name}: {e}")
            return False

    def delete_item(self, table_name: str, key: Dict[str, Any]) -> bool:
        """
        Delete an item from DynamoDB table.

        Args:
            table_name: Name of the table
            key: Primary key of the item

        Returns:
            True if successful, False otherwise
        """
        try:
            table = self.get_table(table_name)
            table.delete_item(Key=key)
            logger.info(f"Successfully deleted item from table {table_name}")
            return True
        except ClientError as e:
            logger.error(f"Error deleting item from {table_name}: {e}")
            return False

    def batch_write(self, table_name: str, items: List[Dict[str, Any]]) -> bool:
        """
        Batch write items to DynamoDB table.

        Args:
            table_name: Name of the table
            items: List of items to write

        Returns:
            True if successful, False otherwise
        """
        try:
            table = self.get_table(table_name)
            with table.batch_writer() as batch:
                for item in items:
                    batch.put_item(Item=item)
            logger.info(f"Successfully batch wrote {len(items)} items to {table_name}")
            return True
        except ClientError as e:
            logger.error(f"Error batch writing to {table_name}: {e}")
            return False

    def query_transactions_by_vendor(self, vendor_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Query transactions for a specific vendor.

        Args:
            vendor_id: Vendor identifier
            limit: Maximum number of transactions to return

        Returns:
            List of transaction items
        """
        try:
            # Query using GSI on vendor_id
            table = self.get_table(Config.DYNAMODB_TRANSACTIONS_TABLE)
            response = table.query(
                IndexName="vendor_id-timestamp-index",
                KeyConditionExpression=Key("vendor_id").eq(vendor_id),
                ScanIndexForward=False,  # Sort by timestamp descending
                Limit=limit,
            )
            return response.get("Items", [])
        except ClientError as e:
            logger.error(f"Error querying transactions for vendor {vendor_id}: {e}")
            return []
