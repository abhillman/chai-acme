#!/usr/bin/env python3
import sys

from gscholar import Simple, Backend

if __name__ == '__main__':
    """
    Run with `$ python -m gscholar.bin.fetcher <query>`
    """
    query_str = sys.argv[1]
    # TODO(@abhillman): merge this functionality into main after we add argparse
    simple_query = Simple(query_str)
    html = Backend.html(simple_query)
    print(html)
