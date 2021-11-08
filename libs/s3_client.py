import json
from botocore.exceptions import ClientError

class S3Client:
    def __init__(self, s3_client, bucket_name, logger):
        self.s3_client = s3_client
        self.bucket_name = bucket_name
        self.logger = logger

    def get_data(self):
        json_data = None
        try:
            bucket = self.s3_client.Bucket(self.bucket_name)
            for obj in bucket.objects.all():
                body = obj.get()['Body'].read()
                json_data=json.loads(body)
            return json_data
        except ClientError as error:
            self.logger.error(error)
        return json_data
