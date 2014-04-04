class DAGCycleException(Exception):

    def __init__(self):
        super(DAGCycleException, self).__init__("Invalid DAG. Cycle detected.")
