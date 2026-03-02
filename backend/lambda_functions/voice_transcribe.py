"""
Lambda function for voice transcription.

Handles POST /voice/transcribe endpoint.
"""

import json
import logging
import base64
from typing import Dict, Any

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Import shared modules
import sys

sys.path.append("/opt/python")  # Lambda layer path

from shared.services.voice_service import VoiceService
from shared.config import Config


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda handler for voice transcription.

    Accepts audio file upload, transcribes using AWS Transcribe.

    Args:
        event: API Gateway event
        context: Lambda context

    Returns:
        API Gateway response
    """
    try:
        logger.info("Processing voice transcription request")

        # Parse request body
        body = json.loads(event.get("body", "{}"))

        # Get audio data (base64 encoded)
        audio_base64 = body.get("audio")
        language_code = body.get("language_code", "en-IN")
        vendor_id = body.get("vendor_id")
        media_format = body.get("media_format", "mp3")

        # Validate inputs
        if not audio_base64:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Missing audio data"}),
            }

        if not vendor_id:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Missing vendor_id"}),
            }

        if language_code not in Config.TRANSCRIBE_LANGUAGE_CODES:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": f"Unsupported language: {language_code}"}),
            }

        # Decode audio
        audio_bytes = base64.b64decode(audio_base64)

        # Process voice transaction
        voice_service = VoiceService()
        result = voice_service.process_voice_transaction(
            audio_bytes=audio_bytes,
            language_code=language_code,
            vendor_id=vendor_id,
            media_format=media_format,
        )

        if not result:
            return {
                "statusCode": 500,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Failed to process voice transaction"}),
            }

        logger.info("Successfully processed voice transcription")

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(
                {
                    "transcription": result["transcription"],
                    "extracted_transaction": result["extracted_transaction"],
                }
            ),
        }

    except Exception as e:
        logger.error(f"Error in voice transcription handler: {e}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Internal server error"}),
        }
