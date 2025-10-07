import boto3
import os
from botocore.exceptions import ClientError
from fastapi import HTTPException
import uuid

def get_s3_client():
    """Initialize and return S3 client"""
    try:
        return boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
            region_name=os.getenv('AWS_REGION', 'us-east-1')
        )
    except Exception as e:
        print(f"⚠️ S3 client initialization failed: {e}")
        return None

async def upload_file_to_s3(file, order_id: str, original_filename: str):
    """Upload file to S3 and return S3 key"""
    try:
        s3_client = get_s3_client()
        if not s3_client:
            raise HTTPException(status_code=500, detail="S3 service unavailable")

        # Generate unique S3 key
        file_extension = original_filename.split('.')[-1].lower()
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        s3_key = f"uploads/{order_id}/{unique_filename}"

        # Get file size
        file.file.seek(0, 2)  # Seek to end
        file_size = file.file.tell()
        file.file.seek(0)  # Reset to beginning

        # Upload to S3
        s3_client.upload_fileobj(
            file.file,
            os.getenv('S3_BUCKET'),
            s3_key,
            ExtraArgs={
                'ContentType': get_content_type(file_extension),
                'Metadata': {
                    'original-filename': original_filename,
                    'order-id': order_id
                }
            }
        )

        return {
            "s3_key": s3_key,
            "file_size": file_size,
            "file_type": file_extension
        }

    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"S3 upload failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

def get_content_type(extension: str) -> str:
    """Map file extension to content type"""
    content_types = {
        'mp4': 'video/mp4',
        'mov': 'video/quicktime',
        'avi': 'video/x-msvideo',
        'mp3': 'audio/mpeg',
        'wav': 'audio/wav',
        'txt': 'text/plain',
        'doc': 'application/msword',
        'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'srt': 'application/x-subrip',
        'vtt': 'text/vtt',
        'pdf': 'application/pdf'
    }
    return content_types.get(extension, 'application/octet-stream')

def generate_download_url(s3_key: str, expiration: int = 3600):
    """Generate pre-signed URL for file download"""
    try:
        s3_client = get_s3_client()
        if not s3_client:
            return None

        url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': os.getenv('S3_BUCKET'),
                'Key': s3_key
            },
            ExpiresIn=expiration
        )
        return url
    except ClientError:
        return None
