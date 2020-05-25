"""
graph.py
Provides graph representation of the network.
"""

class Graph:
    def __init__(self, nodes, nodes_coord, edges, edges_lenght, start=None, end=None):
        self.nodes = nodes
        self.nodes_coord = nodes_coord
        self.edges = edges
        self.edges_lenght = edges_lenght

        self.edges_adjacent_to_node = {node:[] for node in self.nodes}
        for edge in edges:
            for node in edge:
                self.edges_adjacent_to_node[node].append(edge)

        assert (start is None or start in self.nodes)
        assert (end is None or end in self.nodes)
        self.start = start
        self.end = end

class Path:
    def __init__(self, edges, lenght):
        self.edges = edges
        self.lenght = lenght
