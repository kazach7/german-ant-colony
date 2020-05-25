"""
algorithm.py
The implementation of the ant colony algorithm.
"""
from graph import Path
import random

class Solver:
    def __init__(self, graph, printer, verbosity, initial_pheromone_amount, state_displaying_period):
        self.graph = graph
        self.printer = printer
        self.verbosity = verbosity
        self.initial_pheromone_amount = initial_pheromone_amount
        self.state_displaying_period = state_displaying_period

    def perform_algorithm(self, iterations, population_size, evaporation_factor, 
                          pheromone_influence, heuristic_influence):
        self.initialize_pheromone_array()
        self.edge_choice_probabilities = {}
        shortest_path = Path([], float("inf"))

        for i in range(iterations):
            if (self.verbosity >= 1):
                print ("=== Iteration ", i, end="\n\n")
            self.edge_choice_probabilities.clear()
            for j in range(population_size):
                if (self.verbosity >= 1):
                    print ("Ant ", j)
                path = self.choose_path_for_ant(pheromone_influence, heuristic_influence)
                self.drop_pheromone_on_path(path)
                if (path.lenght < shortest_path.lenght):
                    shortest_path = path
            self.update_pheromone_array(evaporation_factor, shortest_path)
            if (i % self.state_displaying_period == 0):
                self.printer.display_state(self.pheromone_array, i)
        self.printer.display_state(self.pheromone_array, iterations)
            
    def initialize_pheromone_array(self):
        self.pheromone_array = {edge:self.initial_pheromone_amount for edge in self.graph.edges}
        self.dropped_pheromone = {edge:0 for edge in self.graph.edges}

    def choose_path_for_ant(self, pheromone_influence, heuristic_influence):
        chosen_edges = []
        node = self.graph.start
        while not (node == self.graph.end):
            possible_edges = self.graph.edges_adjacent_to_node[node][:]
            if (chosen_edges): possible_edges.remove(chosen_edges[-1])

            # Calculate the probabilities.
            # If another ant in current iteration has already been in this node, having come
            # through the same edge, then the probabilities are already calculated.
            if (chosen_edges 
                and node in self.edge_choice_probabilities 
                and chosen_edges[-1] in self.edge_choice_probabilities[node]
            ):
                probabilities = self.edge_choice_probabilities[node][chosen_edges[-1]]
                if (self.verbosity == 2):
                    for i in range (len(possible_edges)):
                        print (possible_edges[i], "[prob:", "{:.3f}".format(probabilities[i]), end="], ")
            else:
                sum = 0
                for edge in possible_edges:
                    sum += self.pheromone_array[edge]**pheromone_influence
                    sum += (1/self.graph.edges_lenght[edge])**heuristic_influence

                probabilities = []
                for edge in possible_edges:
                    probabilities.append((self.pheromone_array[edge]**pheromone_influence \
                                              + (1/self.graph.edges_lenght[edge])**heuristic_influence) \
                                             / sum)
                    if (self.verbosity == 2):
                        print (edge, "[prob:", "{:.3f}".format(probabilities[-1]), end="], ")
                
                # Store the result for future ants.
                if (chosen_edges): 
                    if (not node in self.edge_choice_probabilities): 
                        self.edge_choice_probabilities[node] = {}
                    self.edge_choice_probabilities[node][chosen_edges[-1]] = probabilities

            # Draw the next edge.    
            drawn_edge = random.choices(possible_edges, probabilities, k=1)[0]
            if (self.verbosity == 2):
                print("drawn edge: ", drawn_edge)
            chosen_edges.append(drawn_edge)
            if (node == drawn_edge[0]): 
                node = drawn_edge[1]
            else:
                assert (node == drawn_edge[1])
                node = drawn_edge[0]
        
        assert (chosen_edges)
        lenght = 0
        for edge in chosen_edges: lenght += self.graph.edges_lenght[edge]
        
        if (self.verbosity >= 1):
            if (self.verbosity == 2): print()
            print ("Chosen path: ", chosen_edges, "\nLenght: ", lenght, end="\n\n")
        return Path(chosen_edges, lenght)
    
    def drop_pheromone_on_path(self, path):
        for edge in path.edges:
            self.dropped_pheromone[edge] += (1/path.lenght)
    
    def update_pheromone_array(self, evaporation_factor, shortest_path):
        for edge in self.graph.edges:
            self.pheromone_array[edge] = (1-evaporation_factor)*self.pheromone_array[edge] \
                                        + self.dropped_pheromone[edge]
            if (edge in shortest_path.edges):
                self.pheromone_array[edge] += evaporation_factor*self.dropped_pheromone[edge]

        self.dropped_pheromone = {edge:0 for edge in self.graph.edges}
            
                                             



                





        








    