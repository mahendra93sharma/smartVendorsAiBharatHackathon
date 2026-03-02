"""
Property-based tests for voice transcription.

Feature: hackathon-deliverables, Property 3: Voice transcription for supported languages
**Validates: Requirements 5.1**

Tests that voice transcription works correctly for any valid audio file in Hindi or English.
"""

import pytest
from hypothesis import given, strategies as st, settings, HealthCheck
from unittest.mock import Mock, patch
import io

from shared.aws.transcribe_client import TranscribeClient
from shared.services.voice_service import VoiceService
from shared.config import Config


# Custom strategies for generating test data
@st.composite
def audio_file_strategy(draw):
    """
    Generate mock audio file data.

    Returns a tuple of (audio_bytes, media_format, language_code)
    """
    # Generate audio duration between 1 and 60 seconds
    duration_seconds = draw(st.integers(min_value=1, max_value=60))

    # Select supported language
    language_code = draw(st.sampled_from(Config.TRANSCRIBE_LANGUAGE_CODES))

    # Select supported media format
    media_format = draw(st.sampled_from(["mp3", "wav", "flac", "ogg"]))

    # Generate small mock audio bytes (just enough to be non-empty)
    # We don't need realistic audio data for property testing
    audio_bytes = draw(st.binary(min_size=100, max_size=1000))

    return {
        "audio_bytes": audio_bytes,
        "media_format": media_format,
        "language_code": language_code,
        "duration_seconds": duration_seconds,
    }


@st.composite
def transcription_response_strategy(draw, language_code: str):
    """
    Generate mock transcription response data.

    Args:
        language_code: Language code for the transcription

    Returns:
        Mock transcription response dict
    """
    # Generate confidence score between 0.0 and 1.0
    confidence = draw(st.floats(min_value=0.0, max_value=1.0))

    # Generate sample text based on language
    if language_code == "hi-IN":
        sample_texts = [
            "दो किलो टमाटर पचास रुपये",
            "तीन किलो आलू साठ रुपये",
            "एक किलो प्याज तीस रुपये",
            "पांच किलो टमाटर सौ रुपये",
        ]
    else:  # en-IN
        sample_texts = [
            "Two kilos of tomatoes for fifty rupees",
            "Three kilos of potatoes for sixty rupees",
            "One kilo of onions for thirty rupees",
            "Five kilos of tomatoes for hundred rupees",
        ]

    text = draw(st.sampled_from(sample_texts))

    return {
        "text": text,
        "confidence": confidence,
        "transcript_uri": f"https://example.com/transcript-{draw(st.uuids())}.json",
    }


