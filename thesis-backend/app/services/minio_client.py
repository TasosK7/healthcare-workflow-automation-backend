from minio import Minio
import os

minio_client = Minio(
    endpoint=os.getenv("MINIO_ENDPOINT", "localhost:9000"),
    access_key=os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
    secret_key=os.getenv("MINIO_SECRET_KEY", "minioadmin"),
    secure=False,
)

BUCKET_NAME = os.getenv("MINIO_BUCKET", "lab-tests")

# Ensure bucket exists
if not minio_client.bucket_exists(BUCKET_NAME):
    minio_client.make_bucket(BUCKET_NAME)
