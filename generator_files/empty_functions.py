"""
EMPTY
Functions for checking and creating path-related features.

NOTE:
in many of the functions in this file, the letters a-i are used for variable names. These letters correspond to the 
below 9 by 9 configuration of nodes, where e is the source node:

a b c
d e f
g h i

"""
import random 

from helper_functions import *

def empty_matchmaker(G,source_node):

    empty_dict = {
        "make_new_grass_patch":1,
        "make_forest":1,
        "make_grass_node":3,
        "make_tree":15,
        "make_ox_bow_lake":10,
        "make_house_t_junction":10
    }
        
    possible_replacements = []

    if check_new_grass_patch(G,source_node):
        possible_replacements.append("make_new_grass_patch")
        possible_replacements.append("make_ox_bow_lake")
        possible_replacements.append("make_house_t_junction")
       # possible_replacements.append("make_forest")


    possible_replacements.append("make_grass_node")
    possible_replacements.append("make_tree")

    probabilities = probability_generator(empty_dict,possible_replacements)
    return random.choices(possible_replacements, weights=probabilities, k=1)[0]

def check_new_grass_patch(G,source_node):

    #checks if a 9 by 9 patch of grass is possible

    x,y = source_node
    b2 = ((x+2),y)
    h0 = ((x-2),y)

    centre_of_up_patch = h0
    
    eight_neighbours = eight_connected_neighbours(G,centre_of_up_patch)

    allowed_types = ["grass","empty"]
    check_patch = True

    for node in eight_neighbours:
        if G.nodes[node]['type'] in allowed_types:
            continue
        else:
            check_patch = False
        
    if check_patch:
        return True
    
    centre_of_down_patch = b2
    
    eight_neighbours = eight_connected_neighbours(G,centre_of_down_patch)
    
    check_patch = True

    for node in eight_neighbours:
        if G.nodes[node]['type'] in allowed_types:
            continue
        else:
            check_patch = False

    if check_patch:
        return True

    return False

def make_new_grass_patch(G,source_node):

    
    x,y = source_node
    a = ((x-1),(y-1))
    a0 = ((x-4),(y-1))
    a2 = ((x+2),(y-1))
    b = ((x-1),y)
    b0 = ((x-4),y)
    b2 = ((x+2),y)
    h0 = ((x-2),y)


    choices = []

    centre_of_up_patch = h0
    
    up_neighbours = eight_connected_neighbours(G,centre_of_up_patch)

    allowed_types = ["grass","empty"]
    check_patch = True

    for node in up_neighbours:
        if G.nodes[node]['type'] in allowed_types:
            continue
        else:
            check_patch = False
        
    if check_patch:
        choices.append("u")
    
    centre_of_down_patch = b2
    
    down_neighbours = eight_connected_neighbours(G,centre_of_down_patch)
    
    check_patch = True

    for node in down_neighbours:
        if G.nodes[node]['type'] in allowed_types:
            continue
        else:
            check_patch = False

    if check_patch:
        choices.append("d")

    choice = random.choice(choices)

    if choice=="u":
        for node in up_neighbours:
            G.nodes[node]['type']="grass"

    elif choice=="d":
        for node in down_neighbours:
            G.nodes[node]['type']="grass"

    G.nodes[source_node]['type']="grass"

    return G

################

def make_ox_bow_lake(G,source_node):
    x,y = source_node
    a = ((x-1),(y-1))
    a0 = ((x-4),(y-1))
    a2 = ((x+2),(y-1))
    b = ((x-1),y)
    b0 = ((x-4),y)
    b2 = ((x+2),y)
    h0 = ((x-2),y)


    choices = []

    centre_of_up_patch = h0
    
    up_neighbours = eight_connected_neighbours(G,centre_of_up_patch)

    allowed_types = ["grass","empty"]
    check_patch = True

    for node in up_neighbours:
        if G.nodes[node]['type'] in allowed_types:
            continue
        else:
            check_patch = False
        
    if check_patch:
        choices.append("u")
    
    centre_of_down_patch = b2
    
    down_neighbours = eight_connected_neighbours(G,centre_of_down_patch)
    
    check_patch = True

    for node in down_neighbours:
        if G.nodes[node]['type'] in allowed_types:
            continue
        else:
            check_patch = False

    if check_patch:
        choices.append("d")

    choice = random.choice(choices)

    if choice=="u":
        for node in up_neighbours:
            G.nodes[node]['type']="river"

    elif choice=="d":
        for node in down_neighbours:
            G.nodes[node]['type']="river"

    G.nodes[source_node]['type']="grass"

    return G



