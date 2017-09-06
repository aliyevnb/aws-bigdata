#!env python

import boto3
import argparse

def getService(region):
    ddb_client = boto3.client('dynamodb', region_name=region)
    return ddb_client

def create_table(client,t_name,rcu,wcu):
    table_out = client.create_table(
        TableName=t_name,
        AttributeDefinitions=[
            {
                'AttributeName': 'year',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'title',
                'AttributeType': 'S'
            },
        ],
        KeySchema=[
            {
                'AttributeName': 'year',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'title',
                'KeyType': 'RANGE'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': int(rcu),
            'WriteCapacityUnits': int(wcu) 
        },
    )
    return table_out.table_status

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--region', dest='region', help='Specify region where you want to create table')
    parser.add_argument('--table', dest='table', help='Specify table name')
    parser.add_argument('--wcu', dest='wcu', help='Specify WCU for your new table')
    parser.add_argument('--rcu', dest='rcu', help='Specify RCU for your new table')
    args = parser.parse_args()

    if args.region:
        getClient = getService(region)

        result=create_table(args.region,args.table, args.rcu, args.wcu)
        if result == 'CREATING':
            print('Creating DynamoDB table %s in %s region' % (args.table, args.region))
        else:
            print('Something went wrong...')
