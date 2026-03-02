"""
Freshness service for produce classification.
"""

import logging
from typing import Optional, Dict, Any
from uuid import uuid4

from ..aws.sagemaker_client import SageMakerClient
from ..aws.s3_client import S3Client
from ..config import Config

logger = logging.getLogger(__name__)


class FreshnessService:
    """
    Service for produce freshness assessment.

    Handles image upload and classification using SageMaker.
    """

    def __init__(self):
        """Initialize freshness service with AWS clients."""
        self.sagemaker_client = SageMakerClient()
        self.s3_client = S3Client()

    def classify_produce(self, image_bytes: bytes, vendor_id: str) -> Optional[Dict[str, Any]]:
        """
        Classify produce freshness from image.

        Args:
            image_bytes: Image file content
            vendor_id: Vendor identifier

        Returns:
            Classification result with category, confidence, suggestions
        """
        try:
            # Upload image to S3
            image_key = f"images/{vendor_id}/{uuid4()}.jpg"
            s3_uri = self.s3_client.upload_file(
                file_bytes=image_bytes,
                bucket=Config.S3_IMAGES_BUCKET,
                key=image_key,
                content_type="image/jpeg",
            )

            if not s3_uri:
                logger.error("Failed to upload image to S3")
                return None

            # Classify using SageMaker
            classification = self.sagemaker_client.classify_produce_freshness(s3_uri)

            if not classification:
                logger.error("Failed to classify produce")
                return None

            classification["image_s3_uri"] = s3_uri
            return classification
        except Exception as e:
            logger.error(f"Error classifying produce: {e}")
            return None
