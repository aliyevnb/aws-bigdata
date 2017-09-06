from __future__ import print_function
import boto3
import json

DDBT_REPLICA = '[replica-table]'
client = boto3.client('dynamodb', region_name = '[aws-region]')

def lambda_handler(event, context):
    for record in event['Records']:
        if record['eventName'] == 'INSERT' or record['eventName'] == 'MODIFY':
            client.put_item(TableName = DDBT_REPLICA, Item = record['dynamodb']['NewImage'])
        elif record['eventName'] == 'REMOVE':
            client.delete_item(TableName = DDBT_REPLICA, Key = record['dynamodb']['Keys'])

    return 'Successfully processed {} records.'.format(len(event['Records']))
