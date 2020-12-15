#!/usr/bin/env python

import os
import string
from . import VERSION
import logging
from argparse import ArgumentParser, Action, ArgumentError, RawDescriptionHelpFormatter
import textwrap
import requests
from .exceptions import DNSDBException, QuotaLimit
try:
    import ujson as json
except ImportError:
    import json
import socket

logger = logging.getLogger(__name__)

REMOTE = os.environ.get('FARSIGHT_REMOTE', 'https://api.dnsdb.info/dnsdb/v2')
TOKEN = os.environ.get('FARSIGHT_TOKEN')


class Client(object):

    def __init__(self, token=TOKEN, remote=REMOTE, **kwargs):
        self.remote = remote
        self.token = token
        self.last_request = ''

        self.session = requests.session()
        self.session.headers['User-Agent'] = "csirtg-dnsdb-py/{0}".format(VERSION)
        self.session.headers['X-Api-Key'] = self.token
        self.session.headers['Accept'] = 'application/jsonl'

        self.PREFIX_MAP = {
            'standard': 'lookup',
            'keyword': 'glob',
            'glob': 'glob',
            'regex': 'regex'
        }

    def search(self, i, search_type='standard', limit=5000):
        params = {}

        if limit:
            params['limit'] = limit

        if search_type == 'standard':
            path = '/rdata'
            try:
                socket.inet_aton(i)
                path += '/ip'
            except:
                if '/' in i:
                    i = i.replace('/', ',')
                path = '/rrset/name'

        else:
            # if we strip out all punc and are only left with nums, we prob want rdata. bad assumption?
            if i.translate(str.maketrans('', '', string.punctuation)).isnumeric():
                path = '/rdata'
            else:
                path = '/rrnames'

            if search_type == 'keyword':
                # if the our first char of our keyword query is a not a wildcard, prepend a wildcard
                if i[0] is not '*':
                    i = '*' + i
                # everybody gets a wildcard at the end for keyword 'cuz that's how dnsdb scout seems to do it
                i += '*'

        # TODO: implement rtype options. atm, gets back any. pytests will need to be fixed for .endswith
        # i += '/ANY'
                
        endpoint = self.PREFIX_MAP[search_type]
        path = '{}/{}{}/{}'.format(self.remote, endpoint, path, i)
        self.last_request = path

        r = self.session.get(path, params=params, stream=True)

        if r.status_code == 200:
            lines = r.iter_lines()
            first = next(lines).decode('utf-8')
            if first != '{"cond":"begin"}':
                raise DNSDBException('Unusual response received: {}'.format(first))

            for line in lines:
                if not line:
                    continue
                
                line_dec = json.loads(line.decode('utf-8')).get('obj')
                if line_dec:
                    yield (line_dec)

        if r.status_code == 429:
            raise QuotaLimit('API quota reached..')

class check_limit(Action):
    def __call__(self, parser, namespace, limit, option_string=None):
        if not 1 <= limit <= 100000:
            raise ArgumentError(self, 'limit must be 1 - 100,000')
        setattr(namespace, self.dest, limit)


def main():

    p = ArgumentParser(
        description=textwrap.dedent('''\
            example usage:
                $ dnsdb -q 1.2.3.4
            '''),
        formatter_class=RawDescriptionHelpFormatter,
        prog='dnsdb',
    )
    p.add_argument('--token', help='specify api token (default pulls from FARSIGHT_TOKEN envvar)', default=TOKEN)
    p.add_argument('--search', '-q', help='search for something')
    p.add_argument('--search-type', '-t', choices=('standard', 'keyword', 'glob', 'regex'), nargs='?', const='standard', dest='type',
        help='specify a search type (default is standard)', default='standard'
    )
    p.add_argument('--limit', '-l', type=int, metavar=('(1-100000)'), action=check_limit, nargs='?', const=5000, 
        help='max number of results to return (default of 5000)', default=5000
    )
    args = p.parse_args()

    c = Client(token=args.token)

    for r in c.search(i=args.search, search_type=args.type, limit=args.limit):
        ignore_resps = [ '{"cond":"succeeded"', '{"cond":"limited","msg":"Result limit reached"}' ]
        if r not in ignore_resps:
            print(json.dumps(r))


if __name__ == "__main__":
    main()
