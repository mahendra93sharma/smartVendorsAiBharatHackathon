"""
Amazon Bedrock client for NLP and decision intelligence.

Uses foundation models for transaction extraction and natural language processing.
Supports Claude and Titan models for flexible deployment.
"""

import logging
from typing import Optional, Dict, Any
import json
import re

import boto3
from botocore.exceptions import ClientError

from ..config import Config

logger = logging.getLogger(__name__)


class BedrockClient:
    """
    Amazon Bedrock client for AI/ML capabilities.

    Provides natural language processing for transaction extraction
    from Hindi and English text using foundation models.
    """

    def __init__(self):
        """Initialize Bedrock client."""
        try:
            self.bedrock_runtime = boto3.client("bedrock-runtime", region_name=Config.AWS_REGION)
            self.model_id = Config.BEDROCK_MODEL_ID
            logger.info(
                f"Bedrock client initialized for region {Config.AWS_REGION} with model {self.model_id}"
            )
        except Exception as e:
            logger.error(f"Failed to initialize Bedrock client: {e}")
            raise

    def extract_transaction(self, text: str, language: str = "en") -> Optional[Dict[str, Any]]:
        """
        Extract transaction details from natural language text.

        Args:
            text: Transcribed text containing transaction information
            language: Language of the text (en or hi)

        Returns:
            Dict with extracted fields: item_name, quantity, unit, price_per_unit
        """
        try:
            # Choose appropriate method based on model
            if "claude" in self.model_id.lower():
                return self._extract_with_claude(text, language)
            elif "titan" in self.model_id.lower():
                return self._extract_with_titan(text, language)
            else:
                logger.warning(f"Unknown model {self.model_id}, defaulting to Claude format")
                return self._extract_with_claude(text, language)

        except Exception as e:
            logger.error(f"Unexpected error in extract_transaction: {e}")
            return {
                "item_name": "",
                "quantity": 0.0,
                "unit": "kg",
                "price_per_unit": 0.0,
                "extracted_successfully": False,
                "error": str(e),
            }

    def _extract_with_claude(self, text: str, language: str) -> Dict[str, Any]:
        """
        Extract transaction using Claude model.

        Args:
            text: Input text
            language: Language code

        Returns:
            Extracted transaction data
        """
        try:
            prompt = self._build_claude_prompt(text, language)

            request_body = {
                "prompt": prompt,
                "max_tokens_to_sample": 500,
                "temperature": 0.1,
                "top_p": 0.9,
                "anthropic_version": "bedrock-2023-05-31",
            }

            response = self.bedrock_runtime.invoke_model(
                modelId=self.model_id, body=json.dumps(request_body)
            )

            response_body = json.loads(response["body"].read())
            extracted_data = self._parse_claude_response(response_body, text)

            logger.info(f"Successfully extracted transaction from text: {text[:50]}...")
            return extracted_data

        except ClientError as e:
            logger.error(f"Error calling Bedrock Claude: {e}")
            return {
                "item_name": "",
                "quantity": 0.0,
                "unit": "kg",
                "price_per_unit": 0.0,
                "extracted_successfully": False,
                "error": str(e),
            }

    def _extract_with_titan(self, text: str, language: str) -> Dict[str, Any]:
        """
        Extract transaction using Titan model.

        Args:
            text: Input text
            language: Language code

        Returns:
            Extracted transaction data
        """
        try:
            prompt = self._build_titan_prompt(text, language)

            request_body = {
                "inputText": prompt,
                "textGenerationConfig": {"maxTokenCount": 500, "temperature": 0.1, "topP": 0.9},
            }

            response = self.bedrock_runtime.invoke_model(
                modelId=self.model_id, body=json.dumps(request_body)
            )

            response_body = json.loads(response["body"].read())
            extracted_data = self._parse_titan_response(response_body, text)

            logger.info(f"Successfully extracted transaction from text: {text[:50]}...")
            return extracted_data

        except ClientError as e:
            logger.error(f"Error calling Bedrock Titan: {e}")
            return {
                "item_name": "",
                "quantity": 0.0,
                "unit": "kg",
                "price_per_unit": 0.0,
                "extracted_successfully": False,
                "error": str(e),
            }

    def _build_claude_prompt(self, text: str, language: str) -> str:
        """
        Build prompt for transaction extraction with Claude-specific formatting.

        Args:
            text: Input text
            language: Language code (en or hi)

        Returns:
            Formatted prompt for Claude
        """
        if language == "hi":
            system_instruction = """You are an AI assistant helping street vendors in Delhi-NCR record their transactions. 
Extract transaction details from Hindi text and return ONLY a valid JSON object.

Rules:
- Extract item name (produce item like टमाटर, आलू, प्याज)
- Extract quantity (numeric value)
- Extract unit (किलो, ग्राम, दर्जन, पीस)
- Extract price_per_unit (price in rupees per unit, calculate if total price given)
- If any field cannot be determined, use null
- Return ONLY the JSON object, no other text

Example input: "दो किलो टमाटर पचास रुपये"
Example output: {"item_name": "टमाटर", "quantity": 2.0, "unit": "किलो", "price_per_unit": 25.0}"""
        else:
            system_instruction = """You are an AI assistant helping street vendors in Delhi-NCR record their transactions.
Extract transaction details from English text and return ONLY a valid JSON object.

Rules:
- Extract item name (produce item like tomatoes, potatoes, onions)
- Extract quantity (numeric value)
- Extract unit (kg, grams, dozen, pieces)
- Extract price_per_unit (price in rupees per unit, calculate if total price given)
- If any field cannot be determined, use null
- Return ONLY the JSON object, no other text

Example input: "Two kilos of tomatoes for fifty rupees"
Example output: {"item_name": "tomatoes", "quantity": 2.0, "unit": "kg", "price_per_unit": 25.0}"""

        # Claude format requires specific prompt structure
        prompt = f"\n\nHuman: {system_instruction}\n\nText to extract from: {text}\n\nAssistant: {{"

        return prompt

    def _build_titan_prompt(self, text: str, language: str) -> str:
        """
        Build prompt for transaction extraction with Titan-specific formatting.

        Args:
            text: Input text
            language: Language code (en or hi)

        Returns:
            Formatted prompt for Titan
        """
        if language == "hi":
            instruction = """Extract transaction details from the following Hindi text and return a JSON object.

Required fields:
- item_name: produce item (टमाटर, आलू, प्याज, etc.)
- quantity: numeric value
- unit: किलो, ग्राम, दर्जन, or पीस
- price_per_unit: price in rupees per unit

Example: "दो किलो टमाटर पचास रुपये" -> {"item_name": "टमाटर", "quantity": 2.0, "unit": "किलो", "price_per_unit": 25.0}

Text: {text}

JSON:"""
        else:
            instruction = """Extract transaction details from the following English text and return a JSON object.

Required fields:
- item_name: produce item (tomatoes, potatoes, onions, etc.)
- quantity: numeric value
- unit: kg, grams, dozen, or pieces
- price_per_unit: price in rupees per unit

Example: "Two kilos of tomatoes for fifty rupees" -> {"item_name": "tomatoes", "quantity": 2.0, "unit": "kg", "price_per_unit": 25.0}

Text: {text}

JSON:"""

        return instruction

    def _parse_claude_response(
        self, response: Dict[str, Any], original_text: str
    ) -> Dict[str, Any]:
        """
        Parse Claude response to extract transaction data.

        Args:
            response: Bedrock API response from Claude
            original_text: Original input text for fallback

        Returns:
            Extracted transaction data
        """
        try:
            # Claude response format: {"completion": "...", "stop_reason": "..."}
            completion = response.get("completion", "")

            # The completion should contain JSON, possibly with closing brace
            # Since we started with "{" in the prompt, we need to add it back
            json_text = "{" + completion

            # Find the first complete JSON object
            # Handle case where Claude adds extra text after JSON
            brace_count = 0
            json_end = -1
            for i, char in enumerate(json_text):
                if char == "{":
                    brace_count += 1
                elif char == "}":
                    brace_count -= 1
                    if brace_count == 0:
                        json_end = i + 1
                        break

            if json_end > 0:
                json_text = json_text[:json_end]

            # Parse JSON
            extracted = json.loads(json_text)

            return self._normalize_extraction(extracted)

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from Claude response: {e}")
            logger.error(f"Response completion: {response.get('completion', '')}")
            return {
                "item_name": "",
                "quantity": 0.0,
                "unit": "kg",
                "price_per_unit": 0.0,
                "extracted_successfully": False,
                "error": f"JSON parse error: {str(e)}",
            }
        except Exception as e:
            logger.error(f"Error parsing Claude response: {e}")
            return {
                "item_name": "",
                "quantity": 0.0,
                "unit": "kg",
                "price_per_unit": 0.0,
                "extracted_successfully": False,
                "error": str(e),
            }

    def _parse_titan_response(self, response: Dict[str, Any], original_text: str) -> Dict[str, Any]:
        """
        Parse Titan response to extract transaction data.

        Args:
            response: Bedrock API response from Titan
            original_text: Original input text for fallback

        Returns:
            Extracted transaction data
        """
        try:
            # Titan response format: {"results": [{"outputText": "..."}]}
            results = response.get("results", [])
            if not results:
                raise ValueError("No results in Titan response")

            output_text = results[0].get("outputText", "")

            # Extract JSON from output text
            # Look for JSON object pattern
            json_match = re.search(r"\{[^{}]*\}", output_text)
            if not json_match:
                raise ValueError("No JSON object found in Titan response")

            json_text = json_match.group(0)
            extracted = json.loads(json_text)

            return self._normalize_extraction(extracted)

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from Titan response: {e}")
            logger.error(
                f"Response output: {response.get('results', [{}])[0].get('outputText', '')}"
            )
            return {
                "item_name": "",
                "quantity": 0.0,
                "unit": "kg",
                "price_per_unit": 0.0,
                "extracted_successfully": False,
                "error": f"JSON parse error: {str(e)}",
            }
        except Exception as e:
            logger.error(f"Error parsing Titan response: {e}")
            return {
                "item_name": "",
                "quantity": 0.0,
                "unit": "kg",
                "price_per_unit": 0.0,
                "extracted_successfully": False,
                "error": str(e),
            }

    def _normalize_extraction(self, extracted: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize and validate extracted transaction data.

        Args:
            extracted: Raw extracted data from model

        Returns:
            Normalized transaction data
        """
        # Validate and normalize fields
        item_name = extracted.get("item_name", "")
        quantity = (
            float(extracted.get("quantity", 0.0)) if extracted.get("quantity") is not None else 0.0
        )
        unit = extracted.get("unit", "kg")
        price_per_unit = (
            float(extracted.get("price_per_unit", 0.0))
            if extracted.get("price_per_unit") is not None
            else 0.0
        )

        # Check if extraction was successful
        extracted_successfully = bool(item_name and quantity > 0)

        result = {
            "item_name": item_name,
            "quantity": quantity,
            "unit": unit,
            "price_per_unit": price_per_unit,
            "extracted_successfully": extracted_successfully,
        }

        logger.info(f"Normalized extraction result: {result}")
        return result
