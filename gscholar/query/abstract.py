from abc import ABC, abstractmethod
import urllib.parse

class Abstract(ABC):
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

    def as_uri(self, endpoint=DEFAULT_ENDPOINT, additional_params={}):
        encoded_params = urllib.parse.urlencode({
            **self._query_parameters(),
            **Abstract.COMMON_PARAMS,
            **additional_params,
        }, quote_via=urllib.parse.quote_plus)
        return "".join(
            [
                Abstract.BASE_URI,
                "/",
                endpoint,
                "?",
                encoded_params,
            ]
        )
