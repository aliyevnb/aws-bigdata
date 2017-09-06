#!/env python

import sys
import boto3
import argparse

def getConnected(region):
    session = boto3.Session(region_name=region)
    clientResource = session.resource('dynamodb')
    return clientResource

def createTable(tName, conn):
    myTable = conn.create_table(
        TableName = tName,
        AttributeDefinitions = [
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
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 1
        },
    )
    return myTable.table_status

def deleteTable(tName, conn):
    myTable = conn.delete_table(
        TableName = tName
    )
    return myTable.table_status

if __name__ == '__main__':
    # Let's do some argument parsing for this application
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(help='Available commans')

    # Parse create command arguments
    create_parser = subparser.add_parser('create', help='Create a DynamoDB table')
    create_parser.add_argument('create_tn', help = 'Please specify DynamoDB table name')

    # Parse delete command arguments
    delete_parser = subparser.add_parser('delete', help='Delete a DynamoDB table')
    delete_parser.add_argument('delete_tn', help = 'Please specify DynamoDB table name')

    # Key
    key_parser = subparser.add_parser('key', help='Specify keys')

    # Always ask for a region
    parser.add_argument('--region', required=True, dest='region', help='Specify AWS region')

    # aggregate parsed commands
    args = parser.parse_args()

    '''
    start parsing arguments.
    make sure region was provided to establish connection with service
    '''
    if args.region:
        conn = getConnected(args.region)

        if args.create_tn:
            ddbTable = createTable(args.create_tn, conn)
            if ddbTable == 'CREATING':
                print('Creating DynamoDB Table %s in %s' % (args.create_tn, args.region))
            else:
                print('Something went wrong...')
        elif args.delete_tn:
            ddbTable = deleteTable(args.delete_tn, conn)
            if ddbTable == 'DELETING':
                print('Deleting DynamoDB table %s in %s' % (args.delete_tn, args.region))
        else:
            sys.exit('Please provide action. Available actions {create|delete}')
