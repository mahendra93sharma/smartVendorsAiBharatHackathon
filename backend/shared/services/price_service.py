"""
Price service for market price intelligence.
"""

import logging
from typing import List, Optional

from ..aws.dynamodb_client import DynamoDBClient
from ..models.market_price import MarketPrice
from ..config import Config

logger = logging.getLogger(__name__)


class PriceService:
    """
    Service for market price intelligence.

    Handles price queries and comparisons across mandis.
    """

    def __init__(self):
        """Initialize price service with DynamoDB client."""
        self.dynamodb_client = DynamoDBClient()

    def get_market_prices(self, item_name: str, limit: int = 3) -> List[MarketPrice]:
        """
        Get market prices for an item from multiple mandis.

        Args:
            item_name: Name of the produce item
            limit: Maximum number of prices to return

        Returns:
            List of MarketPrice objects sorted by distance
        """
        try:
            # Query DynamoDB for prices
            items = self.dynamodb_client.scan(
                table_name=Config.DYNAMODB_MARKET_PRICES_TABLE, limit=limit
            )

            # Convert to MarketPrice objects
            prices = [MarketPrice.from_dynamodb_item(item) for item in items]

            # Sort by distance
            prices.sort(key=lambda p: p.distance_km)

            return prices
        except Exception as e:
            logger.error(f"Error getting market prices: {e}")
            return []
