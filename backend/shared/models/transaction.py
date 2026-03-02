"""
Transaction data model.
"""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclass
class Transaction:
    """
    Transaction entity representing a vendor transaction.

    Attributes:
        transaction_id: Unique transaction identifier
        vendor_id: Vendor who made the transaction
        item_name: Name of the produce item
        quantity: Quantity purchased/sold
        unit: Unit of measurement (kg, piece, etc.)
        price_per_unit: Price per unit
        total_amount: Total transaction amount
        timestamp: Transaction timestamp
        recorded_via: How transaction was recorded (voice, manual)
    """

    transaction_id: str
    vendor_id: str
    item_name: str
    quantity: float
    unit: str
    price_per_unit: float
    total_amount: float
    timestamp: datetime
    recorded_via: str = "manual"

    def to_dynamodb_item(self) -> dict:
        """
        Convert transaction to DynamoDB item format.

        Returns:
            Dict suitable for DynamoDB put_item
        """
        return {
            "transaction_id": self.transaction_id,
            "vendor_id": self.vendor_id,
            "item_name": self.item_name,
            "quantity": Decimal(str(self.quantity)),
            "unit": self.unit,
            "price_per_unit": Decimal(str(self.price_per_unit)),
            "total_amount": Decimal(str(self.total_amount)),
            "timestamp": self.timestamp.isoformat(),
            "recorded_via": self.recorded_via,
        }

    @classmethod
    def from_dynamodb_item(cls, item: dict) -> "Transaction":
        """
        Create Transaction from DynamoDB item.

        Args:
            item: DynamoDB item dict

        Returns:
            Transaction instance
        """
        return cls(
            transaction_id=item["transaction_id"],
            vendor_id=item["vendor_id"],
            item_name=item["item_name"],
            quantity=float(item["quantity"]),
            unit=item["unit"],
            price_per_unit=float(item["price_per_unit"]),
            total_amount=float(item["total_amount"]),
            timestamp=datetime.fromisoformat(item["timestamp"]),
            recorded_via=item.get("recorded_via", "manual"),
        )
