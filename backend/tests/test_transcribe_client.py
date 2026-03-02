"""
Tests for AWS Transcribe client.

Tests voice transcription functionality with mock AWS services.
"""

import json
import pytest
from unittest.mock import Mock, patch, MagicMock
from moto import mock_transcribe, mock_s3
import boto3

from shared.aws.transcribe_client import TranscribeClient
from shared.config import Config


@pytest.fixture
def transcribe_client():
    """Create TranscribeClient instance for testing."""
    with mock_transcribe():
        client = TranscribeClient()
        yield client


@pytest.fixture
def mock_transcript_response():
    """Mock transcript JSON response from AWS Transcribe."""
    return {
        "results": {
            "transcripts": [{"transcript": "दो किलो टमाटर पचास रुपये"}],
            "items": [
                {
                    "type": "pronunciation",
                    "alternatives": [{"confidence": "0.95", "content": "दो"}],
                },
                {
                    "type": "pronunciation",
                    "alternatives": [{"confidence": "0.90", "content": "किलो"}],
                },
                {
                    "type": "pronunciation",
                    "alternatives": [{"confidence": "0.85", "content": "टमाटर"}],
                },
                {
                    "type": "pronunciation",
                    "alternatives": [{"confidence": "0.88", "content": "पचास"}],
                },
                {
                    "type": "pronunciation",
                    "alternatives": [{"confidence": "0.92", "content": "रुपये"}],
                },
            ],
        }
    }


class TestTranscribeClient:
    """Test suite for TranscribeClient."""

    def test_initialization(self, transcribe_client):
        """Test TranscribeClient initializes correctly."""
        assert transcribe_client is not None
        assert transcribe_client.transcribe_client is not None

    def test_start_transcription_job_success(self, transcribe_client):
        """Test starting transcription job successfully."""
        with patch.object(
            transcribe_client.transcribe_client, "start_transcription_job"
        ) as mock_start:
            mock_start.return_value = {}

            job_name = transcribe_client.start_transcription_job(
                job_name="test-job", s3_uri="s3://bucket/audio.mp3", language_code="hi-IN"
            )

            assert job_name == "test-job"
            mock_start.assert_called_once()

    def test_start_transcription_job_unsupported_language(self, transcribe_client):
        """Test starting transcription job with unsupported language."""
        job_name = transcribe_client.start_transcription_job(
            job_name="test-job", s3_uri="s3://bucket/audio.mp3", language_code="fr-FR"
        )

        assert job_name is None

    def test_start_transcription_job_with_different_formats(self, transcribe_client):
        """Test starting transcription job with different audio formats."""
        formats = ["mp3", "wav", "flac", "ogg"]

        for fmt in formats:
            with patch.object(
                transcribe_client.transcribe_client, "start_transcription_job"
            ) as mock_start:
                mock_start.return_value = {}

                job_name = transcribe_client.start_transcription_job(
                    job_name=f"test-job-{fmt}",
                    s3_uri=f"s3://bucket/audio.{fmt}",
                    language_code="en-IN",
                    media_format=fmt,
                )

                assert job_name == f"test-job-{fmt}"

    def test_get_transcription_result_completed(self, transcribe_client, mock_transcript_response):
        """Test getting completed transcription result."""
        with patch.object(transcribe_client.transcribe_client, "get_transcription_job") as mock_get:
            with patch("urllib.request.urlopen") as mock_urlopen:
                # Mock the job status response
                mock_get.return_value = {
                    "TranscriptionJob": {
                        "TranscriptionJobStatus": "COMPLETED",
                        "Transcript": {"TranscriptFileUri": "https://example.com/transcript.json"},
                    }
                }

                # Mock the transcript JSON fetch
                mock_response = MagicMock()
                mock_response.read.return_value = json.dumps(mock_transcript_response).encode()
                mock_response.__enter__.return_value = mock_response
                mock_response.__exit__.return_value = None
                mock_urlopen.return_value = mock_response

                result = transcribe_client.get_transcription_result("test-job")

                assert result is not None
                assert result["text"] == "दो किलो टमाटर पचास रुपये"
                assert 0.0 <= result["confidence"] <= 1.0
                assert result["transcript_uri"] == "https://example.com/transcript.json"

    def test_get_transcription_result_failed(self, transcribe_client):
        """Test getting failed transcription result."""
        with patch.object(transcribe_client.transcribe_client, "get_transcription_job") as mock_get:
            mock_get.return_value = {
                "TranscriptionJob": {
                    "TranscriptionJobStatus": "FAILED",
                    "FailureReason": "Audio quality too low",
                }
            }

            result = transcribe_client.get_transcription_result("test-job")

            assert result is None

    def test_get_transcription_result_failed_demo_mode(self, transcribe_client):
        """Test getting failed transcription result in demo mode returns mock data."""
        with patch.object(Config, "DEMO_MODE", True):
            with patch.object(
                transcribe_client.transcribe_client, "get_transcription_job"
            ) as mock_get:
                mock_get.return_value = {
                    "TranscriptionJob": {
                        "TranscriptionJobStatus": "FAILED",
                        "FailureReason": "Audio quality too low",
                    }
                }

                result = transcribe_client.get_transcription_result("test-job")

                assert result is not None
                assert result["text"] == "दो किलो टमाटर पचास रुपये"
                assert result["confidence"] == 0.85

    def test_get_transcription_result_timeout(self, transcribe_client):
        """Test transcription job timeout."""
        with patch.object(transcribe_client.transcribe_client, "get_transcription_job") as mock_get:
            mock_get.return_value = {"TranscriptionJob": {"TranscriptionJobStatus": "IN_PROGRESS"}}

            result = transcribe_client.get_transcription_result("test-job", max_wait_seconds=1)

            assert result is None

    def test_delete_transcription_job_success(self, transcribe_client):
        """Test deleting transcription job successfully."""
        with patch.object(
            transcribe_client.transcribe_client, "delete_transcription_job"
        ) as mock_delete:
            mock_delete.return_value = {}

            success = transcribe_client.delete_transcription_job("test-job")

            assert success is True
            mock_delete.assert_called_once_with(TranscriptionJobName="test-job")

    def test_delete_transcription_job_failure(self, transcribe_client):
        """Test deleting transcription job failure."""
        with patch.object(
            transcribe_client.transcribe_client, "delete_transcription_job"
        ) as mock_delete:
            from botocore.exceptions import ClientError

            mock_delete.side_effect = ClientError(
                {"Error": {"Code": "ResourceNotFoundException"}}, "delete_transcription_job"
            )

            success = transcribe_client.delete_transcription_job("test-job")

            assert success is False