def make_forest(G,source_node):

    
    x,y = source_node

    b2 = ((x+2),y)
    h0 = ((x-2),y)


    choices = []

    centre_of_up_patch = h0
    
    up_neighbours = eight_connected_neighbours(G,centre_of_up_patch)

    allowed_types = ["grass","empty"]
    check_patch = True

    for node in up_neighbours:
        if G.nodes[node]['type'] in allowed_types:
            continue
        else:
            check_patch = False
        
    if check_patch:
        choices.append("u")
    
    centre_of_down_patch = b2
    
    down_neighbours = eight_connected_neighbours(G,centre_of_down_patch)
    
    check_patch = True

    for node in down_neighbours:
        if G.nodes[node]['type'] in allowed_types:
            continue
        else:
            check_patch = False

    if check_patch:
        choices.append("d")

    choice = random.choice(choices)

    if choice=="u":
        for node in up_neighbours:
            G.nodes[node]['type']="irreplaceable_grass"

        trees = random.choices(up_neighbours, k=3)

        for node in trees:
            G.nodes[node]['type']="tree"

    elif choice=="d":
        for node in down_neighbours:
            G.nodes[node]['type']="irreplaceable_grass"
        trees = random.choices(down_neighbours, k=3)

        for node in trees:
            G.nodes[node]['type']="tree"

    G.nodes[source_node]['type']="grass"

    return G

def make_grass_node(G,source_node):

    G.nodes[source_node]['type']="grass"
    print("make_grass_node(G,",source_node,")")

    return G

def make_tree(G,source_node):

    G.nodes[source_node]['type']="tree"
    print("make_tree(G,",source_node,")")

    return G

def make_ob(G,source_node):
    G.nodes[source_node]['type']="out-of-bounds"
    print("make_tree(G,",source_node,")")

    return G

def make_house_t_junction(G,source_node):

    
    x,y = source_node
    
    a = ((x-1),(y-1))
    a0 = ((x-4),(y-1))
    a1=  ((x-4),(y-2))
    a2 = ((x+2),(y-1))
    b = ((x-1),y)
    b0 = ((x-4),y)
    b2 = ((x+2),y)
    c = ((x-1),(y+1))
    c0 = ((x-4),(y+1))
    c1 =  ((x-4),(y+2))
    c2 = ((x+2),(y+1))
    d = (x,(y-1))
    d0 = (x-3,(y-1))
    d2 = (x+3,(y-1))
    e = source_node
    e0 = ((x-3),(y))
    e2 = ((x+3),(y))
    f = (x,(y+1))
    f0 = (x-3,(y+1))
    f2 = (x+3,(y+1))
    g = ((x+1),(y-1))
    g0 = ((x-2),(y-1))
    g2 = ((x+4),(y-1))
    h = ((x+1),y)
    h0 = ((x-2),y)
    h2 = ((x+4),y)
    i = ((x+1),(y+1))
    i0 = ((x-2),(y+1))
    i2 = ((x+14),(y+1))
    d1 = (x-3,(y-2))
    f1 = (x-3,(y+2))

    choices = []

    centre_of_up_patch = h0
    
    up_neighbours = eight_connected_neighbours(G,centre_of_up_patch)

    allowed_types = ["grass","empty"]
    check_patch = True

    for node in up_neighbours:
        if G.nodes[node]['type'] in allowed_types:
            continue
        else:
            check_patch = False
        
    if check_patch:
        choices.append("u")
    
    centre_of_down_patch = b2
    
    down_neighbours = eight_connected_neighbours(G,centre_of_down_patch)
    
    check_patch = True

    for node in down_neighbours:
        if G.nodes[node]['type'] in allowed_types:
            continue
        else:
            check_patch = False

    if check_patch:
        choices.append("d")

    choice = random.choice(choices)

    if choice=="u":
        up_t_junction=[d0,e0,f0,h0,b]
        
        for node in up_t_junction:
            G.nodes[node]['type']="path"

        G.nodes[g0]['type']="house"
        G.nodes[i0]['type']="house"
        

    elif choice=="d":
        down_t_junction=[h,b2,e2,d2,f2]
        for node in down_t_junction:
            G.nodes[node]['type']="path"

        G.nodes[a2]['type']="house"
        G.nodes[c2]['type']="house"

    G.nodes[source_node]['type']="path"

    return G