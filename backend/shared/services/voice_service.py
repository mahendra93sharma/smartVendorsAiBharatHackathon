"""
Voice service for transaction recording and transcription.
"""

import logging
from typing import Optional, Dict, Any
from uuid import uuid4

from ..aws.transcribe_client import TranscribeClient
from ..aws.bedrock_client import BedrockClient
from ..aws.s3_client import S3Client
from ..config import Config

logger = logging.getLogger(__name__)


class VoiceService:
    """
    Service for voice transaction recording and processing.

    Handles audio upload, transcription, and transaction extraction.
    """

    def __init__(self):
        """Initialize voice service with AWS clients."""
        self.transcribe_client = TranscribeClient()
        self.bedrock_client = BedrockClient()
        self.s3_client = S3Client()

    def process_voice_transaction(
        self, audio_bytes: bytes, language_code: str, vendor_id: str, media_format: str = "mp3"
    ) -> Optional[Dict[str, Any]]:
        """
        Process voice transaction from audio to structured data.

        Args:
            audio_bytes: Audio file content
            language_code: Language code (hi-IN or en-IN)
            vendor_id: Vendor identifier
            media_format: Audio format (mp3, wav, etc.)

        Returns:
            Dict with transcription and extracted transaction data
        """
        try:
            # Determine file extension based on format
            file_ext = media_format.lower()
            content_type_map = {
                "mp3": "audio/mpeg",
                "wav": "audio/wav",
                "flac": "audio/flac",
                "ogg": "audio/ogg",
                "webm": "audio/webm",
            }
            content_type = content_type_map.get(file_ext, "audio/mpeg")

            # Upload audio to S3
            audio_key = f"audio/{vendor_id}/{uuid4()}.{file_ext}"
            s3_uri = self.s3_client.upload_file(
                file_bytes=audio_bytes,
                bucket=Config.S3_AUDIO_BUCKET,
                key=audio_key,
                content_type=content_type,
            )

            if not s3_uri:
                logger.error("Failed to upload audio to S3")
                # Fallback to mock transcription for demo
                if Config.DEMO_MODE:
                    logger.info("Using mock transcription in demo mode (S3 upload failed)")
                    return self._get_mock_transcription_result(language_code)
                return None

            # Start transcription job
            job_name = f"transcribe-{uuid4()}"
            job_id = self.transcribe_client.start_transcription_job(
                job_name=job_name,
                s3_uri=s3_uri,
                language_code=language_code,
                media_format=media_format,
            )

            if not job_id:
                logger.error("Failed to start transcription job")
                # Fallback to mock transcription for demo
                if Config.DEMO_MODE:
                    logger.info("Using mock transcription in demo mode (job start failed)")
                    return self._get_mock_transcription_result(language_code)
                return None

            # Get transcription result
            transcription = self.transcribe_client.get_transcription_result(job_name)

            if not transcription:
                logger.error("Failed to get transcription result")
                # Fallback to mock transcription for demo
                if Config.DEMO_MODE:
                    logger.info("Using mock transcription in demo mode (result retrieval failed)")
                    return self._get_mock_transcription_result(language_code)
                return None

            # Extract transaction using Bedrock
            language = "hi" if language_code == "hi-IN" else "en"
            extracted = self.bedrock_client.extract_transaction(
                text=transcription["text"], language=language
            )

            # Clean up transcription job
            self.transcribe_client.delete_transcription_job(job_name)

            return {
                "transcription": transcription,
                "extracted_transaction": extracted,
                "audio_s3_uri": s3_uri,
            }
        except Exception as e:
            logger.error(f"Error processing voice transaction: {e}")
            # Fallback to mock transcription for demo
            if Config.DEMO_MODE:
                logger.info("Using mock transcription in demo mode (exception)")
                return self._get_mock_transcription_result(language_code)
            return None

    def _get_mock_transcription_result(self, language_code: str) -> Dict[str, Any]:
        """
        Get mock transcription result for demo mode.

        Args:
            language_code: Language code (hi-IN or en-IN)

        Returns:
            Mock transcription and extraction result
        """
        if language_code == "hi-IN":
            mock_text = "दो किलो टमाटर पचास रुपये"
            mock_extracted = {
                "item_name": "टमाटर",
                "quantity": 2.0,
                "unit": "किलो",
                "price": 50.0,
                "extracted_successfully": True,
            }
        else:
            mock_text = "Two kilos of tomatoes for fifty rupees"
            mock_extracted = {
                "item_name": "tomatoes",
                "quantity": 2.0,
                "unit": "kilos",
                "price": 50.0,
                "extracted_successfully": True,
            }

        return {
            "transcription": {"text": mock_text, "confidence": 0.85, "transcript_uri": None},
            "extracted_transaction": mock_extracted,
            "audio_s3_uri": None,
        }

    def extract_and_store_transaction(
        self, text: str, vendor_id: str, language_code: str = "en-IN"
    ) -> Optional[Dict[str, Any]]:
        """
        Extract transaction from text and store in DynamoDB.

        Args:
            text: Transcribed text
            vendor_id: Vendor identifier
            language_code: Language code (hi-IN or en-IN)

        Returns:
            Dict with transaction details
        """
        try:
            from ..aws.dynamodb_client import DynamoDBClient
            from datetime import datetime

            # Extract transaction using Bedrock
            language = "hi" if language_code == "hi-IN" else "en"
            extracted = self.bedrock_client.extract_transaction(text=text, language=language)

            if not extracted or not extracted.get("extracted_successfully"):
                logger.error("Failed to extract transaction from text")
                return None

            # Create transaction record
            transaction_id = str(uuid4())
            timestamp = datetime.utcnow().isoformat()

            transaction = {
                "transaction_id": transaction_id,
                "vendor_id": vendor_id,
                "item_name": extracted.get("item_name", ""),
                "quantity": float(extracted.get("quantity", 0)),
                "unit": extracted.get("unit", ""),
                "price_per_unit": float(extracted.get("price", 0)),
                "total_amount": float(extracted.get("quantity", 0))
                * float(extracted.get("price", 0)),
                "timestamp": timestamp,
                "recorded_via": "voice",
                "extracted_successfully": True,
            }

            # Store in DynamoDB
            dynamodb_client = DynamoDBClient()
            success = dynamodb_client.put_item(
                table_name=Config.DYNAMODB_TRANSACTIONS_TABLE, item=transaction
            )

            if not success:
                logger.error("Failed to store transaction in DynamoDB")
                return None

            return transaction

        except Exception as e:
            logger.error(f"Error extracting and storing transaction: {e}")
            return None
