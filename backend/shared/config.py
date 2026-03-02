"""
Configuration management for Lambda functions.

Loads configuration from environment variables with validation and defaults.
"""

import os
from typing import Optional


class Config:
    """Application configuration loaded from environment variables."""

    # AWS Configuration
    AWS_REGION: str = os.getenv("AWS_REGION", "ap-south-1")
    AWS_ACCOUNT_ID: str = os.getenv("AWS_ACCOUNT_ID", "")

    # DynamoDB Tables
    DYNAMODB_VENDORS_TABLE: str = os.getenv("DYNAMODB_VENDORS_TABLE", "smart-vendors-vendors")
    DYNAMODB_TRANSACTIONS_TABLE: str = os.getenv(
        "DYNAMODB_TRANSACTIONS_TABLE", "smart-vendors-transactions"
    )
    DYNAMODB_MARKET_PRICES_TABLE: str = os.getenv(
        "DYNAMODB_MARKET_PRICES_TABLE", "smart-vendors-market-prices"
    )
    DYNAMODB_MARKETPLACE_LISTINGS_TABLE: str = os.getenv(
        "DYNAMODB_MARKETPLACE_LISTINGS_TABLE", "smart-vendors-marketplace-listings"
    )

    # S3 Buckets
    S3_AUDIO_BUCKET: str = os.getenv("S3_AUDIO_BUCKET", "smart-vendors-audio")
    S3_IMAGES_BUCKET: str = os.getenv("S3_IMAGES_BUCKET", "smart-vendors-images")
    S3_ASSETS_BUCKET: str = os.getenv("S3_ASSETS_BUCKET", "smart-vendors-assets")

    # AWS Service Configuration
    TRANSCRIBE_LANGUAGE_CODES: list[str] = ["hi-IN", "en-IN"]
    BEDROCK_MODEL_ID: str = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-v2")
    SAGEMAKER_ENDPOINT_NAME: str = os.getenv(
        "SAGEMAKER_ENDPOINT_NAME", "produce-freshness-classifier"
    )

    # Application Configuration
    DEMO_MODE: bool = os.getenv("DEMO_MODE", "false").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Trust Score Configuration
    TRUST_SCORE_TRANSACTION_POINTS: int = 10
    TRUST_SCORE_MARKETPLACE_SALE_POINTS: int = 20
    TRUST_SCORE_PRICE_REPORT_POINTS: int = 5

    # Trust Score Tiers
    TRUST_SCORE_BRONZE_MIN: int = 0
    TRUST_SCORE_SILVER_MIN: int = 100
    TRUST_SCORE_GOLD_MIN: int = 250

    @classmethod
    def validate(cls) -> None:
        """
        Validate required configuration values are set.

        Raises:
            ValueError: If required configuration is missing.
        """
        required_vars = [
            ("AWS_REGION", cls.AWS_REGION),
            ("DYNAMODB_VENDORS_TABLE", cls.DYNAMODB_VENDORS_TABLE),
            ("DYNAMODB_TRANSACTIONS_TABLE", cls.DYNAMODB_TRANSACTIONS_TABLE),
            ("S3_AUDIO_BUCKET", cls.S3_AUDIO_BUCKET),
            ("S3_IMAGES_BUCKET", cls.S3_IMAGES_BUCKET),
        ]

        missing = [name for name, value in required_vars if not value]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

    @classmethod
    def get_trust_score_tier(cls, score: int) -> str:
        """
        Get trust score tier based on score value.

        Args:
            score: Trust score value

        Returns:
            Tier name: Bronze, Silver, or Gold
        """
        if score >= cls.TRUST_SCORE_GOLD_MIN:
            return "Gold"
        elif score >= cls.TRUST_SCORE_SILVER_MIN:
            return "Silver"
        else:
            return "Bronze"


# Validate configuration on module import
Config.validate()
