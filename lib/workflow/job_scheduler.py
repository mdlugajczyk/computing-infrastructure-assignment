from lib.workflow.dag.dag import DAG

class JobScheduler:

    def schedule(self, jobs, relations):
        graph = self._build_graph(jobs, relations)
        return graph.sort()

    def _build_graph(self, jobs, relations):
        return DAG(jobs, self._build_edges(jobs, relations))

    def _build_edges(self, vertices, relations):
        mapping = {}
        for vertex in vertices:
            mapping[vertex.name] = vertex
        edges = []
        for rel in relations:
            for parent in rel[0]:
                for child in rel[1]:
                    edges.append((mapping[parent], mapping[child]))
        return edges
    
