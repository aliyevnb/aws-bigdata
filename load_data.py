#!env python

import boto3
import json
import decimal
import argparse

def loadData(region, my_table, my_source):
    session = boto3.Session(region_name = region)
    client = session.resource('dynamodb')

    ddbt = client.Table(my_table)

    with open(my_source) as json_file:
        movies = json.load(json_file, parse_float = decimal.Decimal)
        for movie in movies:
            year = int(movie['year'])
            title = movie['title']
            info = movie['info']

            print('Adding movie: ', year, title)

            ddbt.put_item(
                Item = {
                    'year': year,
                    'title': title,
                    'info': info,
                }
            )

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--region', dest='region', required=True, help='Specify region where you want to create table')
    parser.add_argument('--table', dest='table', required=True, help='Specify table name')
    parser.add_argument('--source', dest='src', required=True, help='Specify source JSON file')
    args = parser.parse_args()

    if args.region:
        result = loadData(args.region,args.table,args.src)
