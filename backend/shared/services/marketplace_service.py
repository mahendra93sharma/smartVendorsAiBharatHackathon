"""
Marketplace service for B-Grade produce listings.
"""

import logging
from typing import List, Optional, Dict, Any
from uuid import uuid4
from datetime import datetime

from ..aws.dynamodb_client import DynamoDBClient
from ..models.marketplace_listing import MarketplaceListing
from ..config import Config

logger = logging.getLogger(__name__)


class MarketplaceService:
    """
    Service for marketplace operations.

    Handles listing creation, buyer matching, and notifications.
    """

    def __init__(self):
        """Initialize marketplace service with DynamoDB client."""
        self.dynamodb_client = DynamoDBClient()

    def create_listing(
        self, vendor_id: str, item_name: str, weight_kg: float, price: float
    ) -> Optional[Dict[str, Any]]:
        """
        Create a marketplace listing for B-Grade produce.

        Args:
            vendor_id: Vendor identifier
            item_name: Name of the produce item
            weight_kg: Weight in kilograms
            price: Listing price

        Returns:
            Dict with listing_id, status, and buyers_notified count
        """
        try:
            listing_id = str(uuid4())
            listing = MarketplaceListing(
                listing_id=listing_id,
                vendor_id=vendor_id,
                item_name=item_name,
                weight_kg=weight_kg,
                condition="B-Grade",
                price=price,
                status="active",
                created_at=datetime.now(),
            )

            # Save to DynamoDB
            success = self.dynamodb_client.put_item(
                table_name=Config.DYNAMODB_MARKETPLACE_LISTINGS_TABLE,
                item=listing.to_dynamodb_item(),
            )

            if not success:
                logger.error("Failed to save listing to DynamoDB")
                return None

            # Calculate Mandi Credits (10 credits per kg)
            mandi_credits = int(weight_kg * 10)

            # Simulate buyer notifications (mock for demo)
            buyers_notified = 5

            return {
                "listing_id": listing_id,
                "status": "active",
                "buyers_notified": buyers_notified,
                "mandi_credits_earned": mandi_credits,
            }
        except Exception as e:
            logger.error(f"Error creating marketplace listing: {e}")
            return None

    def get_vendor_listings(self, vendor_id: str) -> List[MarketplaceListing]:
        """
        Get all listings for a vendor.

        Args:
            vendor_id: Vendor identifier

        Returns:
            List of MarketplaceListing objects
        """
        try:
            items = self.dynamodb_client.scan(table_name=Config.DYNAMODB_MARKETPLACE_LISTINGS_TABLE)

            # Filter by vendor_id (in production, use GSI)
            vendor_items = [item for item in items if item.get("vendor_id") == vendor_id]

            return [MarketplaceListing.from_dynamodb_item(item) for item in vendor_items]
        except Exception as e:
            logger.error(f"Error getting vendor listings: {e}")
            return []

    def find_nearby_buyers(self, item_name: str, radius_km: float = 10.0) -> List[Dict[str, Any]]:
        """
        Find nearby buyers interested in B-Grade produce.

        Args:
            item_name: Name of the produce item
            radius_km: Search radius in kilometers

        Returns:
            List of buyer information dicts
        """
        try:
            # Mock buyer data for demo
            mock_buyers = [
                {
                    "buyer_id": "buyer-001",
                    "name": "Delhi Juice Corner",
                    "type": "juice_shop",
                    "distance_km": 2.5,
                    "interested_items": ["tomatoes", "fruits", "leafy vegetables"],
                },
                {
                    "buyer_id": "buyer-002",
                    "name": "Pickle Factory",
                    "type": "processing_unit",
                    "distance_km": 5.0,
                    "interested_items": ["tomatoes", "onions", "chillies"],
                },
                {
                    "buyer_id": "buyer-003",
                    "name": "Community Compost Center",
                    "type": "compost",
                    "distance_km": 3.0,
                    "interested_items": ["all"],
                },
                {
                    "buyer_id": "buyer-004",
                    "name": "Street Food Vendor",
                    "type": "food_vendor",
                    "distance_km": 1.5,
                    "interested_items": ["potatoes", "onions", "tomatoes"],
                },
                {
                    "buyer_id": "buyer-005",
                    "name": "Animal Feed Supplier",
                    "type": "feed_supplier",
                    "distance_km": 8.0,
                    "interested_items": ["leafy vegetables", "fruits"],
                },
            ]

            # Filter buyers by item interest and radius
            matching_buyers = []
            for buyer in mock_buyers:
                if buyer["distance_km"] <= radius_km:
                    interested = buyer["interested_items"]
                    if "all" in interested or item_name.lower() in interested:
                        matching_buyers.append(buyer)

            logger.info(f"Found {len(matching_buyers)} buyers for {item_name} within {radius_km}km")
            return matching_buyers

        except Exception as e:
            logger.error(f"Error finding nearby buyers: {e}")
            return []

    def notify_buyers(self, listing_id: str, buyer_ids: List[str]) -> Dict[str, Any]:
        """
        Notify buyers about a new listing.

        Args:
            listing_id: Listing identifier
            buyer_ids: List of buyer IDs to notify

        Returns:
            Dict with notification status
        """
        try:
            # In production, this would use SNS to send notifications
            # For demo, we simulate the notification

            notified_count = len(buyer_ids) if buyer_ids else 5

            logger.info(
                f"Simulated notification to {notified_count} buyers for listing {listing_id}"
            )

            return {
                "listing_id": listing_id,
                "notified_count": notified_count,
                "status": "notifications_sent",
            }

        except Exception as e:
            logger.error(f"Error notifying buyers: {e}")
            return {"listing_id": listing_id, "notified_count": 0, "status": "failed"}
