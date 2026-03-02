"""
S3 client for Smart Vendors application.

Provides file upload, download, and presigned URL generation.
"""

import logging
from typing import Optional

import boto3
from botocore.exceptions import ClientError

from ..config import Config

logger = logging.getLogger(__name__)


class S3Client:
    """
    S3 client for file storage operations.

    Handles file uploads, downloads, and presigned URL generation.
    """

    def __init__(self):
        """Initialize S3 client."""
        try:
            self.s3_client = boto3.client("s3", region_name=Config.AWS_REGION)
            logger.info(f"S3 client initialized for region {Config.AWS_REGION}")
        except Exception as e:
            logger.error(f"Failed to initialize S3 client: {e}")
            raise

    def upload_file(
        self, file_bytes: bytes, bucket: str, key: str, content_type: Optional[str] = None
    ) -> Optional[str]:
        """
        Upload file to S3 bucket.

        Args:
            file_bytes: File content as bytes
            bucket: Target S3 bucket name
            key: S3 object key
            content_type: Optional content type

        Returns:
            S3 URI if successful, None otherwise
        """
        try:
            extra_args = {}
            if content_type:
                extra_args["ContentType"] = content_type

            self.s3_client.put_object(Bucket=bucket, Key=key, Body=file_bytes, **extra_args)

            s3_uri = f"s3://{bucket}/{key}"
            logger.info(f"Successfully uploaded file to {s3_uri}")
            return s3_uri
        except ClientError as e:
            logger.error(f"Error uploading file to S3: {e}")
            return None

    def download_file(self, bucket: str, key: str) -> Optional[bytes]:
        """
        Download file from S3 bucket.

        Args:
            bucket: S3 bucket name
            key: S3 object key

        Returns:
            File content as bytes if successful, None otherwise
        """
        try:
            response = self.s3_client.get_object(Bucket=bucket, Key=key)
            return response["Body"].read()
        except ClientError as e:
            logger.error(f"Error downloading file from S3: {e}")
            return None

    def generate_presigned_url(
        self, bucket: str, key: str, expiration: int = 3600
    ) -> Optional[str]:
        """
        Generate presigned URL for S3 object.

        Args:
            bucket: S3 bucket name
            key: S3 object key
            expiration: URL expiration time in seconds (default: 1 hour)

        Returns:
            Presigned URL if successful, None otherwise
        """
        try:
            url = self.s3_client.generate_presigned_url(
                "get_object", Params={"Bucket": bucket, "Key": key}, ExpiresIn=expiration
            )
            return url
        except ClientError as e:
            logger.error(f"Error generating presigned URL: {e}")
            return None

    def delete_file(self, bucket: str, key: str) -> bool:
        """
        Delete file from S3 bucket.

        Args:
            bucket: S3 bucket name
            key: S3 object key

        Returns:
            True if successful, False otherwise
        """
        try:
            self.s3_client.delete_object(Bucket=bucket, Key=key)
            logger.info(f"Successfully deleted s3://{bucket}/{key}")
            return True
        except ClientError as e:
            logger.error(f"Error deleting file from S3: {e}")
            return False