class TestVoiceTranscriptionProperty:
    """Property-based tests for voice transcription functionality."""

    @pytest.mark.property
    @settings(
        max_examples=100,
        deadline=None,
        suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.data_too_large],
    )
    @given(audio_data=audio_file_strategy())
    def test_voice_transcription_returns_valid_result(self, audio_data):
        """
        Property: Voice transcription for any valid audio file returns valid result.

        **Validates: Requirements 5.1**

        For any valid audio file in Hindi or English:
        - Transcription should return text (non-empty string)
        - Confidence score should be between 0.0 and 1.0
        - Language should be correctly identified (hi-IN or en-IN)
        """
        with patch("shared.services.voice_service.TranscribeClient") as MockTranscribeClient:
            with patch("shared.services.voice_service.BedrockClient"):
                with patch("shared.services.voice_service.S3Client") as MockS3Client:
                    # Setup mocks
                    voice_service = VoiceService()

                    # Mock S3 upload
                    s3_uri = f"s3://bucket/audio-{audio_data['duration_seconds']}.{audio_data['media_format']}"
                    voice_service.s3_client.upload_file = Mock(return_value=s3_uri)

                    # Generate mock transcription response based on language
                    if audio_data["language_code"] == "hi-IN":
                        text = "दो किलो टमाटर पचास रुपये"
                    else:
                        text = "Two kilos of tomatoes for fifty rupees"

                    transcription_response = {
                        "text": text,
                        "confidence": 0.85,
                        "transcript_uri": "https://example.com/transcript.json",
                    }

                    # Mock transcription job
                    job_name = f"job-{audio_data['duration_seconds']}"
                    voice_service.transcribe_client.start_transcription_job = Mock(
                        return_value=job_name
                    )
                    voice_service.transcribe_client.get_transcription_result = Mock(
                        return_value=transcription_response
                    )
                    voice_service.transcribe_client.delete_transcription_job = Mock(
                        return_value=True
                    )

                    # Mock Bedrock extraction
                    voice_service.bedrock_client.extract_transaction = Mock(
                        return_value={
                            "item_name": "test_item",
                            "quantity": 1.0,
                            "unit": "kg",
                            "price": 50.0,
                            "extracted_successfully": True,
                        }
                    )

                    # Process voice transaction
                    result = voice_service.process_voice_transaction(
                        audio_bytes=audio_data["audio_bytes"],
                        language_code=audio_data["language_code"],
                        vendor_id="test-vendor",
                        media_format=audio_data["media_format"],
                    )

                    # Verify result is not None
                    assert result is not None, "Voice transcription should return a result"

                    # Verify transcription structure
                    assert "transcription" in result, "Result should contain transcription"
                    transcription = result["transcription"]

                    # Property 1: Transcription returns text (non-empty string)
                    assert "text" in transcription, "Transcription should contain text field"
                    assert isinstance(transcription["text"], str), "Text should be a string"
                    assert len(transcription["text"]) > 0, "Text should not be empty"

                    # Property 2: Confidence score is between 0.0 and 1.0
                    assert (
                        "confidence" in transcription
                    ), "Transcription should contain confidence field"
                    assert isinstance(
                        transcription["confidence"], (int, float)
                    ), "Confidence should be numeric"
                    assert (
                        0.0 <= transcription["confidence"] <= 1.0
                    ), f"Confidence score {transcription['confidence']} should be between 0.0 and 1.0"

                    # Property 3: Language is correctly identified
                    # Verify the transcription was called with the correct language
                    voice_service.transcribe_client.start_transcription_job.assert_called_once()
                    call_args = voice_service.transcribe_client.start_transcription_job.call_args
                    assert (
                        call_args[1]["language_code"] == audio_data["language_code"]
                    ), f"Language code should be {audio_data['language_code']}"

    @pytest.mark.property
    @settings(
        max_examples=100, deadline=None, suppress_health_check=[HealthCheck.function_scoped_fixture]
    )
    @given(
        language_code=st.sampled_from(Config.TRANSCRIBE_LANGUAGE_CODES),
        confidence=st.floats(min_value=0.0, max_value=1.0),
    )
    def test_transcription_confidence_bounds(self, language_code, confidence):
        """
        Property: Transcription confidence is always within valid bounds.

        **Validates: Requirements 5.1**

        For any transcription result, the confidence score must be between 0.0 and 1.0.
        """
        with patch("shared.aws.transcribe_client.boto3.client"):
            transcribe_client = TranscribeClient()

            # Mock the transcription result with the given confidence
            with patch.object(
                transcribe_client.transcribe_client, "get_transcription_job"
            ) as mock_get:
                with patch("urllib.request.urlopen") as mock_urlopen:
                    # Create mock transcript response
                    transcript_data = {
                        "results": {
                            "transcripts": [{"transcript": "test text"}],
                            "items": [
                                {
                                    "type": "pronunciation",
                                    "alternatives": [
                                        {"confidence": str(confidence), "content": "test"}
                                    ],
                                }
                            ],
                        }
                    }

                    mock_get.return_value = {
                        "TranscriptionJob": {
                            "TranscriptionJobStatus": "COMPLETED",
                            "Transcript": {
                                "TranscriptFileUri": "https://example.com/transcript.json"
                            },
                        }
                    }

                    import json
                    from unittest.mock import MagicMock

                    mock_response = MagicMock()
                    mock_response.read.return_value = json.dumps(transcript_data).encode()
                    mock_response.__enter__.return_value = mock_response
                    mock_response.__exit__.return_value = None
                    mock_urlopen.return_value = mock_response

                    result = transcribe_client.get_transcription_result("test-job")

                    # Verify confidence is within bounds
                    assert result is not None
                    assert (
                        0.0 <= result["confidence"] <= 1.0
                    ), f"Confidence {result['confidence']} must be between 0.0 and 1.0"

    @pytest.mark.property
    @settings(
        max_examples=100, deadline=None, suppress_health_check=[HealthCheck.function_scoped_fixture]
    )
    @given(language_code=st.sampled_from(Config.TRANSCRIBE_LANGUAGE_CODES))
    def test_supported_languages_accepted(self, language_code):
        """
        Property: All supported languages are accepted for transcription.

        **Validates: Requirements 5.1**

        For any supported language code (hi-IN, en-IN), the transcription job should start successfully.
        """
        with patch("shared.aws.transcribe_client.boto3.client"):
            transcribe_client = TranscribeClient()

            with patch.object(
                transcribe_client.transcribe_client, "start_transcription_job"
            ) as mock_start:
                mock_start.return_value = {}

                job_name = transcribe_client.start_transcription_job(
                    job_name=f"test-job-{language_code}",
                    s3_uri="s3://bucket/audio.mp3",
                    language_code=language_code,
                )

                # Verify job was started successfully
                assert job_name is not None, f"Job should start for language {language_code}"
                assert job_name == f"test-job-{language_code}"

                # Verify the correct language code was passed
                mock_start.assert_called_once()
                call_args = mock_start.call_args
                assert call_args[1]["LanguageCode"] == language_code

    @pytest.mark.property
    @settings(
        max_examples=50, deadline=None, suppress_health_check=[HealthCheck.function_scoped_fixture]
    )
    @given(
        media_format=st.sampled_from(["mp3", "wav", "flac", "ogg", "amr", "webm"]),
        language_code=st.sampled_from(Config.TRANSCRIBE_LANGUAGE_CODES),
    )
    def test_supported_audio_formats(self, media_format, language_code):
        """
        Property: All supported audio formats are accepted for transcription.

        **Validates: Requirements 5.1**

        For any supported audio format, the transcription job should start successfully.
        """
        with patch("shared.aws.transcribe_client.boto3.client"):
            transcribe_client = TranscribeClient()

            with patch.object(
                transcribe_client.transcribe_client, "start_transcription_job"
            ) as mock_start:
                mock_start.return_value = {}

                job_name = transcribe_client.start_transcription_job(
                    job_name=f"test-job-{media_format}",
                    s3_uri=f"s3://bucket/audio.{media_format}",
                    language_code=language_code,
                    media_format=media_format,
                )

                # Verify job was started successfully
                assert job_name is not None, f"Job should start for format {media_format}"

                # Verify the correct media format was passed
                mock_start.assert_called_once()
                call_args = mock_start.call_args
                assert call_args[1]["MediaFormat"] == media_format.lower()
