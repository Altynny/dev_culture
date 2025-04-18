class route:
    def __init__(self, nodes: list, length: int, chance: float):
        self.nodes = nodes
        self.length = length
        self.chance = chance

    def __str__(self):
        return f'length - {self.length}\n{self.nodes}'