from lib.exception.dag_cycle_exception import DAGCycleException


class DAG:

    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges
        self._build_adj_list()

    def sort(self):
        self._setup()

        while len(self._unmakred_nodes) > 0:
            v = self._unmakred_nodes.pop()
            self._visit(v)

        return self._sorted

    def _visit(self, v):
        if self._tmp_marked_nodes[v]:
            raise DAGCycleException
        if not self._marked_nodes[v]:
            self._tmp_marked_nodes[v] = True
            for w in self._adj_list[v]:
                self._visit(w)
            self._mark(v)
            self._sorted = [v] + self._sorted
            
    def _build_adj_list(self):
        self._adj_list = {}
        for vertex in self.vertices:
            vertex.has_incoming_edges = False
            self._adj_list[vertex] = []
            for edge in self.edges:
                if edge[0] == vertex:
                    self._adj_list[vertex].append(edge[1])
                if edge[1] == vertex:
                    vertex.has_incoming_edges = True

    def _remove_edge(self, edge):
        self._adj_list[edge[0]].remove(edge[1])

    def _mark(self, v):
        self._marked_nodes[v] = True
        self._tmp_marked_nodes[v] = False

    def _setup(self):
        self._sorted = []
        self._marked_nodes = {}
        self._tmp_marked_nodes = {}
        self._n_marked_nodes = 0
        self._unmakred_nodes = []
        for v in self.vertices:
            self._marked_nodes[v] = False
            self._tmp_marked_nodes[v] = False
            self._unmakred_nodes.append(v)
