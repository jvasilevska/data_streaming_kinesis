import json
import time
from botocore.exceptions import ClientError

class KinesisClient:
    def __init__(self, kinesis_client, stream_name, logger):
        self.kinesis_client = kinesis_client
        self.name = stream_name
        self.logger = logger

    def put_records_into_stream(self, data, partition_key):
        for record in data:
            try:
                self.kinesis_client.put_record(
                    StreamName=self.name,
                    Data=json.dumps(record),
                    PartitionKey=partition_key)
                self.logger.info("Put record in stream {}.".format(self.name))
            except ClientError as error:
                self.logger.error(error)

    def wait_for_active_stream(self):
        while True:
            try:
                result = self.kinesis_client.describe_stream_summary(StreamName=self.name)
            except ClientError as error:
                self.logger.error(error)
                return False
            status = result['StreamDescriptionSummary']['StreamStatus']
            if status == 'ACTIVE':
                return True
            if status == 'DELETING':
                self.logger.error('Kinesis stream {} is being deleted.'.format(self.name))
                return False
            time.sleep(5)
