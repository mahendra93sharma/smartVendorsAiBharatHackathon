"""
Tests for Voice Service.

Tests voice transaction processing with mock AWS services.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock

from shared.services.voice_service import VoiceService
from shared.config import Config


@pytest.fixture
def voice_service():
    """Create VoiceService instance for testing."""
    with patch("shared.services.voice_service.TranscribeClient"):
        with patch("shared.services.voice_service.BedrockClient"):
            with patch("shared.services.voice_service.S3Client"):
                service = VoiceService()
                yield service


class TestVoiceService:
    """Test suite for VoiceService."""

    def test_initialization(self, voice_service):
        """Test VoiceService initializes correctly."""
        assert voice_service is not None
        assert voice_service.transcribe_client is not None
        assert voice_service.bedrock_client is not None
        assert voice_service.s3_client is not None

    def test_process_voice_transaction_success(self, voice_service):
        """Test successful voice transaction processing."""
        # Mock S3 upload
        voice_service.s3_client.upload_file = Mock(return_value="s3://bucket/audio.mp3")

        # Mock transcription job
        voice_service.transcribe_client.start_transcription_job = Mock(return_value="job-123")
        voice_service.transcribe_client.get_transcription_result = Mock(
            return_value={
                "text": "दो किलो टमाटर पचास रुपये",
                "confidence": 0.90,
                "transcript_uri": "https://example.com/transcript.json",
            }
        )
        voice_service.transcribe_client.delete_transcription_job = Mock(return_value=True)

        # Mock Bedrock extraction
        voice_service.bedrock_client.extract_transaction = Mock(
            return_value={
                "item_name": "टमाटर",
                "quantity": 2.0,
                "unit": "किलो",
                "price": 50.0,
                "extracted_successfully": True,
            }
        )

        # Process transaction
        audio_bytes = b"fake audio data"
        result = voice_service.process_voice_transaction(
            audio_bytes=audio_bytes, language_code="hi-IN", vendor_id="vendor-123"
        )

        assert result is not None
        assert "transcription" in result
        assert "extracted_transaction" in result
        assert "audio_s3_uri" in result
        assert result["transcription"]["text"] == "दो किलो टमाटर पचास रुपये"
        assert result["extracted_transaction"]["item_name"] == "टमाटर"

    def test_process_voice_transaction_s3_upload_failure(self, voice_service):
        """Test voice transaction processing when S3 upload fails."""
        # Mock S3 upload failure
        voice_service.s3_client.upload_file = Mock(return_value=None)

        audio_bytes = b"fake audio data"
        result = voice_service.process_voice_transaction(
            audio_bytes=audio_bytes, language_code="hi-IN", vendor_id="vendor-123"
        )

        assert result is None

    def test_process_voice_transaction_s3_upload_failure_demo_mode(self, voice_service):
        """Test voice transaction processing when S3 upload fails in demo mode."""
        with patch.object(Config, "DEMO_MODE", True):
            # Mock S3 upload failure
            voice_service.s3_client.upload_file = Mock(return_value=None)

            audio_bytes = b"fake audio data"
            result = voice_service.process_voice_transaction(
                audio_bytes=audio_bytes, language_code="hi-IN", vendor_id="vendor-123"
            )

            # Should return mock data in demo mode
            assert result is not None
            assert result["transcription"]["text"] == "दो किलो टमाटर पचास रुपये"
            assert result["transcription"]["confidence"] == 0.85

    def test_process_voice_transaction_transcription_job_failure(self, voice_service):
        """Test voice transaction processing when transcription job fails to start."""
        # Mock S3 upload success
        voice_service.s3_client.upload_file = Mock(return_value="s3://bucket/audio.mp3")

        # Mock transcription job failure
        voice_service.transcribe_client.start_transcription_job = Mock(return_value=None)

        audio_bytes = b"fake audio data"
        result = voice_service.process_voice_transaction(
            audio_bytes=audio_bytes, language_code="hi-IN", vendor_id="vendor-123"
        )

        assert result is None

    def test_process_voice_transaction_transcription_result_failure(self, voice_service):
        """Test voice transaction processing when transcription result retrieval fails."""
        # Mock S3 upload success
        voice_service.s3_client.upload_file = Mock(return_value="s3://bucket/audio.mp3")

        # Mock transcription job success but result failure
        voice_service.transcribe_client.start_transcription_job = Mock(return_value="job-123")
        voice_service.transcribe_client.get_transcription_result = Mock(return_value=None)

        audio_bytes = b"fake audio data"
        result = voice_service.process_voice_transaction(
            audio_bytes=audio_bytes, language_code="hi-IN", vendor_id="vendor-123"
        )

        assert result is None

    def test_process_voice_transaction_english(self, voice_service):
        """Test voice transaction processing for English language."""
        # Mock S3 upload
        voice_service.s3_client.upload_file = Mock(return_value="s3://bucket/audio.mp3")

        # Mock transcription job
        voice_service.transcribe_client.start_transcription_job = Mock(return_value="job-123")
        voice_service.transcribe_client.get_transcription_result = Mock(
            return_value={
                "text": "Two kilos of tomatoes for fifty rupees",
                "confidence": 0.92,
                "transcript_uri": "https://example.com/transcript.json",
            }
        )
        voice_service.transcribe_client.delete_transcription_job = Mock(return_value=True)

        # Mock Bedrock extraction
        voice_service.bedrock_client.extract_transaction = Mock(
            return_value={
                "item_name": "tomatoes",
                "quantity": 2.0,
                "unit": "kilos",
                "price": 50.0,
                "extracted_successfully": True,
            }
        )

        # Process transaction
        audio_bytes = b"fake audio data"
        result = voice_service.process_voice_transaction(
            audio_bytes=audio_bytes, language_code="en-IN", vendor_id="vendor-123"
        )

        assert result is not None
        assert result["transcription"]["text"] == "Two kilos of tomatoes for fifty rupees"
        assert result["extracted_transaction"]["item_name"] == "tomatoes"

    def test_process_voice_transaction_different_formats(self, voice_service):
        """Test voice transaction processing with different audio formats."""
        formats = ["mp3", "wav", "flac", "ogg"]

        for fmt in formats:
            # Mock S3 upload
            voice_service.s3_client.upload_file = Mock(return_value=f"s3://bucket/audio.{fmt}")

            # Mock transcription job
            voice_service.transcribe_client.start_transcription_job = Mock(return_value="job-123")
            voice_service.transcribe_client.get_transcription_result = Mock(
                return_value={
                    "text": "Test transcription",
                    "confidence": 0.90,
                    "transcript_uri": "https://example.com/transcript.json",
                }
            )
            voice_service.transcribe_client.delete_transcription_job = Mock(return_value=True)

            # Mock Bedrock extraction
            voice_service.bedrock_client.extract_transaction = Mock(
                return_value={
                    "item_name": "test",
                    "quantity": 1.0,
                    "unit": "kg",
                    "price": 10.0,
                    "extracted_successfully": True,
                }
            )

            # Process transaction
            audio_bytes = b"fake audio data"
            result = voice_service.process_voice_transaction(
                audio_bytes=audio_bytes,
                language_code="en-IN",
                vendor_id="vendor-123",
                media_format=fmt,
            )

            assert result is not None
            # Verify S3 upload was called with correct content type
            call_args = voice_service.s3_client.upload_file.call_args
            assert fmt in call_args[1]["key"]

    def test_get_mock_transcription_result_hindi(self, voice_service):
        """Test mock transcription result for Hindi."""
        result = voice_service._get_mock_transcription_result("hi-IN")

        assert result is not None
        assert result["transcription"]["text"] == "दो किलो टमाटर पचास रुपये"
        assert result["transcription"]["confidence"] == 0.85
        assert result["extracted_transaction"]["item_name"] == "टमाटर"
        assert result["extracted_transaction"]["quantity"] == 2.0

    def test_get_mock_transcription_result_english(self, voice_service):
        """Test mock transcription result for English."""
        result = voice_service._get_mock_transcription_result("en-IN")

        assert result is not None
        assert result["transcription"]["text"] == "Two kilos of tomatoes for fifty rupees"
        assert result["transcription"]["confidence"] == 0.85
        assert result["extracted_transaction"]["item_name"] == "tomatoes"
        assert result["extracted_transaction"]["quantity"] == 2.0

    def test_process_voice_transaction_exception_handling(self, voice_service):
        """Test voice transaction processing handles exceptions gracefully."""
        # Mock S3 upload to raise exception
        voice_service.s3_client.upload_file = Mock(side_effect=Exception("S3 error"))

        audio_bytes = b"fake audio data"
        result = voice_service.process_voice_transaction(
            audio_bytes=audio_bytes, language_code="hi-IN", vendor_id="vendor-123"
        )

        assert result is None

    def test_process_voice_transaction_exception_demo_mode(self, voice_service):
        """Test voice transaction processing returns mock data on exception in demo mode."""
        with patch.object(Config, "DEMO_MODE", True):
            # Mock S3 upload to raise exception
            voice_service.s3_client.upload_file = Mock(side_effect=Exception("S3 error"))

            audio_bytes = b"fake audio data"
            result = voice_service.process_voice_transaction(
                audio_bytes=audio_bytes, language_code="hi-IN", vendor_id="vendor-123"
            )

            # Should return mock data in demo mode
            assert result is not None
            assert result["transcription"]["confidence"] == 0.85
