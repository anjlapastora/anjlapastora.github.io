# storage_backends.py
from storages.backends.s3boto3 import S3Boto3Storage


class SupabaseStorage(S3Boto3Storage):
    def url(self, name):
        return f"https://zxmttxrnkldjhzdrnbzx.supabase.co/storage/v1/object/public/{self.bucket_name}/{name}"
