import gzip
import urllib.parse
import urllib.request

from . import logging
from .parser import Parser
from .query import Simple
from .query.abstract import Abstract

log = logging.make_logger()

class GScholar:
    def __init__(self, query: type[Abstract]) -> None:
        self.query = query
        # self.state = {}

    # Headers sent by a recent version of Safari in incognito on scholar.google.com
    BASE_HEADERS = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Host": "scholar.google.com",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    }

    @staticmethod
    def _fetch_page(uri, headers=BASE_HEADERS):
        log.info(f"{uri}")
        log.debug(f"{headers}")

        request = urllib.request.Request(uri, headers=headers)

        gzip_bytes = None
        with urllib.request.urlopen(request) as response:
            # TODO: assert that the data is actually gzip
            gzip_bytes = response.read()

        return gzip.decompress(gzip_bytes).decode()

    def results(self):
        uri = self.query.as_uri()
        html = self._fetch_page(uri)
        return Parser.parse_results(html)

    @staticmethod
    def simple_query(query_text):
        simple_query = Simple(query_text)
        return GScholarWrapped(simple_query)

class GScholarWrapped(GScholar):
    """
    Allows for `with` keyword to be used, but only on a fresh instance of `GScholar`
    """
    def __enter__(self):
        return self

    def __exit__(self, *args):
        # We don't deal with args, which tell of an exception;
        # thus we return `False` which will instruct python to
        # raise an exception for us, had one occurred.
        return False
