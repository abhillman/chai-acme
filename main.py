from gscholar import gscholarquery

if __name__ == "__main__":
    query = GScholarQuerySimple(sys.argv[0])
    client = GScholar(query)
    results = client.results()
    print(json.dumps(results, indent=2))