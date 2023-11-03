#!/usr/bin/env python3

import sys
import json

class Harness:
    pass

from gscholar.parser import Parser

if __name__ == '__main__':
    """
    Run me with 
    
    Generate HTML to be used by running `python -m gscholar.bin.fetcher chimichanga`
    """
    with open(sys.argv[1], 'r') as file:
        html_str = file.read()
    results = Parser.parse_results(html_str)
    print(json.dumps(results, indent=2))

# TODO(@aryehh): for testing clarity, see if we can drop javascript, etc. from html
# TODO(@aryehh): for testing clarity, see if we can format html nicely
