class edge:
    def __init__(self, node1: str, node2: str, length=1):
        self.nodes = (node1, node2)
        self.length = length
        self.attractivnes =  1/length
        self.pheromones = 1