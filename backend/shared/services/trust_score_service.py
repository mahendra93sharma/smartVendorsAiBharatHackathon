"""
Trust score service for vendor reputation management.
"""

import logging
from typing import Optional, Dict, Any

from ..aws.dynamodb_client import DynamoDBClient
from ..models.vendor import Vendor
from ..config import Config

logger = logging.getLogger(__name__)


class TrustScoreService:
    """
    Service for trust score calculation and tier management.

    Handles score updates and tier assignments.
    """

    def __init__(self):
        """Initialize trust score service with DynamoDB client."""
        self.dynamodb_client = DynamoDBClient()

    def get_vendor_trust_score(self, vendor_id: str) -> Optional[Dict[str, Any]]:
        """
        Get vendor's trust score and tier information.

        Args:
            vendor_id: Vendor identifier

        Returns:
            Dict with score, tier, and breakdown
        """
        try:
            # Get vendor from DynamoDB
            item = self.dynamodb_client.get_item(
                table_name=Config.DYNAMODB_VENDORS_TABLE, key={"vendor_id": vendor_id}
            )

            if not item:
                logger.error(f"Vendor {vendor_id} not found")
                return None

            vendor = Vendor.from_dynamodb_item(item)

            # Get tier based on score
            tier = Config.get_trust_score_tier(vendor.trust_score)

            # Calculate next tier threshold
            if tier == "Bronze":
                next_tier = "Silver"
                next_threshold = Config.TRUST_SCORE_SILVER_MIN
            elif tier == "Silver":
                next_tier = "Gold"
                next_threshold = Config.TRUST_SCORE_GOLD_MIN
            else:
                next_tier = None
                next_threshold = None

            return {
                "vendor_id": vendor_id,
                "trust_score": vendor.trust_score,
                "tier": tier,
                "next_tier": next_tier,
                "next_threshold": next_threshold,
                "points_to_next_tier": next_threshold - vendor.trust_score if next_threshold else 0,
            }
        except Exception as e:
            logger.error(f"Error getting trust score: {e}")
            return None

    def update_trust_score(self, vendor_id: str, points: int, reason: str) -> bool:
        """
        Update vendor's trust score.

        Args:
            vendor_id: Vendor identifier
            points: Points to add
            reason: Reason for score update

        Returns:
            True if successful, False otherwise
        """
        try:
            # Get current vendor
            item = self.dynamodb_client.get_item(
                table_name=Config.DYNAMODB_VENDORS_TABLE, key={"vendor_id": vendor_id}
            )

            if not item:
                logger.error(f"Vendor {vendor_id} not found")
                return False

            vendor = Vendor.from_dynamodb_item(item)
            new_score = vendor.trust_score + points
            new_tier = Config.get_trust_score_tier(new_score)

            # Update in DynamoDB
            success = self.dynamodb_client.update_item(
                table_name=Config.DYNAMODB_VENDORS_TABLE,
                key={"vendor_id": vendor_id},
                update_expression="SET trust_score = :score, tier = :tier",
                expression_attribute_values={":score": new_score, ":tier": new_tier},
            )

            if success:
                logger.info(f"Updated trust score for {vendor_id}: +{points} ({reason})")

            return success
        except Exception as e:
            logger.error(f"Error updating trust score: {e}")
            return False
