import unittest
import base64
import json
from lambdas.mappers.event_mapper import EventMapper
from unittest.mock import patch

class EventMapperTestCase(unittest.TestCase):

    def test_json_to_csv_row_customer_registered(self):
        data = {
            "name": "Test",
            "aggregate_id": "agg-id",
            "id": "1",
            "type": "customer_registered",
            "timestamp": "timestamp",
            "data":{"name":["Test"], "birthdate": "2000-01-01"}
        }
        self.assertEqual(
            ('1,agg-id,customer_registered,timestamp,Test,2000-01-01,\n').encode('utf-8'),
            EventMapper.json_to_csv_row(data)
        )

    def test_json_to_csv_row_product_ordered(self):
        data = {
            "name": "Test",
            "aggregate_id": "agg-id",
            "id": "1",
            "type": "product_ordered",
            "timestamp": "timestamp",
            "data":{"name":"test", "birthdate": "2000-01-01"}
        }
        self.assertEqual(
            ('1,agg-id,product_ordered,timestamp,,,test\n').encode('utf-8'),
            EventMapper.json_to_csv_row(data)
        )

    def test_json_to_csv_row_other(self):
        data = {
            "name": "Test",
            "aggregate_id": "agg-id",
            "id": "1",
            "type": "other",
            "timestamp": "timestamp",
            "data":{"name":"test", "birthdate": "2000-01-01"}
        }
        self.assertEqual(
            ('1,agg-id,other,timestamp,,,\n').encode('utf-8'),
            EventMapper.json_to_csv_row(data)
        )