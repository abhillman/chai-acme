from . import logging
from .backend import Backend
from .parser import Parser
from .query import Simple
from .query.abstract import Abstract

log = logging.make_logger()

class GScholar:
    def __init__(self, query: type[Abstract]) -> None:
        self.query = query

    def results(self):
        html = Backend.html(self.query)
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
