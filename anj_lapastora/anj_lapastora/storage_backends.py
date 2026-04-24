from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    bucket_name = "media"  # must match your Supabase bucket
    default_acl = "public-read"
    file_overwrite = False
    custom_domain = False  # IMPORTANT for Supabase

    def get_available_name(self, name, max_length=None):
        # prevents weird overwrite issues
        return super().get_available_name(name, max_length)
