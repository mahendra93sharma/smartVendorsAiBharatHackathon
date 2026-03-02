"""
Property-based tests for produce freshness classification.

Tests the SageMaker endpoint integration and classification logic.
"""

import pytest
from hypothesis import given, strategies as st, settings, assume
from unittest.mock import Mock, patch, MagicMock
import json
import io

from shared.aws.sagemaker_client import SageMakerClient
from shared.services.freshness_service import FreshnessService


# Feature: hackathon-deliverables, Property 5: Freshness classification into valid categories
# **Validates: Requirements 5.3**


@st.composite
def s3_uri_strategy(draw):
    """Generate valid S3 URIs for testing."""
    bucket = draw(
        st.text(
            alphabet=st.characters(
                whitelist_categories=("Ll", "Nd"), min_codepoint=97, max_codepoint=122
            ),
            min_size=3,
            max_size=20,
        )
    )
    vendor_id = draw(st.uuids())
    image_id = draw(st.uuids())
    return f"s3://{bucket}/images/{vendor_id}/{image_id}.jpg"


@st.composite
def confidence_score_strategy(draw):
    """Generate confidence scores in valid range [0.0, 1.0]."""
    return draw(st.floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False))


@st.composite
def sagemaker_response_strategy(draw):
    """Generate mock SageMaker endpoint responses."""
    confidence = draw(confidence_score_strategy())

    # Support multiple response formats
    format_choice = draw(st.integers(min_value=0, max_value=2))

    if format_choice == 0:
        return {"confidence": confidence}
    elif format_choice == 1:
        return {"score": confidence}
    else:
        return {"predictions": [{"score": confidence}]}


@pytest.mark.property
@given(s3_uri=s3_uri_strategy(), response=sagemaker_response_strategy())
@settings(max_examples=100, deadline=None)
def test_freshness_classification_returns_valid_category(s3_uri, response):
    """
    Property: For any produce image, classification returns exactly one valid category.

    **Validates: Requirements 5.3**
    """
    with patch("shared.aws.sagemaker_client.boto3.client") as mock_boto:
        # Mock SageMaker response
        mock_client = MagicMock()
        mock_response = {"Body": io.BytesIO(json.dumps(response).encode())}
        mock_client.invoke_endpoint.return_value = mock_response
        mock_boto.return_value = mock_client

        # Create client and classify
        client = SageMakerClient()
        client.demo_mode = False  # Force real classification path
        result = client.classify_produce_freshness(s3_uri)

        # Verify result structure
        assert result is not None, "Classification should return a result"
        assert "category" in result, "Result must contain 'category'"
        assert "confidence" in result, "Result must contain 'confidence'"
        assert "shelf_life_hours" in result, "Result must contain 'shelf_life_hours'"
        assert "suggestions" in result, "Result must contain 'suggestions'"

        # Verify category is one of the three valid values
        valid_categories = {"Fresh", "B-Grade", "Waste"}
        assert (
            result["category"] in valid_categories
        ), f"Category must be one of {valid_categories}, got {result['category']}"

        # Verify confidence is in valid range
        assert (
            0.0 <= result["confidence"] <= 1.0
        ), f"Confidence must be between 0 and 1, got {result['confidence']}"

        # Verify shelf_life_hours is non-negative
        assert (
            result["shelf_life_hours"] >= 0
        ), f"Shelf life must be non-negative, got {result['shelf_life_hours']}"

        # Verify suggestions is a list
        assert isinstance(result["suggestions"], list), "Suggestions must be a list"


@pytest.mark.property
@given(confidence=confidence_score_strategy())
@settings(max_examples=100, deadline=None)
def test_confidence_threshold_mapping(confidence):
    """
    Property: Confidence thresholds correctly map to categories.

    Tests the requirement:
    - >0.7 for Fresh
    - 0.4-0.7 for B-Grade
    - <0.4 for Waste

    **Validates: Requirements 5.3**
    """
    with patch("shared.aws.sagemaker_client.boto3.client") as mock_boto:
        # Mock SageMaker response with specific confidence
        mock_client = MagicMock()
        mock_response = {"Body": io.BytesIO(json.dumps({"confidence": confidence}).encode())}
        mock_client.invoke_endpoint.return_value = mock_response
        mock_boto.return_value = mock_client

        # Create client and classify
        client = SageMakerClient()
        client.demo_mode = False
        result = client.classify_produce_freshness("s3://test-bucket/test.jpg")

        # Verify confidence threshold logic
        if confidence > 0.7:
            assert (
                result["category"] == "Fresh"
            ), f"Confidence {confidence} > 0.7 should map to Fresh"
            assert result["shelf_life_hours"] == 48, "Fresh produce should have 48h shelf life"
        elif confidence >= 0.4:
            assert (
                result["category"] == "B-Grade"
            ), f"Confidence {confidence} in [0.4, 0.7] should map to B-Grade"
            assert result["shelf_life_hours"] == 12, "B-Grade produce should have 12h shelf life"
        else:
            assert (
                result["category"] == "Waste"
            ), f"Confidence {confidence} < 0.4 should map to Waste"
            assert result["shelf_life_hours"] == 0, "Waste produce should have 0h shelf life"


