from __future__ import print_function

import logging
import base64
import json
from mappers.event_mapper import EventMapper


def lambda_handler(event, context):
    output = []
    logging.basicConfig(level=logging.DEBUG,
        format='%(levelname)s: %(asctime)s: %(message)s')
    logger = logging.getLogger(__name__)
    for record in event['records']:
        logger.info(record)
        payload = base64.b64decode(record['data']).decode("utf-8")
        logger.info(payload)

        csv_row = EventMapper.json_to_csv_row(json.loads(payload))

        output_record = {
          'recordId': record['recordId'],
          'result': 'Ok',
          'data': base64.b64encode(csv_row)
        }

        logger.info(output_record)

        output.append(output_record)

    logger.info('Successfully processed {} records.'.format(len(event['records'])))
    return {'records': output}
