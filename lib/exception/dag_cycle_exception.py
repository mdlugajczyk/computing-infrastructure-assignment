class DAGCycleException(Exception):
    """
    An exception thrown when a cycle in DAG is detected.
    """

    def __init__(self):
        super(DAGCycleException, self).__init__("Invalid DAG. Cycle detected.")
