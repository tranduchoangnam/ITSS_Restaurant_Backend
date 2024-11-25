import logging

import boto3
from botocore.exceptions import ClientError

from backend.core.config import settings
from backend.utils import get_filename_from_cdn_url


class S3Service:
    def __init__(self):
        self.bucket_name = settings.BUCKET_NAME
        self.s3_client = self.get_s3_client()

    def get_s3_client(self):
        return boto3.client("s3")

    def generate_presigned_url(self, object_name: str, expiration=3600):
        try:
            response_url = self.s3_client.generate_presigned_url(
                "put_object",
                Params={
                    "Bucket": self.bucket_name,
                    "Key": object_name,
                },
                ExpiresIn=expiration,
            )
            return response_url
        except ClientError as e:
            print(e)
            return None

    def move_file_from_tmp(self, path: str):
        try:
            tmp_filename = get_filename_from_cdn_url(path)
            if not tmp_filename:
                return path
            if not tmp_filename.startswith(settings.MEDIA_PATH_TMP_PREFIX):
                return path
            destination_key = tmp_filename.removeprefix(settings.MEDIA_PATH_TMP_PREFIX)
            copy_source = {"Bucket": self.bucket_name, "Key": tmp_filename}
            self.s3_client.copy_object(
                CopySource=copy_source, Bucket=self.bucket_name, Key=destination_key
            )
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=tmp_filename)
            return settings.PUBLIC_CDN_URL + destination_key
        except ClientError as e:
            logging.error(f"Error with S3 move_file_from_tmp: {str(e)}")
            return path
