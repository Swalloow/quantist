from typing import List

import boto3
from boto3.dynamodb.conditions import Key


class DynamoDBHandler(object):
    # TODO: Make dynamoDB abstract handler
    def __init__(self, table_name: str):
        self.dynamodb = boto3.resource('dynamodb', 'ap-northeast-2')
        self.table = self.dynamodb.Table(table_name)

    def get_table_metadata(self):
        """
        Get some metadata about chosen table.
        """
        return {
            'num_items': self.table.item_count,
            'primary_key_name': self.table.key_schema[0],
            'status': self.table.table_status,
            'bytes_size': self.table.table_size_bytes,
            'global_secondary_indices': self.table.global_secondary_indexes
        }

    def get_item_by_key(self, name: str, date: str) -> List[dict]:
        """
        Get single item by key string.
        """
        response = self.table.get_item(
            Key={'name': name, 'date': date})
        # TODO: Custom error handling
        return response['Item']

    def get_price_by_date(self, name: str, start_date: str, end_date: str) -> List[dict]:
        """
        Perform a query operation on the table.
        Can specify filter_key (col name) and its value to be filtered.
        """
        key_exp = Key('name').eq(name) & Key('date').between(start_date, end_date)
        response = self.table.query(
            KeyConditionExpression=key_exp,
            ProjectionExpression="#nm, #dt, #clo",
            ExpressionAttributeNames={"#nm": "name", "#dt": "date", "#clo": "close"})
        return response['Items']

    def get_baseline(self, name: str, start_date: str, end_date: str) -> List[dict]:
        """
        Get baseline index by key string
        """
        key_exp = Key('name').eq(name) & Key('date').between(start_date, end_date)
        response = self.table.query(
            KeyConditionExpression=key_exp,
            ProjectionExpression='#nm, #dt, #pr',
            ExpressionAttributeNames={"#nm": "name", "#dt": "date", "#pr": "price"})
        return response['Items']

    def get_stock_master(self):
        self.table = 'master'
        response = self.table.scan()
        return response['Items']
