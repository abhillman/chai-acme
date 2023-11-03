import sys
import gscholar
from gscholar import GScholar
from gscholar.query import Simple as GScholarSimpleQuery
import json

if __name__ == "__main__":
    gs_query = GScholarSimpleQuery(sys.argv[1])
    gs = GScholar(gs_query)
    results = gs.results()
    print(json.dumps(results, indent=2))