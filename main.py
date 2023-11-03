import json

import gscholar

if __name__ == "__main__":
    with gscholar.GScholar.simple_query("pasta primavera") as gs:
        print(json.dumps(gs.results(), indent=2))
