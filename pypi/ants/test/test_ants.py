import pytest
from ants.graph import graph
from ants.algorithm import ant_colony

def test_route_is_the_shortest():
    REAL_SHORTEST_ROUTE = 14

    g = graph()
    g.read_edges('test/edges.txt')

    ITERATIONS = 10**4
    ANTS = 1
    ALPHA = 1
    BETA = 0.6
    RO = 0

    ant_alg = ant_colony()
    result = ant_alg.algorithm(g, iterations=ITERATIONS, ants=ANTS, alpha=ALPHA, beta=BETA, ro=RO)
    assert result[0].length == REAL_SHORTEST_ROUTE