"""
이미지 처리와 관련된 유틸 함수
"""
import base64
import io
import os
import uuid
import boto3
from fastapi import HTTPException
from dotenv import load_dotenv
load_dotenv()

def create_s3_client():
    """S3 클라이언트 생성"""
    return boto3.client(
        's3',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name='ap-northeast-2'
    )

def upload_image_to_s3(base64_string: str, s3_client) -> str:
    """
    Base64 이미지를 S3에 업로드하고 URL 반환
    """
    try:
        bucket_name = 'balm-bucket'

        # base64 디코딩
        if 'base64,' in base64_string:
            image_data = base64_string.split('base64,')[1]
        else:
            image_data = base64_string
        image_bytes = base64.b64decode(image_data)
        # S3에 업로드
        file_id = str(uuid.uuid4())
        key = f"images/user/{file_id}.jpg"
        s3_client.upload_fileobj(
            io.BytesIO(image_bytes),
            bucket_name,
            key,
            ExtraArgs={
                'ContentType': 'image/jpeg',
                'CacheControl': 'max-age=31536000'
            }
        )
        return f"https://{bucket_name}.s3.ap-northeast-2.amazonaws.com/{key}"
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}") from e
