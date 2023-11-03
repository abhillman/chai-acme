import gzip
import urllib.parse
import urllib.request

from gscholar import logging
from gscholar.query.abstract import Abstract

log = logging.make_logger()

class Backend:
    """
    This is a backend of type `GScholar`.  This abstraction is helpful as it enables
    fetching the "raw" results of a given query against Google Scholar. This enables
    the ability for the main binary to merely print raw results out as opposed to
    going through the entire flow of fetching results over the network and also printing
    them, which is especially useful for auditing output and testing.
    """
    def __init__(self) -> None:
        pass

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
    def _fetch_page(uri, headers=BASE_HEADERS) -> str:
        log.info(f"{uri}")
        log.debug(f"{headers}")

        request = urllib.request.Request(uri, headers=headers)

        gzip_bytes = None
        with urllib.request.urlopen(request) as response:
            # TODO: assert that the data is actually gzip
            gzip_bytes = response.read()

        return gzip.decompress(gzip_bytes).decode()

    @staticmethod
    def html(query: type[Abstract]):
        """
        Fetches the HTML for the given query by going out to network. Note that this
        is not a "cheap" method as it goes out to network.
        """
        # TODO(@abhillman): look into using async
        uri = query.as_uri()
        return Backend._fetch_page(uri)

# TODO(@abhillman): lot of thoughts here regarding python and "pure" types
