"""
Marketplace listing data model.
"""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclass
class MarketplaceListing:
    """
    Marketplace listing entity for B-Grade produce.

    Attributes:
        listing_id: Unique listing identifier
        vendor_id: Vendor who created the listing
        item_name: Name of the produce item
        weight_kg: Weight in kilograms
        condition: Condition of produce (B-Grade)
        price: Listing price
        status: Listing status (active, sold, expired)
        created_at: Listing creation timestamp
    """

    listing_id: str
    vendor_id: str
    item_name: str
    weight_kg: float
    condition: str
    price: float
    status: str = "active"
    created_at: Optional[datetime] = None

    def to_dynamodb_item(self) -> dict:
        """
        Convert marketplace listing to DynamoDB item format.

        Returns:
            Dict suitable for DynamoDB put_item
        """
        item = {
            "listing_id": self.listing_id,
            "vendor_id": self.vendor_id,
            "item_name": self.item_name,
            "weight_kg": Decimal(str(self.weight_kg)),
            "condition": self.condition,
            "price": Decimal(str(self.price)),
            "status": self.status,
        }

        if self.created_at:
            item["created_at"] = self.created_at.isoformat()

        return item

    @classmethod
    def from_dynamodb_item(cls, item: dict) -> "MarketplaceListing":
        """
        Create MarketplaceListing from DynamoDB item.

        Args:
            item: DynamoDB item dict

        Returns:
            MarketplaceListing instance
        """
        created_at = None
        if "created_at" in item:
            created_at = datetime.fromisoformat(item["created_at"])

        return cls(
            listing_id=item["listing_id"],
            vendor_id=item["vendor_id"],
            item_name=item["item_name"],
            weight_kg=float(item["weight_kg"]),
            condition=item["condition"],
            price=float(item["price"]),
            status=item.get("status", "active"),
            created_at=created_at,
        )
