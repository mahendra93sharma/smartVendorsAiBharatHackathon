"""
Market price data model.
"""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class MarketPrice:
    """
    Market price entity representing produce prices at mandis.

    Attributes:
        price_id: Unique price record identifier
        item_name: Name of the produce item
        mandi_name: Name of the mandi (market)
        price_per_kg: Price per kilogram
        distance_km: Distance from reference point
        timestamp: Price record timestamp
    """

    price_id: str
    item_name: str
    mandi_name: str
    price_per_kg: float
    distance_km: float
    timestamp: datetime

    def to_dynamodb_item(self) -> dict:
        """
        Convert market price to DynamoDB item format.

        Returns:
            Dict suitable for DynamoDB put_item
        """
        return {
            "price_id": self.price_id,
            "item_name": self.item_name,
            "mandi_name": self.mandi_name,
            "price_per_kg": Decimal(str(self.price_per_kg)),
            "distance_km": Decimal(str(self.distance_km)),
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_dynamodb_item(cls, item: dict) -> "MarketPrice":
        """
        Create MarketPrice from DynamoDB item.

        Args:
            item: DynamoDB item dict

        Returns:
            MarketPrice instance
        """
        return cls(
            price_id=item["price_id"],
            item_name=item["item_name"],
            mandi_name=item["mandi_name"],
            price_per_kg=float(item["price_per_kg"]),
            distance_km=float(item["distance_km"]),
            timestamp=datetime.fromisoformat(item["timestamp"]),
        )
