import unittest
from unittest.mock import patch
from data_stream_generator import main

class DataStreamGeneratorTestCase(unittest.TestCase):

    @patch( 'libs.s3_client')
    @patch('libs.kinesis_client')
    @patch( 'logging.getLogger')
    def test_main_will_put_records(self, s3_client, kinesis_client, logger):
        kinesis_client.wait_for_active_stream.return_value = True
        kinesis_client.name = 'test'

        s3_client.get_data.return_value = []

        main(s3_client, kinesis_client, logger, 'partition_key')

        logger.info.assert_called_with('Kinesis stream test is active')
        s3_client.get_data.assert_called_with()
        kinesis_client.put_records_into_stream.assert_called_with([], 'partition_key')


    @patch( 'libs.s3_client')
    @patch('libs.kinesis_client')
    @patch( 'logging.getLogger')
    def test_main_will_not_put_records(self, s3_client, kinesis_client, logger):
        kinesis_client.wait_for_active_stream.return_value = False
        kinesis_client.name = 'test'

        main(s3_client, kinesis_client, logger, 'partition_key')

        logger.error.assert_called_with('Kinesis stream test is not active')
