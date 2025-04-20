class Edge:
    """
    Graph edge with distance, attractiveness, and pheromone level.
    """

    def __init__(self, node1: str, node2: str, length: float = 1.0):
        """
        :param node1: Identifier of the first node.
        :param node2: Identifier of the second node.
        :param length: Distance between nodes.
        """
        self.nodes = (node1, node2)
        self.length = length
        self.attractiveness = 1.0 / length
        self.pheromones = 1.0