class TestTranscribeClientLanguageSupport:
    """Test language support for transcription."""

    def test_supported_languages(self, transcribe_client):
        """Test that both Hindi and English are supported."""
        supported_languages = ["hi-IN", "en-IN"]

        for lang in supported_languages:
            with patch.object(
                transcribe_client.transcribe_client, "start_transcription_job"
            ) as mock_start:
                mock_start.return_value = {}

                job_name = transcribe_client.start_transcription_job(
                    job_name=f"test-job-{lang}", s3_uri="s3://bucket/audio.mp3", language_code=lang
                )

                assert job_name is not None


class TestTranscribeClientErrorHandling:
    """Test error handling in TranscribeClient."""

    def test_quota_exceeded_error(self, transcribe_client):
        """Test handling of quota exceeded error."""
        with patch.object(
            transcribe_client.transcribe_client, "start_transcription_job"
        ) as mock_start:
            from botocore.exceptions import ClientError

            mock_start.side_effect = ClientError(
                {"Error": {"Code": "LimitExceededException"}}, "start_transcription_job"
            )

            job_name = transcribe_client.start_transcription_job(
                job_name="test-job", s3_uri="s3://bucket/audio.mp3", language_code="hi-IN"
            )

            assert job_name is None

    def test_conflict_error(self, transcribe_client):
        """Test handling of conflict error (job already exists)."""
        with patch.object(
            transcribe_client.transcribe_client, "start_transcription_job"
        ) as mock_start:
            from botocore.exceptions import ClientError

            mock_start.side_effect = ClientError(
                {"Error": {"Code": "ConflictException"}}, "start_transcription_job"
            )

            job_name = transcribe_client.start_transcription_job(
                job_name="test-job", s3_uri="s3://bucket/audio.mp3", language_code="hi-IN"
            )

            assert job_name is None
