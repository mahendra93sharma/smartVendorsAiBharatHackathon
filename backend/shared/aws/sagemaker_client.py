"""
Amazon SageMaker client for ML model inference.

Handles produce freshness classification using deployed SageMaker endpoints.
"""

import logging
from typing import Optional, Dict, Any
import json
import random
import hashlib

import boto3
from botocore.exceptions import ClientError, EndpointConnectionError

from ..config import Config

logger = logging.getLogger(__name__)


class SageMakerClient:
    """
    Amazon SageMaker client for ML inference.

    Provides produce freshness classification using deployed endpoints.
    Includes fallback to mock classification for demo purposes.
    """

    def __init__(self):
        """Initialize SageMaker runtime client."""
        try:
            self.sagemaker_runtime = boto3.client(
                "sagemaker-runtime", region_name=Config.AWS_REGION
            )
            self.demo_mode = Config.DEMO_MODE
            logger.info(
                f"SageMaker client initialized for region {Config.AWS_REGION}, demo_mode={self.demo_mode}"
            )
        except Exception as e:
            logger.error(f"Failed to initialize SageMaker client: {e}")
            # Don't raise - allow fallback to demo mode
            self.sagemaker_runtime = None
            self.demo_mode = True

    def classify_produce_freshness(self, image_s3_uri: str) -> Optional[Dict[str, Any]]:
        """
        Classify produce freshness using SageMaker endpoint.

        Falls back to mock classification if endpoint is unavailable or in demo mode.

        Args:
            image_s3_uri: S3 URI of the produce image

        Returns:
            Classification result with category and confidence
        """
        # Use demo mode if enabled or if SageMaker client failed to initialize
        if self.demo_mode or self.sagemaker_runtime is None:
            logger.info("Using mock classification (demo mode)")
            return self._mock_classification(image_s3_uri)

        try:
            # Prepare input payload for SageMaker endpoint
            payload = {"image_uri": image_s3_uri}

            response = self.sagemaker_runtime.invoke_endpoint(
                EndpointName=Config.SAGEMAKER_ENDPOINT_NAME,
                ContentType="application/json",
                Body=json.dumps(payload),
            )

            result = json.loads(response["Body"].read())
            classification = self._parse_classification_result(result)

            logger.info(f"Successfully classified produce image: {classification['category']}")
            return classification
        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "")
            logger.error(f"Error invoking SageMaker endpoint: {error_code} - {e}")

            # Fallback to mock classification
            logger.info("Falling back to mock classification")
            return self._mock_classification(image_s3_uri)
        except EndpointConnectionError as e:
            logger.error(f"SageMaker endpoint connection error: {e}")
            logger.info("Falling back to mock classification")
            return self._mock_classification(image_s3_uri)
        except Exception as e:
            logger.error(f"Unexpected error during classification: {e}")
            logger.info("Falling back to mock classification")
            return self._mock_classification(image_s3_uri)

    def _parse_classification_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse SageMaker endpoint response.

        Implements confidence threshold logic:
        - >0.7: Fresh (24-48h shelf life)
        - 0.4-0.7: B-Grade (6-12h shelf life)
        - <0.4: Waste (0h shelf life)

        Args:
            result: Raw endpoint response

        Returns:
            Parsed classification with category, confidence, shelf_life
        """
        # Extract confidence from model output
        # Support multiple output formats
        if "predictions" in result:
            confidence = result["predictions"][0].get("score", 0.5)
        elif "confidence" in result:
            confidence = result["confidence"]
        elif "score" in result:
            confidence = result["score"]
        else:
            # Default to middle confidence if format is unexpected
            confidence = 0.5
            logger.warning(f"Unexpected model output format: {result}")

        # Apply confidence threshold logic as per requirements
        if confidence > 0.7:
            category = "Fresh"
            shelf_life_hours = 48
        elif confidence >= 0.4:
            category = "B-Grade"
            shelf_life_hours = 12
        else:
            category = "Waste"
            shelf_life_hours = 0

        return {
            "category": category,
            "confidence": float(confidence),
            "shelf_life_hours": shelf_life_hours,
            "suggestions": self._get_suggestions(category),
        }

    def _mock_classification(self, image_s3_uri: str) -> Dict[str, Any]:
        """
        Generate mock classification for demo purposes.

        Uses deterministic pseudo-random based on image URI to ensure
        consistent results for the same image.

        Args:
            image_s3_uri: S3 URI of the image

        Returns:
            Mock classification result
        """
        # Use hash of URI for deterministic pseudo-random
        hash_value = int(hashlib.md5(image_s3_uri.encode()).hexdigest(), 16)
        random.seed(hash_value)

        # Generate confidence with realistic distribution
        # 50% Fresh, 30% B-Grade, 20% Waste
        rand_val = random.random()

        if rand_val < 0.5:
            # Fresh: confidence > 0.7
            confidence = random.uniform(0.71, 0.95)
            category = "Fresh"
            shelf_life_hours = 48
        elif rand_val < 0.8:
            # B-Grade: confidence 0.4-0.7
            confidence = random.uniform(0.45, 0.69)
            category = "B-Grade"
            shelf_life_hours = 12
        else:
            # Waste: confidence < 0.4
            confidence = random.uniform(0.15, 0.39)
            category = "Waste"
            shelf_life_hours = 0

        logger.info(f"Mock classification: {category} (confidence: {confidence:.2f})")

        return {
            "category": category,
            "confidence": confidence,
            "shelf_life_hours": shelf_life_hours,
            "suggestions": self._get_suggestions(category),
            "mock": True,  # Flag to indicate this is mock data
        }

    def _get_suggestions(self, category: str) -> list[str]:
        """
        Get suggestions based on freshness category.

        Args:
            category: Freshness category

        Returns:
            List of suggestions
        """
        suggestions_map = {
            "Fresh": ["Sell at premium price", "Display prominently", "Store in cool place"],
            "B-Grade": [
                "List on marketplace",
                "Consider making juice or pickle",
                "Sell at discounted price",
            ],
            "Waste": ["Use for composting", "Contact waste buyers", "Dispose properly"],
        }
        return suggestions_map.get(category, [])
