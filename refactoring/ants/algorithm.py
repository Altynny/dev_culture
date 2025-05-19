import random
from graph import Graph
from route import Route


class AntColony:
    """
    Ant Colony Optimization for finding shortest tours in a graph.
    """

    def __init__(self, evaporation_rate: float = 0.25, alpha: float = 1.0, beta: float = 1.0):
        """
        :param evaporation_rate: Fraction of pheromone that evaporates each iteration.
        :param alpha: Pheromone influence factor.
        :param beta: Heuristic attractiveness factor.
        """
        self.evaporation_coefficient = 1.0 - evaporation_rate
        self.alpha = alpha
        self.beta = beta
        self.graph_matrix = {}

    def _choose_next_node(self, current_node, neighbours: list) -> tuple:
        """
        Select the next node based on pheromone intensity and heuristic attractiveness.
        """
        weights = []
        total = 0.0

        for neighbour in neighbours:
            edge = self.graph_matrix[current_node][neighbour]
            pheromone_term = edge.pheromones ** self.alpha
            attractiveness_term = edge.attractiveness ** self.beta
            weight = pheromone_term * attractiveness_term
            weights.append(weight)
            total += weight

        probabilities = [w / total for w in weights]
        chosen = random.choices(neighbours, weights=probabilities, k=1)[0]
        probability = probabilities[neighbours.index(chosen)]
        return chosen, probability

    def _calculate_route_length(self, path: list) -> float:
        """
        Compute the total length of a sequence of nodes.
        """
        return sum(
            self.graph_matrix[path[i - 1]][path[i]].length
            for i in range(1, len(path))
        )

    def _filter_neighbours(self, current_node, neighbours: list, start_node, visited: list) -> tuple:
        """
        Identify which neighbours are unvisited and if return to start is possible.

        :return: (visitable neighbours, can return to start)
        """
        visitable = [n for n in neighbours if n not in visited and n != start_node]
        can_return = start_node in neighbours
        return visitable, can_return

    def find_shortest_paths(self, graph: Graph, iterations: int = 100, ants_count=None) -> tuple:
        """
        Run the optimization over the specified number of iterations.

        :param graph: Graph with adjacency matrix and pheromone update method.
        :param iterations: Number of simulation rounds.
        :param ants_count: Number of ants; defaults to total nodes.
        :return: (best route overall, best per iteration, route lengths per ant).
        """
        self.graph_matrix = graph.matrix
        nodes = list(self.graph_matrix.keys())
        ants_count = ants_count or len(nodes)

        best_route = None
        iteration_best_routes = []
        ants_route_lengths = [[] for _ in range(ants_count)]

        for iteration in range(iterations):
            if iteration % max(1, iterations // len(nodes)) == 0:
                random.shuffle(nodes)

            start_node = nodes[0]
            best_route_this_iter = None

            for ant_index in range(ants_count):
                current_node = start_node
                path = [current_node]
                path_probability = 1.0

                while True:
                    neighbours = list(self.graph_matrix[current_node].keys())
                    visitable, can_return = self._filter_neighbours(
                        current_node, neighbours, start_node, path
                    )
                    if not visitable:
                        if can_return and len(path) == len(nodes):
                            path.append(start_node)
                            length = self._calculate_route_length(path)
                            route_obj = Route(path, length, path_probability)
                            ants_route_lengths[ant_index].append(length)
                            graph.update_pheromones(route_obj, self.evaporation_coefficient)

                            if not best_route_this_iter or route_obj.length < best_route_this_iter.length:
                                best_route_this_iter = route_obj
                                if not best_route or route_obj.length < best_route.length:
                                    best_route = route_obj
                        break

                    current_node, prob = self._choose_next_node(current_node, visitable)
                    path_probability *= prob
                    path.append(current_node)

            iteration_best_routes.append(best_route_this_iter)

        assert best_route is not None, "No valid route found."
        return best_route, iteration_best_routes, ants_route_lengths