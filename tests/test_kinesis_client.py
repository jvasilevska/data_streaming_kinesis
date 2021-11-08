import unittest
import json
from unittest.mock import patch, Mock
from libs.kinesis_client import KinesisClient
from botocore.exceptions import ClientError

def get_mocked_boto_kinesis_put_record_error():
    mocked_client = Mock()
    mocked_client.put_record.side_effect = Mock(side_effect=ClientError({}, 'test'))

    return mocked_client

def get_mocked_boto_kinesis_active():
    mocked_client = Mock()
    mocked_client.describe_stream_summary.return_value = {
        'StreamDescriptionSummary': {
            'StreamStatus': 'ACTIVE'
        }
    }

    return mocked_client

def get_mocked_boto_kinesis_deleting():
    mocked_client = Mock()
    mocked_client.describe_stream_summary.return_value = {
        'StreamDescriptionSummary': {
            'StreamStatus': 'DELETING'
        }
    }

    return mocked_client

def get_mocked_boto_kinesis_error():
    mocked_client = Mock()
    mocked_client.describe_stream_summary.side_effect = Mock(side_effect=ClientError({}, 'test'))

    return mocked_client

class KinesisClientTestCase(unittest.TestCase):

    @patch( 'boto3.client')
    @patch( 'logging.getLogger')
    def test_put_records_into_stream_will_log_record(self, boto3, logger):
        kinesis_client = KinesisClient(boto3, 'stream_name', logger)
        kinesis_client.put_records_into_stream([{'key': 'value'}], 'key')


        logger.info.assert_called_with('Put record in stream stream_name.')

        boto3.put_record.assert_called_with(
            StreamName='stream_name',
            Data=json.dumps({'key': 'value'}),
            PartitionKey='key'
        )
    
    @patch( 'logging.getLogger')
    def test_put_records_into_stream_will_log_error(self, logger):
        boto3 = get_mocked_boto_kinesis_put_record_error()

        kinesis_client = KinesisClient(boto3, 'stream_name', logger)
        kinesis_client.put_records_into_stream([{'key': 'value'}], 'key')

        self.assertTrue(logger.error.called)

    @patch( 'logging.getLogger')
    def test_wait_for_active_stream_will_return_true(self, logger):
        boto3 = get_mocked_boto_kinesis_active()

        kinesis_client = KinesisClient(boto3, 'stream_name', logger)
        self.assertTrue(kinesis_client.wait_for_active_stream())

    @patch( 'logging.getLogger')
    def test_wait_for_active_stream_will_return_false_on_deleted_stream(self, logger):
        boto3 = get_mocked_boto_kinesis_deleting()

        kinesis_client = KinesisClient(boto3, 'stream_name', logger)
        self.assertFalse(kinesis_client.wait_for_active_stream())

    @patch( 'logging.getLogger')
    def test_wait_for_active_stream_will_return_false_on_error(self, logger):
        boto3 = get_mocked_boto_kinesis_error()

        kinesis_client = KinesisClient(boto3, 'stream_name', logger)

        self.assertFalse(kinesis_client.wait_for_active_stream())
        self.assertTrue(logger.error.called)

