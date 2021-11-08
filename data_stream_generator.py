import configparser
import logging
import boto3
from libs.s3_client import S3Client
from libs.kinesis_client import KinesisClient


def main(s3_client_obj, kinesis_client_obj, logger_obj, partition_key):
    logger_obj.info('Waiting for new stream {} to become active...'.format(kinesis_client_obj.name))
    if not kinesis_client_obj.wait_for_active_stream():
        logger_obj.error('Kinesis stream {} is not active'.format(kinesis_client_obj.name))
        return
    logger_obj.info('Kinesis stream {} is active'.format(kinesis_client_obj.name))

    data = s3_client_obj.get_data()
    kinesis_client_obj.put_records_into_stream(data, partition_key)


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')

    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s: %(asctime)s: %(message)s')
    logger = logging.getLogger(__name__)


    boto_s3 = boto3.resource('s3', aws_access_key_id=config['aws_access']['access_key'],
                      aws_secret_access_key=config['aws_access']['secret_key'])
    s3_client = S3Client(boto_s3, config['s3_access']['bucket_name'], logger)


    boto_kinesis = boto3.client('kinesis', aws_access_key_id=config['aws_access']['access_key'],
                      aws_secret_access_key=config['aws_access']['secret_key'])
    kinesis_client = KinesisClient(boto_kinesis, config['kinesis_stream']['stream_name'], logger)


    main(s3_client, kinesis_client, logger, "type")
