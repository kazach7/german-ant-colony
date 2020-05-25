"""
printer.py
Displays algorithm state.
"""
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt

class Printer():
    def __init__(self, graph):
        matplotlib.use('TkAgg')
        self.graph = graph

        self.G=nx.Graph()
        self.G.add_nodes_from(self.graph.nodes)
        self.G.add_edges_from(self.graph.edges)

        self.node_labels = {node:node for node in self.graph.nodes}
        self.edge_labels = {e:"0" for e in self.G.edges()}
        self.edge_colors = {e:'black' for e in self.G.edges()}
        
        self.pos = nx.spring_layout(self.G, pos=self.graph.nodes_coord, scale=2.0, iterations=1000)

    def display_state(self, pheromone_array, iteration_number):
        for e in self.G.edges():
            if (e in self.graph.edges): # networkx graph may change nodes order in an edge
                pheromone = pheromone_array[e]
            else: 
                pheromone = pheromone_array[(e[1], e[0])]
            self.edge_labels[e] = '{:.2f}'.format(pheromone)

        nx.draw_networkx_nodes(self.G, self.pos, node_size=200, node_color="pink", alpha=0.9)
        nx.draw_networkx_edges(self.G, self.pos, edge_color=tuple(self.edge_colors.values()))
        nx.draw_networkx_labels(self.G, self.pos, labels=self.node_labels, font_size=9, alpha=2)
        nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=self.edge_labels, font_size=8)
        
        plt.title('Iteration {}'.format(iteration_number))

        mng = plt.get_current_fig_manager()
        mng.resize(*mng.window.maxsize())
        mng.window.wm_geometry("+0+0")
        plt.show()

