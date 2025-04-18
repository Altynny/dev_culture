from edge import edge
from route import route
from collections import defaultdict

class graph:
    matrix = defaultdict(lambda: {}) # матрица смежности

    def add_edge(self, edge: edge):
        self.matrix[edge.nodes[0]][edge.nodes[1]] = edge

    def create_edge(self, node1: str, node2: str, length=1):
        self.add_edge(edge(node1, node2, length))
    
    # поделить 1 на длину каждого ребра 
    def _pheromones_update(self, route: route, ro: float):
        delta_pher = 1 / route.length

        # испарение на всех рёбрах
        for node1 in self.matrix:
            for node2 in self.matrix[node1]:
                self.matrix[node1][node2].pheromones *= ro

        # добавление феромона на пройденном пути
        for n in range(1, len(route.nodes)):
            node1 = route.nodes[n-1]
            node2 = route.nodes[n]
            self.matrix[node1][node2].pheromones += delta_pher