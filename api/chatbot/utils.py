import boto3
import os
import uuid
from botocore.exceptions import ClientError
from typing import Optional
from datetime import datetime
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile

aws_access_key_id = os.environ.get("AWS_BEDROCK_ACCESS_KEY_ID")
aws_secret_access_key = os.environ.get("AWS_BEDROCK_SECRET_ACCESS_KEY")
bucket_name = "nugibot-cdn-storage"

s3_client = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name="ap-southeast-1",
)


def handle_image_upload(
    image_file: InMemoryUploadedFile | TemporaryUploadedFile, user_id: str
) -> str:
    """
    Handle image upload to AWS S3 from Django request file

    Args:
        image_file: Django uploaded file object (from request.FILES)
        user_id: User ID for file path organization

    Returns:
        str: S3 URL of the uploaded file

    Raises:
        Exception: If upload fails
    """
    try:
        # Generate a unique filename with proper path
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        file_extension = image_file.name.split(".")[-1].lower()

        # Structure: users/{user_id}/images/{timestamp}_{unique_id}.{extension}
        s3_key = f"users/{user_id}/images/{timestamp}_{unique_id}.{file_extension}"

        # Upload file to S3
        s3_client.upload_fileobj(
            image_file,
            bucket_name,
            s3_key,
            ExtraArgs={"ContentType": image_file.content_type, "ACL": "private"},
        )

        return s3_key

    except ClientError as e:
        print(f"AWS S3 Error: {str(e)}")
        raise Exception("Failed to upload image to S3")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise Exception("Failed to process image upload")


def generate_presigned_url(s3_path: str, expiration: int = 3600) -> Optional[str]:
    """
    Generate a presigned URL for a specific path in S3

    Args:
        s3_path (str): The full path to the object in S3 (e.g., 'folder/subfolder/file.jpg')
        expiration (int): URL expiration time in seconds (default: 1 hour)
        bucket_name (str): Optional bucket name, defaults to bucket_name

    Returns:
        str: Presigned URL or None if generation fails
    """
    try:
        # Generate the presigned URL
        url = s3_client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": bucket_name, "Key": s3_path},
            ExpiresIn=expiration,
            HttpMethod="GET",  # You can specify 'PUT' for upload URLs
        )

        return url

    except ClientError as e:
        print(f"Error generating presigned URL: {str(e)}")
        return None


def check_s3_file_exists(s3_path: str) -> bool:
    try:
        s3_client = boto3.client("s3")
        s3_client.head_object(Bucket=bucket_name, Key=s3_path)
        return True
    except ClientError:
        return False
