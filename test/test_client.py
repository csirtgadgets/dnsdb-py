
import pytest
import os
from csirtg_dnsdb.client import Client
from csirtg_dnsdb.exceptions import QuotaLimit

DISABLE_TESTS = True
if os.environ.get('FARSIGHT_TOKEN'):
    DISABLE_TESTS = False


def test_client():
    c = Client(token='1234')
    assert c


@pytest.mark.skipif(DISABLE_TESTS, reason='need to set FARSIGHT_TOKEN to run')
def test_standard_rrname_search_live():
    c = Client()

    try:
        r = c.search('google.com', limit=5)
        assert len(list(r)) > 0
    except QuotaLimit:
        pass

def test_standard_rrname_search_mocked():
    c = Client()

    try:
        list(c.search('google.com', limit=5))
        assert c.__dict__['last_request'].endswith('/lookup/rrset/name/google.com')
    except QuotaLimit:
        pass


@pytest.mark.skipif(DISABLE_TESTS, reason='need to set FARSIGHT_TOKEN to run')
def test_standard_rdata_search_live():
    c = Client()

    try:
        r = c.search('8.8.8.8', limit=5)
        assert len(list(r)) > 0
    except QuotaLimit:
        pass
 

def test_standard_rdata_search_mocked():
    c = Client()

    try:
        list(c.search('8.8.8.8', limit=5))
        assert c.__dict__['last_request'].endswith('/lookup/rdata/ip/8.8.8.8')
    except QuotaLimit:
        pass
    
@pytest.mark.skipif(DISABLE_TESTS, reason='need to set FARSIGHT_TOKEN to run')
def test_keyword_rrname_search_live():
    c = Client()

    try:
        r = c.search('google.com', search_type='keyword', limit=5)
        assert len(list(r)) > 0
    except QuotaLimit:
        pass


def test_keyword_rrname_search_mocked():
    c = Client()

    try:
        list(c.search('google.com', search_type='keyword', limit=5))
        assert c.__dict__['last_request'].endswith('/glob/rrnames/*google.com*')
    except QuotaLimit:
        pass

@pytest.mark.skipif(DISABLE_TESTS, reason='need to set FARSIGHT_TOKEN to run')
def test_keyword_rdata_search_live():
    c = Client()

    try:
        r = c.search('9.9.9.', search_type='keyword', limit=5)
        assert len(list(r)) > 0
    except QuotaLimit:
        pass

def test_keyword_rdata_search_mocked():
    c = Client()

    try:
        list(c.search('9.9.9.', search_type='keyword', limit=5))
        assert c.__dict__['last_request'].endswith('/glob/rdata/*9.9.9.*')
    except QuotaLimit:
        pass


@pytest.mark.skipif(DISABLE_TESTS, reason='need to set FARSIGHT_TOKEN to run')
def test_globbing_rdata_search_live():
    c = Client()

    try:
        r = c.search('9.*.9.*', limit=5, search_type='glob')
        assert len(list(r)) > 0
    except QuotaLimit:
        pass


def test_globbing_rdata_search_mocked():
    c = Client()

    try:
        list(c.search('9.*.9.*', limit=5, search_type='glob'))
        assert c.__dict__['last_request'].endswith('/glob/rdata/9.*.9.*')
    except QuotaLimit:
        pass

@pytest.mark.skipif(DISABLE_TESTS, reason='need to set FARSIGHT_TOKEN to run')
def test_globbing_rrname_search_live():
    c = Client()

    try:
        r = c.search('*.google.com*', limit=5, search_type='glob')
        assert len(list(r)) > 0
    except QuotaLimit:
        pass


def test_globbing_rrname_search_mocked():
    c = Client()

    try:
        list(c.search('.google.com', limit=5, search_type='glob'))
        assert c.__dict__['last_request'].endswith('/glob/rrnames/.google.com')
    except QuotaLimit:
        pass


@pytest.mark.skipif(DISABLE_TESTS, reason='need to set FARSIGHT_TOKEN to run')
def test_regex_rrname_search_live():
    c = Client()

    try:
        r = c.search(r'.*\.google\.com\.', limit=5, search_type='regex')
        assert len(list(r)) > 0
    except QuotaLimit:
        pass


def test_regex_rrname_search_mocked():
    c = Client()

    try:
        list(c.search(r'.*\.google\.com\.', limit=5, search_type='regex'))
        assert c.__dict__['last_request'].endswith(r'/regex/rrnames/.*\.google\.com\.')
    except QuotaLimit:
        pass

@pytest.mark.skipif(DISABLE_TESTS, reason='need to set FARSIGHT_TOKEN to run')
def test_regex_rdata_search_live():
    c = Client()

    try:
        r = c.search(r'1\.1\.1\.1', limit=5, search_type='regex')
        assert len(list(r)) > 0
    except QuotaLimit:
        pass


def test_regex_rdata_search_mocked():
    c = Client()

    try:
        list(c.search(r'1\.1\.1\.1', limit=5, search_type='regex'))
        assert c.__dict__['last_request'].endswith(r'/regex/rdata/1\.1\.1\.1')
    except QuotaLimit:
        pass