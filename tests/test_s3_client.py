import unittest
import json
from unittest.mock import patch, Mock
from libs.s3_client import S3Client
from botocore.exceptions import ClientError

def get_mocked_boto_s3_error():
    mocked_client = Mock()
    mocked_client.Bucket.side_effect = Mock(side_effect=ClientError({}, 'test'))

    return mocked_client

class S3ClientTestCase(unittest.TestCase):

    @patch( 'logging.getLogger')
    @patch( 'boto3.resource')
    def test_get_data_will_call_s3(self, logger, boto3):
        s3_client = S3Client(boto3, 'bucket_name', logger)
        s3_client.get_data()

        boto3.Bucket.assert_called_with('bucket_name')

    @patch( 'logging.getLogger')
    def test_get_data_will_log_error(self, logger):
        boto3 = get_mocked_boto_s3_error()

        s3_client = S3Client(boto3,  'bucket_name', logger)

        s3_client.get_data()
        self.assertTrue(logger.error.called)