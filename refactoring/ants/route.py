class Route:
    """
    Represents a candidate path in the graph.
    """

    def __init__(self, nodes: list, length: float, probability: float):
        """
        :param nodes: Sequence of nodes in the route.
        :param length: Total distance of the route.
        :param probability: Product of branch probabilities.
        """
        self.nodes = nodes
        self.length = length
        self.probability = probability

    def __str__(self):
        return f"Route(length={self.length}, nodes={self.nodes})"