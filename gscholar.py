from abc import ABC, abstractmethod  # https://docs.python.org/3/library/abc.html
import enum
import gzip
import json
import lxml.etree
import urllib.parse
import urllib.request
import sys


class GScholarQuery(ABC):
    """
    Example query:
      https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=chimichanga&btnG=
    """

    BASE_URI = "https://scholar.google.com"
    DEFAULT_ENDPOINT = "scholar"
    COMMON_PARAMS = {
        "hl": "en",
        "as_sdt": "=0,5",
    }

    @abstractmethod
    def _query_parameters(self):
        pass

    def as_uri(self, endpoint="/scholar", additional_params={}):
        params = {
            **self._query_parameters(),
            **GScholarQuery.COMMON_PARAMS,
            **additional_params,
        }
        encoded_params = urllib.parse.urlencode(
            params, quote_via=urllib.parse.quote_plus
        )
        return "".join(
            [
                GScholarQuery.BASE_URI,
                "/",
                GScholarQuery.DEFAULT_ENDPOINT,
                "?",
                encoded_params,
            ]
        )


class GScholarQuerySimple(GScholarQuery):
    def __init__(self, query):
        self.query = query

    def _query_parameters(self):
        return {"q": self.query}


class GScholar:
    def __init__(self, query: type[GScholarQuery]) -> None:
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

    def _fetch_page(self, uri, headers=BASE_HEADERS):
        # TODO: logging
        request = urllib.request.Request(uri, headers=headers)

        gzip_bytes = None
        with urllib.request.urlopen(request) as response:
            # TODO: assert that the data is actually gzip
            gzip_bytes = response.read()

        return gzip.decompress(gzip_bytes).decode()

    class ResultAttributes(enum.StrEnum):
        KIND = enum.auto()
        LINK = enum.auto()

    def _parse_results(self, html):
        parser = lxml.etree.HTMLParser()
        etree = lxml.etree.fromstring(html, parser=parser)

        # If querying breaks, consider referencing the documentation,
        # especially the part about generating xpath expressions; which
        # could form the basis of a means of fetching things with dynamic
        # selectors. https://lxml.de/xpathxslt.html#generating-xpath-expressions

        # List of artifacts (scholarly references like PDFs, books, etc.) on the current page
        artifacts = []

        # Fetch all elements with the class `gs_ri` (presumably "Google Scholar Row Item")
        for item in etree.xpath('//*[@id="gs_res_ccl_mid"]/div[*]/*[@class="gs_ri"]'):
            # > The .find*() methods are usually faster than the full-blown XPath support
            # - https://lxml.de/xpathxslt.html#xpath

            current_artifact = {}

            # `current_artifact[property_name]` is repeated as `match` has isolated scope
            for property_name in GScholar.ResultAttributes.__members__.values():
                match property_name:
                    case GScholar.ResultAttributes.KIND:
                        xpath_result = item.find('.//span[@class="gs_ct1"]')
                        if text := getattr(xpath_result, "text", None):
                            current_artifact[property_name] = text[1:-1].lower()
                        else:
                            current_artifact[property_name] = None
                    case GScholar.ResultAttributes.LINK:
                        current_artifact[property_name] = item.find(".//a").attrib[
                            "href"
                        ]

            artifacts.append(current_artifact)

        return artifacts

    def results(self):
        uri = self.query.as_uri()
        html = self._fetch_page(uri)
        return self._parse_results(html)


if __name__ == "__main__":
    query = GScholarQuerySimple(sys.argv[0])
    client = GScholar(query)
    results = client.results()
    print(json.dumps(results, indent=2))
