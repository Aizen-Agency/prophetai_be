import boto3
import os
from botocore.exceptions import ClientError
from datetime import datetime, timedelta

class S3Service:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION')
        )
        self.bucket_name = os.getenv('S3_BUCKET_NAME')

    def upload_file(self, file_path, object_name=None):
        """
        Upload a file to S3 bucket
        :param file_path: Path to the file to upload
        :param object_name: S3 object name. If not specified, file_path is used
        :return: True if file was uploaded, else False
        """
        if object_name is None:
            object_name = os.path.basename(file_path)

        try:
            self.s3_client.upload_file(file_path, self.bucket_name, object_name)
            return True
        except ClientError as e:
            print(f"Error uploading file to S3: {e}")
            return False

    def get_presigned_url(self, object_name, expiration=3600):
        """
        Generate a presigned URL to share an S3 object
        :param object_name: S3 object name
        :param expiration: Time in seconds for the presigned URL to remain valid
        :return: Presigned URL as string. If error, returns None.
        """
        try:
            response = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': object_name
                },
                ExpiresIn=expiration
            )
            return response
        except ClientError as e:
            print(f"Error generating presigned URL: {e}")
            return None

    def get_object_url(self, object_name):
        """
        Get the public URL for an S3 object
        :param object_name: S3 object name
        :return: Public URL as string
        """
        return f"https://{self.bucket_name}.s3.{os.getenv('AWS_REGION')}.amazonaws.com/{object_name}"

# Create a singleton instance
s3_service = S3Service()
