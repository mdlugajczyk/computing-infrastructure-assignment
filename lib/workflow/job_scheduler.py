from lib.workflow.dag.dag import DAG

class JobScheduler:
    """
    Schedules jobs from workfow file.
    """

    def schedule(self, jobs, relations):
        """
        Schedules jobs by building a graph from relationship
        and sorting it topologically.

        :param jobs: Jobs to sort.
        :param relations: List of Parent/Child relations.
        :type relations: List of pairs of lists
        """
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
    
