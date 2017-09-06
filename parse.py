#!env python

import argparse
import sys

class CmdParse(object):
    def __init__(self):
        parser = argparse.ArgumentParser(
            description = 'Some text',
            usage = '''Provide program usage here
            ''')
        parser.add_argument('command', help = 'Subcommand to run')
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self,args.command):
            parser.print_help()
            exit(1)

    def create(self):
        parser = argparse.ArgumentParser(
            description = 'Create something')
    
    def delete(self):
        parser = argparse.ArgumentParser(
            description = 'Delete something')


class RegConn(object):
    def __init__(self, region):
        session = boto3.Session(region_name = region)
        ddbt = session.resource('dynamodb')


if __name__ == '__main__':
