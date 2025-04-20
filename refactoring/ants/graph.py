from edge import Edge
from route import Route
from collections import defaultdict


class Graph:
    """
    Graph structure with adjacency matrix and pheromone updates.
    """

    def __init__(self):
        """
        Initialize an empty adjacency matrix.
        """
        self.matrix = defaultdict(dict)

    def add_edge(self, edge: Edge):
        """
        Add a pre-built Edge into the graph.

        :param edge: Edge instance connecting two nodes.
        """
        node1, node2 = edge.nodes
        self.matrix[node1][node2] = edge

    def create_edge(self, node1: str, node2: str, length: float = 1.0):
        """
        Create and add a new Edge based on node identifiers.

        :param node1: Identifier for the first node.
        :param node2: Identifier for the second node.
        :param length: Distance between nodes.
        """
        new_edge = Edge(node1, node2, length)
        self.add_edge(new_edge)

    def update_pheromones(self, route: Route, evaporation_coef: float):
        """
        Evaporate and deposit pheromones along edges in a completed route.

        :param route: Route instance with the tour path.
        :param evaporation_coef: Coefficient remaining after evaporation.
        """
        # Evaporation on all edges
        for src, targets in self.matrix.items():
            for dst, edge_obj in targets.items():
                edge_obj.pheromones *= evaporation_coef

        # Deposit pheromone along the route
        deposit = 1.0 / route.length
        for i in range(1, len(route.nodes)):
            src = route.nodes[i - 1]
            dst = route.nodes[i]
            self.matrix[src][dst].pheromones += deposit