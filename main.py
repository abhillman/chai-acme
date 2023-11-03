import json
import sys

import gscholar

if __name__ == "__main__":
    with gscholar.GScholar.simple_query(sys.argv[1]) as gs:
        print(json.dumps(gs.results(), indent=2))
