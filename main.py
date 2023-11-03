import sys
import gscholar
from gscholar import GScholar
from gscholar.query import Simple as GScholarSimpleQuery
import json

if __name__ == "__main__":
    with gscholar.GScholar.simple_query("pasta primavera") as gs:
        print(json.dumps(gs.results(), indent=2))
