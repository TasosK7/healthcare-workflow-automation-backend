from minio import Minio
import os
from datetime import timedelta

BUCKET_NAME = os.getenv("MINIO_BUCKET", "lab-tests")

minio_client = Minio(
    endpoint="localhost:9000",
    access_key=os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
    secret_key=os.getenv("MINIO_SECRET_KEY", "minioadmin"),
    secure=False,
)


# Ensure bucket exists
if not minio_client.bucket_exists(BUCKET_NAME):
    minio_client.make_bucket(BUCKET_NAME)

def generate_presigned_url(object_name: str, expires_in_seconds: int = 300) -> str:
    return minio_client.presigned_get_object(
        bucket_name=BUCKET_NAME,
        object_name=object_name,
        expires=timedelta(seconds=expires_in_seconds)
    )