@pytest.mark.property
@given(s3_uri=s3_uri_strategy())
@settings(max_examples=50, deadline=None)
def test_mock_classification_consistency(s3_uri):
    """
    Property: Mock classification returns consistent results for same image.

    **Validates: Requirements 5.3**
    """
    client = SageMakerClient()
    client.demo_mode = True

    # Classify same image twice
    result1 = client.classify_produce_freshness(s3_uri)
    result2 = client.classify_produce_freshness(s3_uri)

    # Results should be identical (deterministic)
    assert result1["category"] == result2["category"], "Mock classification should be deterministic"
    assert result1["confidence"] == result2["confidence"], "Mock confidence should be deterministic"
    assert (
        result1["shelf_life_hours"] == result2["shelf_life_hours"]
    ), "Mock shelf life should be deterministic"


@pytest.mark.property
@given(s3_uri=s3_uri_strategy())
@settings(max_examples=50, deadline=None)
def test_fallback_to_mock_on_error(s3_uri):
    """
    Property: Classification falls back to mock when SageMaker fails.

    **Validates: Requirements 5.3, 8.4**
    """
    with patch("shared.aws.sagemaker_client.boto3.client") as mock_boto:
        # Mock SageMaker to raise an error
        mock_client = MagicMock()
        mock_client.invoke_endpoint.side_effect = Exception("Endpoint unavailable")
        mock_boto.return_value = mock_client

        # Create client and classify
        client = SageMakerClient()
        client.demo_mode = False
        result = client.classify_produce_freshness(s3_uri)

        # Should still return a valid result (fallback to mock)
        assert result is not None, "Should fallback to mock classification"
        assert result["category"] in {
            "Fresh",
            "B-Grade",
            "Waste",
        }, "Fallback should return valid category"
        assert "mock" in result, "Fallback result should be flagged as mock"
        assert result["mock"] is True, "Mock flag should be True"


@pytest.mark.property
@given(image_bytes=st.binary(min_size=100, max_size=10000), vendor_id=st.uuids())
@settings(max_examples=50, deadline=None)
def test_freshness_service_end_to_end(image_bytes, vendor_id):
    """
    Property: FreshnessService handles image upload and classification.

    **Validates: Requirements 5.3**
    """
    with patch("shared.services.freshness_service.S3Client") as mock_s3, patch(
        "shared.services.freshness_service.SageMakerClient"
    ) as mock_sagemaker:
        # Mock S3 upload
        mock_s3_instance = MagicMock()
        mock_s3_instance.upload_file.return_value = f"s3://test-bucket/images/{vendor_id}/test.jpg"
        mock_s3.return_value = mock_s3_instance

        # Mock SageMaker classification
        mock_sagemaker_instance = MagicMock()
        mock_sagemaker_instance.classify_produce_freshness.return_value = {
            "category": "Fresh",
            "confidence": 0.85,
            "shelf_life_hours": 48,
            "suggestions": ["Sell at premium price"],
        }
        mock_sagemaker.return_value = mock_sagemaker_instance

        # Create service and classify
        service = FreshnessService()
        result = service.classify_produce(image_bytes=image_bytes, vendor_id=str(vendor_id))

        # Verify service called both S3 and SageMaker
        assert mock_s3_instance.upload_file.called, "Should upload image to S3"
        assert (
            mock_sagemaker_instance.classify_produce_freshness.called
        ), "Should classify using SageMaker"

        # Verify result
        assert result is not None, "Service should return result"
        assert result["category"] in {
            "Fresh",
            "B-Grade",
            "Waste",
        }, "Service should return valid category"
        assert "image_s3_uri" in result, "Result should include S3 URI"


@pytest.mark.unit
def test_suggestions_for_each_category():
    """
    Unit test: Verify suggestions are provided for each category.

    **Validates: Requirements 5.3**
    """
    client = SageMakerClient()

    # Test Fresh suggestions
    fresh_suggestions = client._get_suggestions("Fresh")
    assert len(fresh_suggestions) > 0, "Fresh category should have suggestions"
    assert any(
        "premium" in s.lower() for s in fresh_suggestions
    ), "Fresh suggestions should mention premium pricing"

    # Test B-Grade suggestions
    bgrade_suggestions = client._get_suggestions("B-Grade")
    assert len(bgrade_suggestions) > 0, "B-Grade category should have suggestions"
    assert any(
        "marketplace" in s.lower() or "juice" in s.lower() for s in bgrade_suggestions
    ), "B-Grade suggestions should mention marketplace or alternative uses"

    # Test Waste suggestions
    waste_suggestions = client._get_suggestions("Waste")
    assert len(waste_suggestions) > 0, "Waste category should have suggestions"
    assert any(
        "compost" in s.lower() for s in waste_suggestions
    ), "Waste suggestions should mention composting"


@pytest.mark.unit
def test_demo_mode_enabled():
    """
    Unit test: Verify demo mode uses mock classification.

    **Validates: Requirements 5.7**
    """
    with patch("shared.aws.sagemaker_client.Config") as mock_config:
        mock_config.DEMO_MODE = True
        mock_config.AWS_REGION = "ap-south-1"

        client = SageMakerClient()
        result = client.classify_produce_freshness("s3://test/image.jpg")

        assert result is not None, "Demo mode should return result"
        assert "mock" in result, "Demo mode should flag result as mock"
        assert result["mock"] is True, "Mock flag should be True in demo mode"
