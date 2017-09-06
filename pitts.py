#!env python

import sys
import time
import boto3
import argparse

def getStream(region):
    # Connect to service
    ksc = boto3.client('kinesis', region_name=region)
    return ksc

def streamStat(conn, sName):
    # Get kenesis stream status
    stat = conn.describe_stream(StreamName = sName)['StreamDescription']['StreamStatus']
    return stat

def wait_for_stream(conn, sName):
    # Verify KS status is active, we can not write to stream if it's not active
    SLEEP_TIME = 3
    stat = streamStat(conn, sName)
    while stat != 'ACTIVE':
        print('%s is not ready for ops, sleeping for %s seconds' % (sName, SLEEP_TIME))
        time.sleep(SLEEP_TIME)
        stat = streamStat(conn, sName)

def put_to_stream(conn, sName, pWords):
    # start pushing data to the stream
    for w in pWords:
        conn.put_record(StreamName = sName, Data = w, PartitionKey = w)
        print('Added %s to stream %s' % (w, sName))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', dest='strnm', required=True, help='Specify the Kinesis Stream name')
    parser.add_argument('-w', dest='wrd', required=True, action='append', help='A word add to a stream')
    parser.add_argument('--region', dest='region', required=True, help='Specify region name')

    args = parser.parse_args()

    if args.region:
        conn = getStream(args.region)

    try:
        status = streamStat(conn,args.strnm)

        if status == 'DELETING':
            sys.exit('Stream is being deleted and cannot be used!')
        else:
            wait_for_stream(conn, args.strnm)
    except:
        print('%s stream does not exist. Creating...' %args.strnm)
        conn.create_stream(StreamName = args.strnm,
                           ShardCount=1)
        wait_for_stream(conn, args.strnm)

    if args.wrd:
        put_to_stream(conn, args.strnm, args.wrd)
    else:
        print('Oooops')
