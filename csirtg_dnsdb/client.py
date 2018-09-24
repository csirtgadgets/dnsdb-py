#!/usr/bin/env python

import os
from . import VERSION
import logging
from argparse import ArgumentParser, RawDescriptionHelpFormatter
import textwrap
import requests
from .exceptions import QuotaLimit
try:
    import ujson as json
except ImportError:
    import json
import socket

logger = logging.getLogger(__name__)

REMOTE = os.environ.get('FARSIGHT_REMOTE', 'https://api.dnsdb.info')
TOKEN = os.environ.get('FARSIGHT_TOKEN')


class Client(object):

    def __init__(self, token=TOKEN, remote=REMOTE, limit=None, **kwargs):
        self.remote = remote
        self.token = token
        self.limit = limit

        self.session = requests.session()
        self.session.headers['User-Agent'] = "csirtg-dnsdb-py/{0}".format(VERSION)
        self.session.headers['X-Api-Key'] = self.token
        self.session.headers['Accept'] = 'application/json'

    def search(self, i, limit=None):
        params = {}

        if limit:
            params['limit'] = limit

        path = '/rdata/ip'
        try:
            socket.inet_aton(i)
        except:
            if '/' in i:
                i = i.replace('/', ',')
            else:
                path = '/rrset/name'

        path = '{}/lookup{}/{}'.format(self.remote, path, i)
        r = self.session.get(path, params=params, stream=True)

        if r.status_code == 200:
            for line in r.iter_lines():
                if not line:
                    continue

                yield (json.loads(line.decode('utf-8')))

        if r.status_code == 429:
            raise QuotaLimit('API quota reached..')


def main():

    p = ArgumentParser(
        description=textwrap.dedent('''\
            example usage:
                $ dnsdb -q 1.2.3.4
            '''),
        formatter_class=RawDescriptionHelpFormatter,
        prog='dnsdb',
    )
    p.add_argument('--token', help='specify api token', default=TOKEN)
    p.add_argument('--search', '-q', help='search for something')
    args = p.parse_args()

    c = Client(token=args.token)

    for r in c.search(args.search):
        print(json.dumps(r))


if __name__ == "__main__":
    main()
