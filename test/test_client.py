
import pytest
import os
from csirtg_dnsdb.client import Client
from csirtg_dnsdb.exceptions import QuotaLimit

DISABLE_TESTS = True
if os.environ.get('FARSIGHT_TOKEN'):
    DISABLE_TESTS = False


def test_client():
    c = Client(token='1234')


@pytest.mark.skipif(DISABLE_TESTS, reason='need to set FARSIGHT_TOKEN to run')
def test_client_live():
    c = Client()

    try:
        r = c.search('172.217.6.206')
        assert len(list(r)) > 0
    except QuotaLimit:
        pass

    try:
        r = c.search('google.com')
        assert len(list(r)) > 0
    except QuotaLimit:
        pass


