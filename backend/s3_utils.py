import boto3
import os
from botocore.exceptions import ClientError
from fastapi import HTTPException

def get_s3_client():
    return boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
        region_name=os.getenv('AWS_REGION', 'us-east-1')
    )

async def upload_to_s3(file, order_id: str, filename: str):
    try:
        s3_client = get_s3_client()
        
        # Generate unique S3 key
        file_extension = filename.split('.')[-1].lower()
        s3_key = f"uploads/{order_id}/{filename}"
        
        # Upload file to S3
        s3_client.upload_fileobj(
            file.file,
            os.getenv('S3_BUCKET'),
            s3_key,
            ExtraArgs={
                'ContentType': get_content_type(file_extension),
                'Metadata': {
                    'original-filename': filename,
                    'order-id': order_id,
                    'upload-time': '2024-10-07T00:00:00Z'  # You'd use actual datetime
                }
            }
        )
        
        return s3_key
        
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"S3 upload failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

def get_content_type(extension: str) -> str:
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
        'vtt': 'text/vtt'
    }
    return content_types.get(extension, 'application/octet-stream')

def generate_presigned_url(s3_key: str, expiration: int = 3600):
    try:
        s3_client = get_s3_client()
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': os.getenv('S3_BUCKET'),
                'Key': s3_key
            },
            ExpiresIn=expiration
        )
        return url
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate download URL: {str(e)}")
