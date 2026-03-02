"""
Vendor data model.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class Vendor:
    """
    Vendor entity representing a street vendor.

    Attributes:
        vendor_id: Unique vendor identifier
        phone_number: Vendor's phone number
        name: Vendor's name
        preferred_language: Preferred language (hi or en)
        district: Delhi-NCR district
        trust_score: Current trust score
        tier: Trust score tier (Bronze, Silver, Gold)
        created_at: Account creation timestamp
    """

    vendor_id: str
    phone_number: str
    name: str
    preferred_language: str
    district: str
    trust_score: int = 0
    tier: str = "Bronze"
    created_at: Optional[datetime] = None

    def to_dynamodb_item(self) -> dict:
        """
        Convert vendor to DynamoDB item format.

        Returns:
            Dict suitable for DynamoDB put_item
        """
        item = {
            "vendor_id": self.vendor_id,
            "phone_number": self.phone_number,
            "name": self.name,
            "preferred_language": self.preferred_language,
            "district": self.district,
            "trust_score": self.trust_score,
            "tier": self.tier,
        }

        if self.created_at:
            item["created_at"] = self.created_at.isoformat()

        return item

    @classmethod
    def from_dynamodb_item(cls, item: dict) -> "Vendor":
        """
        Create Vendor from DynamoDB item.

        Args:
            item: DynamoDB item dict

        Returns:
            Vendor instance
        """
        created_at = None
        if "created_at" in item:
            created_at = datetime.fromisoformat(item["created_at"])

        return cls(
            vendor_id=item["vendor_id"],
            phone_number=item["phone_number"],
            name=item["name"],
            preferred_language=item["preferred_language"],
            district=item["district"],
            trust_score=int(item.get("trust_score", 0)),
            tier=item.get("tier", "Bronze"),
            created_at=created_at,
        )
