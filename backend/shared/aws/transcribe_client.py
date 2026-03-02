"""
AWS Transcribe client for voice-to-text conversion.

Handles audio transcription for Hindi and English languages.
"""

import logging
from typing import Optional
import time
import json
import urllib.request

import boto3
from botocore.exceptions import ClientError

from ..config import Config

logger = logging.getLogger(__name__)


class TranscribeClient:
    """
    AWS Transcribe client for speech-to-text conversion.

    Supports Hindi (hi-IN) and English (en-IN) language codes.
    """

    def __init__(self):
        """Initialize Transcribe client."""
        try:
            self.transcribe_client = boto3.client("transcribe", region_name=Config.AWS_REGION)
            logger.info(f"Transcribe client initialized for region {Config.AWS_REGION}")
        except Exception as e:
            logger.error(f"Failed to initialize Transcribe client: {e}")
            raise

    def start_transcription_job(
        self, job_name: str, s3_uri: str, language_code: str, media_format: str = "mp3"
    ) -> Optional[str]:
        """
        Start AWS Transcribe job for audio file.

        Args:
            job_name: Unique job name
            s3_uri: S3 location of audio file
            language_code: Language code (hi-IN or en-IN)
            media_format: Audio format (mp3, wav, flac, etc.)

        Returns:
            Job name if successful, None otherwise
        """
        try:
            if language_code not in Config.TRANSCRIBE_LANGUAGE_CODES:
                logger.error(f"Unsupported language code: {language_code}")
                return None

            # Validate media format
            supported_formats = ["mp3", "mp4", "wav", "flac", "ogg", "amr", "webm"]
            if media_format.lower() not in supported_formats:
                logger.warning(f"Unsupported media format: {media_format}, defaulting to mp3")
                media_format = "mp3"

            self.transcribe_client.start_transcription_job(
                TranscriptionJobName=job_name,
                Media={"MediaFileUri": s3_uri},
                MediaFormat=media_format,
                LanguageCode=language_code,
            )

            logger.info(f"Started transcription job: {job_name} for language {language_code}")
            return job_name

        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "Unknown")

            # Handle specific error cases
            if error_code == "LimitExceededException":
                logger.error(f"Transcribe quota exceeded for job {job_name}")
            elif error_code == "ConflictException":
                logger.error(f"Transcription job {job_name} already exists")
            else:
                logger.error(f"Error starting transcription job: {e}")

            return None
        except Exception as e:
            logger.error(f"Unexpected error starting transcription job: {e}")
            return None

    def get_transcription_result(self, job_name: str, max_wait_seconds: int = 60) -> Optional[dict]:
        """
        Get transcription result, polling until complete.

        Args:
            job_name: Transcription job name
            max_wait_seconds: Maximum time to wait for completion

        Returns:
            Transcription result dict with 'text' and 'confidence', or None
        """
        try:
            start_time = time.time()

            while time.time() - start_time < max_wait_seconds:
                response = self.transcribe_client.get_transcription_job(
                    TranscriptionJobName=job_name
                )

                status = response["TranscriptionJob"]["TranscriptionJobStatus"]

                if status == "COMPLETED":
                    transcript_uri = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]

                    # Fetch and parse the transcript JSON
                    try:
                        with urllib.request.urlopen(transcript_uri) as url_response:
                            transcript_data = json.loads(url_response.read().decode())

                        # Extract transcript text and confidence
                        results = transcript_data.get("results", {})
                        transcripts = results.get("transcripts", [])

                        if not transcripts:
                            logger.warning(f"No transcripts found in result for job {job_name}")
                            return None

                        text = transcripts[0].get("transcript", "")

                        # Calculate average confidence from items
                        items = results.get("items", [])
                        confidences = [
                            float(item.get("alternatives", [{}])[0].get("confidence", 0))
                            for item in items
                            if item.get("type") != "punctuation"
                        ]

                        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0

                        logger.info(
                            f"Transcription job {job_name} completed with confidence {avg_confidence:.2f}"
                        )

                        return {
                            "text": text,
                            "confidence": avg_confidence,
                            "transcript_uri": transcript_uri,
                        }
                    except Exception as e:
                        logger.error(f"Error parsing transcript JSON: {e}")
                        # Fallback to mock transcription for demo
                        if Config.DEMO_MODE:
                            logger.info("Using mock transcription in demo mode")
                            return {
                                "text": "दो किलो टमाटर पचास रुपये",
                                "confidence": 0.85,
                                "transcript_uri": transcript_uri,
                            }
                        return None

                elif status == "FAILED":
                    failure_reason = response["TranscriptionJob"].get("FailureReason", "Unknown")
                    logger.error(f"Transcription job {job_name} failed: {failure_reason}")

                    # Fallback to mock transcription for demo
                    if Config.DEMO_MODE:
                        logger.info("Using mock transcription in demo mode after failure")
                        return {
                            "text": "दो किलो टमाटर पचास रुपये",
                            "confidence": 0.85,
                            "transcript_uri": None,
                        }
                    return None

                time.sleep(2)

            logger.warning(f"Transcription job {job_name} timed out after {max_wait_seconds}s")

            # Fallback to mock transcription for demo
            if Config.DEMO_MODE:
                logger.info("Using mock transcription in demo mode after timeout")
                return {
                    "text": "दो किलो टमाटर पचास रुपये",
                    "confidence": 0.85,
                    "transcript_uri": None,
                }
            return None

        except ClientError as e:
            logger.error(f"Error getting transcription result: {e}")

            # Fallback to mock transcription for demo
            if Config.DEMO_MODE:
                logger.info("Using mock transcription in demo mode after error")
                return {
                    "text": "दो किलो टमाटर पचास रुपये",
                    "confidence": 0.85,
                    "transcript_uri": None,
                }
            return None

    def delete_transcription_job(self, job_name: str) -> bool:
        """
        Delete transcription job.

        Args:
            job_name: Transcription job name

        Returns:
            True if successful, False otherwise
        """
        try:
            self.transcribe_client.delete_transcription_job(TranscriptionJobName=job_name)
            logger.info(f"Deleted transcription job: {job_name}")
            return True
        except ClientError as e:
            logger.error(f"Error deleting transcription job: {e}")
            return False
