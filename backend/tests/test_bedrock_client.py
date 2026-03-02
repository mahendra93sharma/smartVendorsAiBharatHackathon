"""
Unit tests for Bedrock client transaction extraction.

Tests the NLP and decision intelligence capabilities.
"""

import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from botocore.exceptions import ClientError

from shared.aws.bedrock_client import BedrockClient


class TestBedrockClient:
    """Test suite for BedrockClient."""

    @pytest.fixture
    def bedrock_client(self):
        """Create BedrockClient instance with mocked boto3."""
        with patch("shared.aws.bedrock_client.boto3.client"):
            client = BedrockClient()
            client.bedrock_runtime = Mock()
            return client

    def test_extract_transaction_english_claude(self, bedrock_client):
        """Test transaction extraction from English text using Claude."""
        # Mock Claude response
        mock_response = {"body": MagicMock()}
        mock_response["body"].read.return_value = json.dumps(
            {
                "completion": '"item_name": "tomatoes", "quantity": 2.0, "unit": "kg", "price_per_unit": 25.0}',
                "stop_reason": "stop_sequence",
            }
        ).encode()

        bedrock_client.bedrock_runtime.invoke_model.return_value = mock_response
        bedrock_client.model_id = "anthropic.claude-v2"

        # Test extraction
        result = bedrock_client.extract_transaction(
            text="Two kilos of tomatoes for fifty rupees", language="en"
        )

        assert result is not None
        assert result["item_name"] == "tomatoes"
        assert result["quantity"] == 2.0
        assert result["unit"] == "kg"
        assert result["price_per_unit"] == 25.0
        assert result["extracted_successfully"] is True

    def test_extract_transaction_hindi_claude(self, bedrock_client):
        """Test transaction extraction from Hindi text using Claude."""
        # Mock Claude response
        mock_response = {"body": MagicMock()}
        mock_response["body"].read.return_value = json.dumps(
            {
                "completion": '"item_name": "टमाटर", "quantity": 2.0, "unit": "किलो", "price_per_unit": 25.0}',
                "stop_reason": "stop_sequence",
            }
        ).encode()

        bedrock_client.bedrock_runtime.invoke_model.return_value = mock_response
        bedrock_client.model_id = "anthropic.claude-v2"

        # Test extraction
        result = bedrock_client.extract_transaction(text="दो किलो टमाटर पचास रुपये", language="hi")

        assert result is not None
        assert result["item_name"] == "टमाटर"
        assert result["quantity"] == 2.0
        assert result["unit"] == "किलो"
        assert result["price_per_unit"] == 25.0
        assert result["extracted_successfully"] is True

    def test_extract_transaction_titan(self, bedrock_client):
        """Test transaction extraction using Titan model."""
        # Mock Titan response
        mock_response = {"body": MagicMock()}
        mock_response["body"].read.return_value = json.dumps(
            {
                "results": [
                    {
                        "outputText": 'Here is the extracted data: {"item_name": "potatoes", "quantity": 5.0, "unit": "kg", "price_per_unit": 30.0}'
                    }
                ]
            }
        ).encode()

        bedrock_client.bedrock_runtime.invoke_model.return_value = mock_response
        bedrock_client.model_id = "amazon.titan-text-express-v1"

        # Test extraction
        result = bedrock_client.extract_transaction(
            text="Five kilograms of potatoes for one hundred fifty rupees", language="en"
        )

        assert result is not None
        assert result["item_name"] == "potatoes"
        assert result["quantity"] == 5.0
        assert result["unit"] == "kg"
        assert result["price_per_unit"] == 30.0
        assert result["extracted_successfully"] is True

    def test_extract_transaction_incomplete_data(self, bedrock_client):
        """Test extraction with incomplete data."""
        # Mock response with missing fields
        mock_response = {"body": MagicMock()}
        mock_response["body"].read.return_value = json.dumps(
            {
                "completion": '"item_name": "onions", "quantity": null, "unit": "kg", "price_per_unit": 0.0}',
                "stop_reason": "stop_sequence",
            }
        ).encode()

        bedrock_client.bedrock_runtime.invoke_model.return_value = mock_response
        bedrock_client.model_id = "anthropic.claude-v2"

        # Test extraction
        result = bedrock_client.extract_transaction(text="Some onions", language="en")

        assert result is not None
        assert result["item_name"] == "onions"
        assert result["quantity"] == 0.0
        assert result["extracted_successfully"] is False

    def test_extract_transaction_api_error(self, bedrock_client):
        """Test handling of Bedrock API errors."""
        # Mock API error
        bedrock_client.bedrock_runtime.invoke_model.side_effect = ClientError(
            {"Error": {"Code": "ThrottlingException", "Message": "Rate exceeded"}}, "InvokeModel"
        )
        bedrock_client.model_id = "anthropic.claude-v2"

        # Test extraction
        result = bedrock_client.extract_transaction(text="Two kilos of tomatoes", language="en")

        assert result is not None
        assert result["extracted_successfully"] is False
        assert "error" in result

    def test_extract_transaction_invalid_json(self, bedrock_client):
        """Test handling of invalid JSON in response."""
        # Mock response with invalid JSON
        mock_response = {"body": MagicMock()}
        mock_response["body"].read.return_value = json.dumps(
            {"completion": "This is not valid JSON", "stop_reason": "stop_sequence"}
        ).encode()

        bedrock_client.bedrock_runtime.invoke_model.return_value = mock_response
        bedrock_client.model_id = "anthropic.claude-v2"

        # Test extraction
        result = bedrock_client.extract_transaction(text="Two kilos of tomatoes", language="en")

        assert result is not None
        assert result["extracted_successfully"] is False
        assert "error" in result

    def test_build_claude_prompt_english(self, bedrock_client):
        """Test Claude prompt building for English."""
        bedrock_client.model_id = "anthropic.claude-v2"
        prompt = bedrock_client._build_claude_prompt("Two kilos of tomatoes", "en")

        assert "Human:" in prompt
        assert "Assistant:" in prompt
        assert "Two kilos of tomatoes" in prompt
        assert "JSON object" in prompt

    def test_build_claude_prompt_hindi(self, bedrock_client):
        """Test Claude prompt building for Hindi."""
        bedrock_client.model_id = "anthropic.claude-v2"
        prompt = bedrock_client._build_claude_prompt("दो किलो टमाटर", "hi")

        assert "Human:" in prompt
        assert "Assistant:" in prompt
        assert "दो किलो टमाटर" in prompt
        assert "Hindi text" in prompt

    def test_normalize_extraction(self, bedrock_client):
        """Test extraction normalization."""
        raw_data = {
            "item_name": "tomatoes",
            "quantity": "2.5",
            "unit": "kg",
            "price_per_unit": "30",
        }

        result = bedrock_client._normalize_extraction(raw_data)

        assert result["item_name"] == "tomatoes"
        assert result["quantity"] == 2.5
        assert isinstance(result["quantity"], float)
        assert result["price_per_unit"] == 30.0
        assert isinstance(result["price_per_unit"], float)
        assert result["extracted_successfully"] is True

    def test_normalize_extraction_null_values(self, bedrock_client):
        """Test extraction normalization with null values."""
        raw_data = {"item_name": "tomatoes", "quantity": None, "unit": "kg", "price_per_unit": None}

        result = bedrock_client._normalize_extraction(raw_data)

        assert result["item_name"] == "tomatoes"
        assert result["quantity"] == 0.0
        assert result["price_per_unit"] == 0.0
        assert result["extracted_successfully"] is False
