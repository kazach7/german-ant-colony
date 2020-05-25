"""
main.py
Initializes the program, starts the algorithm.
"""
import xml.etree.ElementTree as ET
import argparse
import math
from graph import Graph
from printer import Printer
from algorithm import Solver
import config as cfg

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbosity', type=int, 
                        default=0, help='Verbosity level -- possible values: (0,1,2)')

    graph = parseGraph(cfg.path)
    assert (cfg.source != cfg.destination)
    graph.start = cfg.source
    graph.end = cfg.destination
    assert (cfg.population_size > 0)
    assert (cfg.evaporation_factor > 0.0 and cfg.evaporation_factor <= 1.0)
    assert (cfg.pheromone_influence >= 0.0)
    assert (cfg.heuristic_influence >= 0.0)

    args = parser.parse_args()
    assert (args.verbosity in (0,1,2))

    printer = Printer(graph)
    solver = Solver(graph, printer, args.verbosity, 
                    cfg.initial_pheromone_amount, cfg.state_displaying_period)
    
    solver.perform_algorithm(cfg.iterations, cfg.population_size, cfg.evaporation_factor, 
                            cfg.pheromone_influence, cfg.heuristic_influence)

def parseGraph(path):
        tree = ET.parse(path)
        root = tree.getroot()

        nodes = []
        nodes_coord = {}
        links = []
        links_lenght = {}

        for node in root[0][0]:
            nodes.append(node.get('id'))
            nodes_coord[node.get('id')] = (float(node[0][0].text), float(node[0][1].text)) 
        for link in root[0][1]:
            links.append((link[0].text, link[1].text))
            x_len = abs(nodes_coord[link[0].text][0] - nodes_coord[link[1].text][0])
            y_len = abs(nodes_coord[link[0].text][1] - nodes_coord[link[1].text][1])
            links_lenght[(link[0].text, link[1].text)] = math.sqrt(x_len**2 + y_len**2)

        return Graph(nodes, nodes_coord, links, links_lenght)

main()

    #parser.add_argument('path', type=str, help='Path to an xml file with the network.')
    #parser.add_argument('--source', type=str, required=True, help='Starting node in the graph (name)')
    #parser.add_argument('--dest', type=str, required=True, help='Destination node in the graph (name)')
    #parser.add_argument('-i', '--iterations', type=int, required=True,
    #                    help='Number of algorithm iterations')
    #parser.add_argument('-p', '--population', type=int, required=True,
    #                    help='Population size')
    #parser.add_argument('-e', '--evaporation', metavar='(0.0, 1.0]', type=float, required=True,
    #                    help='Evaporation factor')
    #parser.add_argument('-ph', '--pheromone', type=float, required=True, 
    #                    help='Influence of the pheromone in edge choice probability')
    #parser.add_argument('-he', '--heuristic', type=float, required=True,
    #                    help='Influence of the heuristic value in edge choice probability')
    #args = parser.parse_args()
    #path = args.path
    #source = args.source
    #if (config.source not in graph.nodes):
    #    print ("Provided source node does not exist in the graph.")
    #    return
    #dest = args.dest
    #if (config.destination not in graph.nodes):
    #    print("Provided destination node does not exist in the graph.")
    #    return
    #graph.start = config.source 
    #graph.end = config.destination

    #iterations = args.iterations
    #population_size = args.population
    #if (population_size <= 0):
    #    print ("Population size must be a positive integer!")
    #    return
    #evaporation_factor = args.evaporation
    #if (evaporation_factor <= 0.0 or evaporation_factor > 1.0):
    #    print ("Evaporation factor's range is: (0.0, 1.0]")
    #    return
    #pheromone_influence = args.pheromone
    ##heuristic_influence = args.heuristic
    #if (pheromone_influence < 0 or heuristic_influence < 0):
    #    print ("Influence values must be non-negative!")