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
        for edge in relations:
            src = edge[0]
            dst = edge[1]
            edges.append((mapping[src], mapping[dst]))
        return edges

    
