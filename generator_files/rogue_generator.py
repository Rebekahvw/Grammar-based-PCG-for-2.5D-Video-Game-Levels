import networkx as nx
import numpy as np
from collections import defaultdict
from PIL import Image #represent level as image
import random 

from path_functions import *
from river_functions import *
from grass_functions import *
from empty_functions import *

"""

Rogue-like domain

Within this particular domain, the world or level is represented as a two-dimensional grid consisting of cells. 
However, in this scenario, each cell can exist in any one of 38 distinct states. 
The motivation behind this particular domain was twofold; firstly, it was intended to utilize domains with similar characteristics to previous works. Secondly, it was designed as a more intricate iteration of the Maze domain that could be observed in contemporary video games.

green - grass
blue - river
red - path
pink - bridge
black - wall
yellow - houses
white - gate
dark green - trees

"""
from helper_functions import *

def represent_graph(G):

    # a function to convert a graph into an image of a level
    
    # if the level is binary, just have to consider 1s and 0s. Else, have a lot more to consider.
    # matrix_rep is the matrix representation of the level (generated by matrix_representation)
    node_type = nx.get_node_attributes(G, 'type')

    image = np.zeros((31, 31, 3), dtype=np.uint8)
    
    for y in range(31):
        for x in range(31):

            type = node_type[x,y]
            if type =='grass' or type=="irreplaceable_grass": # light green
                image[x][y]=[31,198,0]
            elif type =='path': #dull red/maroon
                image[x][y]=[151,59,50]
            elif type =='empty':#white
                image[x][y]=[255,255,255] 
            elif type =='out-of-bounds': #purple
                image[x][y]=[132,89,126]
            elif type =='river': #blue
                image[x][y]=[0,23,248]
            elif type =='house': #yellow
                image[x][y]=[255,254,72]
            elif type =='bridge': #coral/pink
                image[x][y]=[234,63,35]
            elif type =='wall': #black
                image[x][y]=[0,0,0]
            elif type =='indoors': #grey
                image[x][y]=[127,127,127]
            elif type =='doorway': #beige
                image[x][y]=[232,220,202]
            elif type =='tree': #green
                image[x][y]=[0,103,26] 

    # delete border rows
    image = np.delete(image, 0, axis=0)
    image = np.delete(image, 29, axis=0)

    # delete border columns
    image = np.delete(image, 0, axis=1)
    image = np.delete(image, 29, axis=1)
            
    level = Image.fromarray(image, "RGB")
    return level

def initial_graph(dimensions):

    G=nx.grid_graph(dim=dimensions) 
    
    for node in G.nodes:
        x, y = node #gets label of node, which corresponds to its coordinate/position in the grid
    
        # Check if the node is on the edge of the grid, then sets the type to out of bounds
        # else, sets type to "empty". empty cells are non-terminal cells that have to be replaced before the level can be called complete
        
        if x == 0 or x == dimensions[0]-1 or y == 0 or y == dimensions[1]-1:
            G.nodes[node]['type'] = 'out-of-bounds'
        else:
            G.nodes[node]['type'] = 'empty'

    return G


def create_level(dimensions):
    # dimensions should include an extra 1 in each direction for out of bounds nodes
    # must be square

    G = initial_graph(dimensions) # [31,31] for dimensions for our purposes

    # finding the centre node if possible, and a near-centre node if not

    if (dimensions[0]-1)%2==0:
        centre_x=(dimensions[0]-1)/2
    else:
        centre_x = (dimensions[0]-2)/2
    
    if (dimensions[1]-1)%2==0:
        centre_y=(dimensions[0]-1)/2
    else:
        centre_y = (dimensions[1]-2)/2

    # set the centre node to be either grass or path randomly

    G.nodes[(centre_x, centre_y)]['type'] = random.choice(['river','path'])
    source_node = (centre_x, centre_y)

    #random.seed(100)
 
    queue = [source_node]
    visited = set()
    counter = 0
    rep_counter =0

    replacement_dictionary={}

    while check_for_empty_nodes(G) and queue:
        source_node = queue.pop(0)
        if source_node in visited and source_node in replacement_dictionary.keys() and replacement_dictionary[source_node] is not None:
            counter+=1
            continue
        visited.add(source_node)

        replacement_function = None
        new_source = None

        if G.nodes[source_node]['type'] == "path" or G.nodes[source_node]['type'] == "bridge":
            replacement_function = path_matchmaker(G, source_node)

        elif G.nodes[source_node]['type'] == "river":
            replacement_function = river_matchmaker(G, source_node)

        elif G.nodes[source_node]['type'] == "empty":
            replacement_function = empty_matchmaker(G, source_node)

        elif G.nodes[source_node]['type'] == "grass":
            replacement_function,new_source = grass_matchmaker(G, source_node)


        if replacement_function is not None:
            if new_source is None:
                G = execute_replacement(G, replacement_function, source_node)
            else:
                G = execute_replacement(G, replacement_function, new_source)

        new_neighbours = [neighbour for neighbour in G.neighbors(source_node) if neighbour not in visited]
        replacement_dictionary[source_node]=replacement_function
        queue.extend(new_neighbours)
        counter+=1

    print("counter is",counter)
    print("Replacement Dictionary:")
    for key in replacement_dictionary.keys():
        print(key,":",replacement_dictionary[key])
    
    return G


def check_for_empty_nodes(G):
    for node in G.nodes:
        if G.nodes[node]['type'] == 'empty':
            return True
    return False
    
# function that calls the appropriate replacement function
def execute_replacement(G, function_to_call, source_node):
    if function_to_call in globals() and callable(globals()[function_to_call]):
        function = globals()[function_to_call]
        G = function(G, source_node)
    return G












