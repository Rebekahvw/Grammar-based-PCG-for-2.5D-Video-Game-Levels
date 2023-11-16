"""
GRASS

Functions for checking and creating grass-related features.

NOTE:
in many of the functions in this file, the letters a-i are used for variable names. These letters correspond to the 
below 9 by 9 configuration of nodes, where e is the source node:

a b c
d e f
g h i

"""
import networkx as nx
import numpy as np
from collections import defaultdict
from PIL import Image #represent level as image
import random 

from river_functions import *
from path_functions import *
from helper_functions import *

def grass_matchmaker(G,source_node):

    grass_dict = {
        # the numbers are a ranking. The better the rank (1>2>3 etc) the higher the probability of seeing that feature

        "make_grass_node":10,
        "make_path_L_bend":2,
        "make_t_junction":1,
        "make_forked_road":4,
        "make_horizontal_path":2,
        "make_vertical_path":2,
        "make_castle":8,
        "make_house":10,
        "make_horizontal_river":1,
        "make_vertical_river":1,
        "make_bridged_river": 20,
        "make_large_castle":13

    }

    possible_replacements = []
    grass_count=0
    path_count=0
    path_nodes=[]
    river_count=0
    river_nodes=[]

    for node in list(G.neighbors(source_node)):
        if G.nodes[node]['type']=="grass":
            grass_count+=1
        elif G.nodes[node]['type']=="path":
            path_count+=1
            path_nodes.append(node)
        elif G.nodes[node]['type']=="river":
            river_nodes.append(node)
            river_count+=1
        
    possible_replacements = []

    if check_castle(G,source_node):
        possible_replacements.append("make_castle")

    
    if check_large_castle(G,source_node):
        possible_replacements.append("make_large_castle")

    river_reps=[]
    if river_count>0:

        river_node = random.choice(river_nodes)
        rep = river_matchmaker(G,river_node)
        if rep is not None:
            possible_replacements.append(rep)
            river_reps.append(rep)
            print("Found river replacement",rep)

    path_reps=[]

    if path_count>0:

        path_node = random.choice(path_nodes)
        rep = path_matchmaker(G,path_node)
        if rep is not None:
            possible_replacements.append(rep)
            path_reps.append(rep)
            print("Found path replacement",rep)

    possible_replacements.append("make_grass_node")

    probabilities = probability_generator(grass_dict,possible_replacements)
    choice = random.choices(possible_replacements, weights=probabilities, k=1)[0]

    if choice in path_reps:
        return choice,path_node
    
    elif choice in river_reps:
        return choice,river_node
    
    else:
        return choice,source_node

def make_grass_node(G,source_node):

    G.nodes[source_node]['type']="grass"
    print("make_grass_node(G,",source_node,")")

    return G

def make_tree(G,source_node):

    G.nodes[source_node]['type']="tree"
    print("make_tree(G,",source_node,"source_node")

    return G




