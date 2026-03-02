"""
Property-based tests for transaction extraction from natural language.

Feature: hackathon-deliverables
Property: Transaction extraction from natural language
Validates: Requirements 5.1
"""

import pytest
from hypothesis import given, strategies as st, settings, assume
from hypothesis.strategies import composite
from unittest.mock import Mock, patch

from shared.services.voice_service import VoiceService


@composite
def transaction_text_strategy(draw):
    """
    Generate transaction text in Hindi or English.

    Returns:
        Tuple of (text, language_code, expected_item)
    """
    language = draw(st.sampled_from(["hi-IN", "en-IN"]))

    # Common produce items
    items_hi = ["टमाटर", "आलू", "प्याज", "पत्तागोभी", "फूलगोभी"]
    items_en = ["tomatoes", "potatoes", "onions", "cabbage", "cauliflower"]

    # Quantity words
    quantities = [1, 2, 3, 5, 10]

    # Price values
    prices = [20, 30, 40, 50, 100]

    quantity = draw(st.sampled_from(quantities))
    price = draw(st.sampled_from(prices))

    if language == "hi-IN":
        item = draw(st.sampled_from(items_hi))
        # Generate Hindi transaction text
        text = f"{quantity} किलो {item} {price} रुपये"
        expected_item = item
    else:
        item = draw(st.sampled_from(items_en))
        # Generate English transaction text
        text = f"{quantity} kilos of {item} for {price} rupees"
        expected_item = item

    return text, language, expected_item, quantity, price


@given(transaction_data=transaction_text_strategy())
@settings(max_examples=100, deadline=30000)
def test_transaction_extraction_property(transaction_data):
    """
    Property: For any valid transaction text in Hindi or English,
    the extraction should return structured data with item, quantity, and price.

    **Validates: Requirements 5.1**
    """
    text, language_code, expected_item, expected_quantity, expected_price = transaction_data

    # Mock Bedrock client to return extracted data
    with patch("shared.services.voice_service.BedrockClient") as mock_bedrock_class:
        mock_bedrock = Mock()
        mock_bedrock_class.return_value = mock_bedrock

        # Mock extraction result
        mock_bedrock.extract_transaction.return_value = {
            "item_name": expected_item,
            "quantity": float(expected_quantity),
            "unit": "किलो" if language_code == "hi-IN" else "kilos",
            "price": float(expected_price),
            "extracted_successfully": True,
        }

        # Mock DynamoDB client
        with patch("shared.aws.dynamodb_client.DynamoDBClient") as mock_dynamodb_class:
            mock_dynamodb = Mock()
            mock_dynamodb_class.return_value = mock_dynamodb
            mock_dynamodb.put_item.return_value = True

            # Create service and extract transaction
            voice_service = VoiceService()
            result = voice_service.extract_and_store_transaction(
                text=text, vendor_id="test-vendor-123", language_code=language_code
            )

            # Verify result structure
            assert result is not None, "Transaction extraction should not return None"
            assert "transaction_id" in result, "Result should contain transaction_id"
            assert "vendor_id" in result, "Result should contain vendor_id"
            assert "item_name" in result, "Result should contain item_name"
            assert "quantity" in result, "Result should contain quantity"
            assert "unit" in result, "Result should contain unit"
            assert "price_per_unit" in result, "Result should contain price_per_unit"
            assert "total_amount" in result, "Result should contain total_amount"
            assert (
                "extracted_successfully" in result
            ), "Result should contain extracted_successfully"

            # Verify data types
            assert isinstance(result["transaction_id"], str), "transaction_id should be string"
            assert isinstance(result["vendor_id"], str), "vendor_id should be string"
            assert isinstance(result["item_name"], str), "item_name should be string"
            assert isinstance(result["quantity"], float), "quantity should be float"
            assert isinstance(result["unit"], str), "unit should be string"
            assert isinstance(result["price_per_unit"], float), "price_per_unit should be float"
            assert isinstance(result["total_amount"], float), "total_amount should be float"
            assert isinstance(
                result["extracted_successfully"], bool
            ), "extracted_successfully should be bool"

            # Verify values
            assert result["vendor_id"] == "test-vendor-123", "vendor_id should match input"
            assert result["item_name"] == expected_item, "item_name should match expected"
            assert result["quantity"] == float(expected_quantity), "quantity should match expected"
            assert result["price_per_unit"] == float(expected_price), "price should match expected"
            assert result["total_amount"] == float(expected_quantity) * float(
                expected_price
            ), "total_amount should be quantity * price"
            assert result["extracted_successfully"] is True, "extracted_successfully should be True"


@given(text=st.text(min_size=1, max_size=100), language=st.sampled_from(["hi", "en"]))
@settings(max_examples=50, deadline=30000)
def test_transaction_extraction_handles_invalid_text(text, language):
    """
    Property: For any text input, the extraction should handle gracefully
    and return None or valid structure (never crash).

    **Validates: Requirements 5.1**
    """
    language_code = f"{language}-IN"

    # Mock Bedrock client to return failed extraction
    with patch("shared.services.voice_service.BedrockClient") as mock_bedrock_class:
        mock_bedrock = Mock()
        mock_bedrock_class.return_value = mock_bedrock

        # Mock extraction failure
        mock_bedrock.extract_transaction.return_value = {"extracted_successfully": False}

        # Create service and extract transaction
        voice_service = VoiceService()
        result = voice_service.extract_and_store_transaction(
            text=text, vendor_id="test-vendor-123", language_code=language_code
        )

        # Should return None for failed extraction
        assert result is None, "Failed extraction should return None"


def test_transaction_extraction_example():
    """
    Example test: Verify specific transaction extraction works correctly.

    **Validates: Requirements 5.1**
    """
    # Mock Bedrock client
    with patch("shared.services.voice_service.BedrockClient") as mock_bedrock_class:
        mock_bedrock = Mock()
        mock_bedrock_class.return_value = mock_bedrock

        mock_bedrock.extract_transaction.return_value = {
            "item_name": "tomatoes",
            "quantity": 2.0,
            "unit": "kilos",
            "price": 50.0,
            "extracted_successfully": True,
        }

        # Mock DynamoDB client
        with patch("shared.aws.dynamodb_client.DynamoDBClient") as mock_dynamodb_class:
            mock_dynamodb = Mock()
            mock_dynamodb_class.return_value = mock_dynamodb
            mock_dynamodb.put_item.return_value = True

            voice_service = VoiceService()
            result = voice_service.extract_and_store_transaction(
                text="Two kilos of tomatoes for fifty rupees",
                vendor_id="demo-vendor",
                language_code="en-IN",
            )

            assert result is not None
            assert result["item_name"] == "tomatoes"
            assert result["quantity"] == 2.0
            assert result["price_per_unit"] == 50.0
            assert result["total_amount"] == 100.0
