from graph import graph, edge, route
import random
class ant_colony:
    
    __matrix = {}

    def __choose_next_node(self, node, neighbours):
            chances = []
            s = 0
            for neighbour in neighbours:
                dest_edge = self.__matrix[node][neighbour]
                tau2 = dest_edge.pheromones**self.__alpha
                nu2 = dest_edge.attractivnes**self.__beta
                factor = tau2*nu2
                chances.append(factor)
                s += factor
            chances = [x / s for x in chances]
            chosen = random.choices(neighbours, weights=chances)[0]
            for n, neighbour in enumerate(neighbours):
                if chosen == neighbour:
                    return chosen, chances[n]

    def __calc_route_len(self, nodes):
        length = 0
        for n in range(1, len(nodes)):
            length += self.__matrix[nodes[n-1]][nodes[n]].length
        return length

    def algorithm(self, graph: graph, iterations=1, ants=0, ro=0.25, alpha=1, beta=1):
        ro = 1 - ro # заранее вычитаем из единицы скорость испарения, получаем коэффициент оставшихся феромонов
        self.__matrix = graph.matrix # матрица смежности графа
        self.__alpha = alpha
        self.__beta = beta
        nodes = list(self.__matrix.keys()) # список вершин графа
        
        # если кол-во муравьёв не задано, оно будет равно кол-ву вершин
        if not ants: 
            ants = len(nodes)

        shortest_route = None
        shortest_routes = []
        ants_iterations = [[]]*ants
        for i in range(iterations):
            if i%(iterations//len(nodes))==0: random.shuffle(nodes)
            shortest_iter_route = None
            start_node = nodes[0]
            for ant in range(ants):
                curr_node = start_node
                visited = [start_node]
                route_chance = 1
                while True:
                    neighbours = list(self.__matrix[curr_node].keys())
                    
                    start_is_neighbour = False
                    neighbours_to_visit = []
                    for neighbour in neighbours:
                        if neighbour!=start_node:
                            if neighbour not in visited:      
                                neighbours_to_visit.append(neighbour)
                        else: start_is_neighbour = True

                    if not neighbours_to_visit:
                        if start_is_neighbour and len(visited) == len(nodes):
                            visited.append(start_node)
                            r = route(visited, self.__calc_route_len(visited), route_chance)
                            ants_iterations[ant].append(r.length)
                            graph._pheromones_update(r, ro)
                            if not shortest_iter_route or shortest_iter_route.length > r.length:
                                shortest_iter_route = r
                                if not shortest_route or shortest_route.length > r.length:
                                    shortest_route = r
                        break
                        
                    curr_node, chance = self.__choose_next_node(curr_node, neighbours_to_visit)
                    route_chance *= chance
                    visited.append(curr_node)
            
            shortest_routes.append(shortest_iter_route)

        return (shortest_route, shortest_routes, ants_iterations)