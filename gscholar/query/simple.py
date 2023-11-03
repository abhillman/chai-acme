from gscholar.query.abstract import Abstract

class Simple(Abstract):
    def __init__(self, query):
        self.query = query

    def _query_parameters(self):
        return {"q": self.query}