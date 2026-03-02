"""
Unit tests for S3 client.

Tests S3 file upload, download, presigned URL generation, and error handling.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from botocore.exceptions import ClientError

from shared.aws.s3_client import S3Client


class TestS3Client:
    """Test suite for S3Client."""

    @patch("shared.aws.s3_client.boto3.client")
    def test_s3_client_initialization(self, mock_boto_client):
        """Test S3 client initializes successfully."""
        mock_s3 = Mock()
        mock_boto_client.return_value = mock_s3

        client = S3Client()

        assert client.s3_client is not None
        mock_boto_client.assert_called_once()

    @patch("shared.aws.s3_client.boto3.client")
    def test_upload_file_success(self, mock_boto_client):
        """Test successful file upload to S3."""
        mock_s3 = Mock()
        mock_boto_client.return_value = mock_s3

        client = S3Client()
        file_bytes = b"test content"
        bucket = "test-bucket"
        key = "test-key.txt"

        result = client.upload_file(file_bytes, bucket, key)

        assert result == f"s3://{bucket}/{key}"
        mock_s3.put_object.assert_called_once_with(Bucket=bucket, Key=key, Body=file_bytes)

    @patch("shared.aws.s3_client.boto3.client")
    def test_upload_file_with_content_type(self, mock_boto_client):
        """Test file upload with content type."""
        mock_s3 = Mock()
        mock_boto_client.return_value = mock_s3

        client = S3Client()
        file_bytes = b"test content"
        bucket = "test-bucket"
        key = "test-image.jpg"
        content_type = "image/jpeg"

        result = client.upload_file(file_bytes, bucket, key, content_type)

        assert result == f"s3://{bucket}/{key}"
        mock_s3.put_object.assert_called_once_with(
            Bucket=bucket, Key=key, Body=file_bytes, ContentType=content_type
        )

    @patch("shared.aws.s3_client.boto3.client")
    def test_upload_file_error(self, mock_boto_client):
        """Test file upload error handling."""
        mock_s3 = Mock()
        mock_s3.put_object.side_effect = ClientError(
            {"Error": {"Code": "AccessDenied", "Message": "Access Denied"}}, "PutObject"
        )
        mock_boto_client.return_value = mock_s3

        client = S3Client()
        result = client.upload_file(b"test", "bucket", "key")

        assert result is None

    @patch("shared.aws.s3_client.boto3.client")
    def test_download_file_success(self, mock_boto_client):
        """Test successful file download from S3."""
        mock_s3 = Mock()
        mock_response = {"Body": Mock()}
        mock_response["Body"].read.return_value = b"downloaded content"
        mock_s3.get_object.return_value = mock_response
        mock_boto_client.return_value = mock_s3

        client = S3Client()
        result = client.download_file("bucket", "key")

        assert result == b"downloaded content"
        mock_s3.get_object.assert_called_once_with(Bucket="bucket", Key="key")

    @patch("shared.aws.s3_client.boto3.client")
    def test_download_file_error(self, mock_boto_client):
        """Test file download error handling."""
        mock_s3 = Mock()
        mock_s3.get_object.side_effect = ClientError(
            {"Error": {"Code": "NoSuchKey", "Message": "Key not found"}}, "GetObject"
        )
        mock_boto_client.return_value = mock_s3

        client = S3Client()
        result = client.download_file("bucket", "key")

        assert result is None

    @patch("shared.aws.s3_client.boto3.client")
    def test_generate_presigned_url_success(self, mock_boto_client):
        """Test presigned URL generation."""
        mock_s3 = Mock()
        expected_url = "https://bucket.s3.amazonaws.com/key?signature=xyz"
        mock_s3.generate_presigned_url.return_value = expected_url
        mock_boto_client.return_value = mock_s3

        client = S3Client()
        result = client.generate_presigned_url("bucket", "key", expiration=3600)

        assert result == expected_url
        mock_s3.generate_presigned_url.assert_called_once_with(
            "get_object", Params={"Bucket": "bucket", "Key": "key"}, ExpiresIn=3600
        )

    @patch("shared.aws.s3_client.boto3.client")
    def test_generate_presigned_url_custom_expiration(self, mock_boto_client):
        """Test presigned URL with custom expiration."""
        mock_s3 = Mock()
        expected_url = "https://bucket.s3.amazonaws.com/key?signature=abc"
        mock_s3.generate_presigned_url.return_value = expected_url
        mock_boto_client.return_value = mock_s3

        client = S3Client()
        result = client.generate_presigned_url("bucket", "key", expiration=7200)

        assert result == expected_url
        mock_s3.generate_presigned_url.assert_called_once_with(
            "get_object", Params={"Bucket": "bucket", "Key": "key"}, ExpiresIn=7200
        )

    @patch("shared.aws.s3_client.boto3.client")
    def test_generate_presigned_url_error(self, mock_boto_client):
        """Test presigned URL generation error handling."""
        mock_s3 = Mock()
        mock_s3.generate_presigned_url.side_effect = ClientError(
            {"Error": {"Code": "AccessDenied", "Message": "Access Denied"}}, "GeneratePresignedUrl"
        )
        mock_boto_client.return_value = mock_s3

        client = S3Client()
        result = client.generate_presigned_url("bucket", "key")

        assert result is None

    @patch("shared.aws.s3_client.boto3.client")
    def test_delete_file_success(self, mock_boto_client):
        """Test successful file deletion."""
        mock_s3 = Mock()
        mock_boto_client.return_value = mock_s3

        client = S3Client()
        result = client.delete_file("bucket", "key")

        assert result is True
        mock_s3.delete_object.assert_called_once_with(Bucket="bucket", Key="key")

    @patch("shared.aws.s3_client.boto3.client")
    def test_delete_file_error(self, mock_boto_client):
        """Test file deletion error handling."""
        mock_s3 = Mock()
        mock_s3.delete_object.side_effect = ClientError(
            {"Error": {"Code": "AccessDenied", "Message": "Access Denied"}}, "DeleteObject"
        )
        mock_boto_client.return_value = mock_s3

        client = S3Client()
        result = client.delete_file("bucket", "key")

        assert result is False
