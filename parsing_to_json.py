#!env python

import argparse
import json

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', dest='wcu')
    parser.add_argument('-r', dest='rcu')

    args=parser.parse_args()

    print(args)

    adict = vars(args)
    print(adict)

    if args.wcu and args.rcu:
        with ('file1.tmp', 'w') as afile:
            json.dump(['ProvisionedThroughput',{'ReadCapacityUnits':args.wcu,'WriteCapacityUnits':args.rcu}], sort_keys=True, indent=4, afile)
