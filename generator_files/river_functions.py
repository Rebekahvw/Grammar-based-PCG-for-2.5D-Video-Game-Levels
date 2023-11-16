"""
RIVER

Functions for checking and creating river-related features.

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
import random 

from helper_functions import *

def river_matchmaker(G,source_node):

    river_dict = {
        "make_horizontal_river":1,
        "make_vertical_river":1,
        "make_bridged_river": 20
    }

    possible_replacements = []

    if check_horizontal_river(G,source_node):
        possible_replacements.append("make_horizontal_river")
    
    if check_vertical_river(G,source_node):
        possible_replacements.append("make_vertical_river")

    if check_river_bridge(G,source_node):
        possible_replacements.append("make_river_bridge")


    if len(possible_replacements)>0:
        probabilities = probability_generator(river_dict,possible_replacements)
        print("Probabilities",probabilities)
        return random.choices(possible_replacements, weights=probabilities, k=1)[0]

    else:

        return None

def check_horizontal_river(G,source_node):
    
    node_type = nx.get_node_attributes(G, 'type')
    x,y = source_node

    a = ((x-1),(y-1))
    s = ((x-1),(y-2))
    b = ((x-1),y)
    c = ((x-1),(y+1))
    j = ((x-1),(y+2))
    d = (x,(y-1))
    t = (x,(y-2))
    e = source_node
    f = (x,(y+1))
    m = (x,(y+2))
    g = ((x+1),(y-1))
    u = ((x+1),(y-2))
    h = ((x+1),y)
    i = ((x+1),(y+1))
    p = ((x+1),(y+2))
    k = ((x-1),(y+3))
    n = (x,(y+3))
    q = ((x+1),(y+3))
    v = ((x-1),(y-3))
    w = (x,(y-3))
    z = ((x+1),(y-3))
    
    extra_nodes = [a,b,c,d,e,f,g,h,i,j,k,m,n,p,q,s,t,u,v,w,z]

    for node in extra_nodes:
        if node not in G.nodes:
            return False

    # check right river (e f m)
    #here we check that if we add the horizontal river, no nodes will become pooled

    #check if the nodes above or below have two river nodes next to each other
    right_river_check = True
    left_river_check = True

    if G.nodes[b]['type']=="river" and G.nodes[c]['type']=="river":
        right_river_check = False
    
    if G.nodes[c]['type']=="river" and G.nodes[j]['type']=="river":
        right_river_check = False
    
    if G.nodes[h]['type']=="river" and G.nodes[i]['type']=="river":
        right_river_check = False
    
    if G.nodes[i]['type']=="river" and G.nodes[p]['type']=="river":
        right_river_check = False
    
    # check beyond ones just above and below as well

    if G.nodes[d]['type']=="river" and G.nodes[a]['type']=="river" and G.nodes[b]['type']=="river":
        right_river_check = False
    
    if G.nodes[d]['type']=="river" and G.nodes[g]['type']=="river" and G.nodes[h]['type']=="river":
        right_river_check = False
    
    if G.nodes[j]['type']=="river" and G.nodes[k]['type']=="river" and G.nodes[n]['type']=="river":
        right_river_check = False
    
    if G.nodes[n]['type']=="river" and G.nodes[p]['type']=="river" and G.nodes[q]['type']=="river":
        right_river_check = False

    if G.nodes[j]['type']=="river" and G.nodes[p]['type']=="river":
        right_river_check = False
    
    if G.nodes[b]['type']=="river" and G.nodes[h]['type']=="river":
        right_river_check = False

    # left river checks


    if G.nodes[s]['type']=="river" and G.nodes[a]['type']=="river":
        left_river_check = False
    
    if G.nodes[a]['type']=="river" and G.nodes[b]['type']=="river":
        left_river_check = False
    
    if G.nodes[u]['type']=="river" and G.nodes[g]['type']=="river":
        left_river_check = False
    
    if G.nodes[g]['type']=="river" and G.nodes[h]['type']=="river":
        left_river_check = False

    # check beyond ones just above and below as well

    if G.nodes[v]['type']=="river" and G.nodes[s]['type']=="river" and G.nodes[w]['type']=="river":
        left_river_check = False
    
    if G.nodes[w]['type']=="river" and G.nodes[z]['type']=="river" and G.nodes[u]['type']=="river":
        left_river_check = False
    
    if G.nodes[h]['type']=="river" and G.nodes[i]['type']=="river" and G.nodes[f]['type']=="river":
        left_river_check = False
    
    if G.nodes[b]['type']=="river" and G.nodes[c]['type']=="river" and G.nodes[f]['type']=="river":
        left_river_check = False

    
    if G.nodes[s]['type']=="river" and G.nodes[u]['type']=="river":
        left_river_check = False
    
    if G.nodes[b]['type']=="river" and G.nodes[h]['type']=="river":
        left_river_check = False


    replaceable_types= ["grass","empty"]

    if G.nodes[f]['type'] not in replaceable_types or G.nodes[m]['type'] not in replaceable_types:
        right_river_check = False
    
    if G.nodes[t]['type'] not in replaceable_types or G.nodes[d]['type'] not in replaceable_types:
        left_river_check = False

    if right_river_check or left_river_check:
        return True
        
    return False

def make_horizontal_river(G, source_node):

    x,y = source_node

    a = ((x-1),(y-1))
    s = ((x-1),(y-2))
    b = ((x-1),y)
    c = ((x-1),(y+1))
    j = ((x-1),(y+2))
    d = (x,(y-1))
    t = (x,(y-2))
    e = source_node
    f = (x,(y+1))
    m = (x,(y+2))
    g = ((x+1),(y-1))
    u = ((x+1),(y-2))
    h = ((x+1),y)
    i = ((x+1),(y+1))
    p = ((x+1),(y+2))
    k = ((x-1),(y+3))
    n = (x,(y+3))
    q = ((x+1),(y+3))
    v = ((x-1),(y-3))
    w = (x,(y-3))
    z = ((x+1),(y-3))
    
    extra_nodes = [a,b,c,d,e,f,g,h,i,j,k,m,n,p,q,s,t,u,v,w,z]

    for node in extra_nodes:
        if node not in G.nodes:
            return False

    # check right river (e f m)
    #here we check that if we add the horizontal river, no nodes will become pooled

    #check if the nodes above or below have two river nodes next to each other
    right_river_check = True
    left_river_check = True

    if G.nodes[b]['type']=="river" and G.nodes[c]['type']=="river":
        right_river_check = False
    
    if G.nodes[c]['type']=="river" and G.nodes[j]['type']=="river":
        right_river_check = False
    
    if G.nodes[h]['type']=="river" and G.nodes[i]['type']=="river":
        right_river_check = False
    
    if G.nodes[i]['type']=="river" and G.nodes[p]['type']=="river":
        right_river_check = False
    
    # check beyond ones just above and below as well

    if G.nodes[d]['type']=="river" and G.nodes[a]['type']=="river" and G.nodes[b]['type']=="river":
        right_river_check = False
    
    if G.nodes[d]['type']=="river" and G.nodes[g]['type']=="river" and G.nodes[h]['type']=="river":
        right_river_check = False
    
    if G.nodes[j]['type']=="river" and G.nodes[k]['type']=="river" and G.nodes[n]['type']=="river":
        right_river_check = False
    
    if G.nodes[n]['type']=="river" and G.nodes[p]['type']=="river" and G.nodes[q]['type']=="river":
        right_river_check = False

    # left river checks

    if G.nodes[s]['type']=="river" and G.nodes[a]['type']=="river":
        left_river_check = False

    if G.nodes[a]['type']=="river" and G.nodes[b]['type']=="river":
        left_river_check = False
    
    if G.nodes[u]['type']=="river" and G.nodes[g]['type']=="river":
        left_river_check = False
    
    if G.nodes[g]['type']=="river" and G.nodes[h]['type']=="river":
        left_river_check = False

    # check beyond ones just above and below as well

    if G.nodes[v]['type']=="river" and G.nodes[s]['type']=="river" and G.nodes[w]['type']=="river":
        left_river_check = False
    
    if G.nodes[w]['type']=="river" and G.nodes[z]['type']=="river" and G.nodes[u]['type']=="river":
        left_river_check = False
    
    if G.nodes[h]['type']=="river" and G.nodes[i]['type']=="river" and G.nodes[f]['type']=="river":
        left_river_check = False
    
    if G.nodes[b]['type']=="river" and G.nodes[c]['type']=="river" and G.nodes[f]['type']=="river":
        left_river_check = False

    replaceable_types= ["grass","empty"]

    if G.nodes[f]['type'] not in replaceable_types or G.nodes[m]['type'] not in replaceable_types:
        right_river_check = False
    
    if G.nodes[t]['type'] not in replaceable_types or G.nodes[d]['type'] not in replaceable_types:
        left_river_check = False

    choices = []
    if right_river_check:
        choices.append("r")

    if left_river_check:
        choices.append("l")

    river = random.choice(choices)

    if river == "l":
        
        if G.nodes[d]['type']!="path":
            G.nodes[d]['type']="river"
        else:
            G.nodes[d]['type']="bridge"
        
        if G.nodes[t]['type']!="path":
            G.nodes[t]['type']="river"
        else:
            G.nodes[t]['type']="bridge"

        alongside_nodes = [a,g]
        grass_nodes=[u,h,s,b]

        print("make_horizontal_river(G,",source_node,") going to left")

    if river == "r":
            
        if G.nodes[m]['type']!="path":
            G.nodes[m]['type']="river"
        else:
            G.nodes[m]['type']="bridge"
        
        if G.nodes[f]['type']!="path":
            G.nodes[f]['type']="river"
        else:
            G.nodes[f]['type']="bridge"

        alongside_nodes = [c,i]
        grass_nodes=[b,j,h,p]
    
        print("make_horizontal_river(G,",source_node,") going to right")

    G.nodes[source_node]['type']="river"

    for node in alongside_nodes:
        if G.nodes[node]['type'] in replaceable_types:
            #G.nodes[node]['type']="irreplaceable_grass"
            G.nodes[node]['type']="grass"

    for node in grass_nodes:
        if G.nodes[node]['type'] in replaceable_types:
            G.nodes[node]['type']="grass"

    return G

def check_vertical_river(G,source_node):    

    """

    a0 b0 c0

    d0 e0 f0

    g0 h0 i0

    a  b  c

    d  e  f

    g  h  i

    a2 b2 c2

    d2 e2 f2

    g2 h2 i2

    """
    
    x,y = source_node

    a = ((x-1),(y-1))
    a0 = ((x-4),(y-1))
    a2 = ((x+2),(y-1))
    b = ((x-1),y)
    b0 = ((x-4),y)
    b2 = ((x+2),y)
    c = ((x-1),(y+1))
    c0 = ((x-4),(y+1))
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

    extra_nodes = [a,b,c,d,e,f,g,h,i,a0,b0,c0,d0,e0,f0,g0,h0,i0,a2,b2,c2,d2,e2,f2,g2,h2,i2]

    for node in extra_nodes:
        if node not in G.nodes:
            return False

    #here we check that if we add the vertical river, no nodes will become pooled

    #check if the nodes to the left or right have two river nodes next to each other
    
    # down river checks

    down_river_check = True

    if G.nodes[d]['type']=="river" and G.nodes[g]['type']=="river":
        print("fail d g")
        down_river_check = False
    #else:
      #  print("a is",G.nodes[a]['type'],"b is",G.nodes[b]['type'])
    
    if G.nodes[g]['type']=="river" and G.nodes[a2]['type']=="river":
        print("fail g a2")
        down_river_check = False
    
    if G.nodes[f]['type']=="river" and G.nodes[i]['type']=="river":
        print("fail f i")
        down_river_check = False
    
    if G.nodes[i]['type']=="river" and G.nodes[c2]['type']=="river":
        print("fail i c2")
        down_river_check = False
    
    # check beyond ones just above and below as well

    if G.nodes[a2]['type']=="river" and G.nodes[d2]['type']=="river" and G.nodes[e2]['type']=="river":
        down_river_check = False
    
    if G.nodes[c2]['type']=="river" and G.nodes[e2]['type']=="river" and G.nodes[f2]['type']=="river":
        down_river_check = False
    
    if G.nodes[a]['type']=="river" and G.nodes[b]['type']=="river" and G.nodes[d]['type']=="river":
        down_river_check = False
    
    if G.nodes[b]['type']=="river" and G.nodes[c]['type']=="river" and G.nodes[f]['type']=="river":
        down_river_check = False


    if G.nodes[a2]['type']=="river" and G.nodes[c2]['type']=="river":
        down_river_check = False
    
    if G.nodes[d]['type']=="river" and G.nodes[f]['type']=="river":
        down_river_check = False

    # up river checks

    up_river_check = True

    if G.nodes[a]['type']=="river" and G.nodes[d]['type']=="river":
        up_river_check = False
    #else:
      #  print("a is",G.nodes[a]['type'],"b is",G.nodes[b]['type'])
    
    if G.nodes[a]['type']=="river" and G.nodes[g0]['type']=="river":
        up_river_check = False
    
    if G.nodes[f]['type']=="river" and G.nodes[c]['type']=="river":
        up_river_check = False
    
    if G.nodes[c]['type']=="river" and G.nodes[i0]['type']=="river":
        up_river_check = False


        # check beyond ones just above and below as well

    if G.nodes[a]['type']=="river" and G.nodes[g0]['type']=="river" and G.nodes[h0]['type']=="river":
        up_river_check = False
    
    if G.nodes[h0]['type']=="river" and G.nodes[i0]['type']=="river" and G.nodes[c]['type']=="river":
        up_river_check = False
    
    if G.nodes[f]['type']=="river" and G.nodes[i]['type']=="river" and G.nodes[h]['type']=="river":
        up_river_check = False
    
    if G.nodes[d]['type']=="river" and G.nodes[g]['type']=="river" and G.nodes[h]['type']=="river":
        up_river_check = False

    # if G.nodes[g]['type']=="river" and G.nodes[i]['type']=="river":
    #     up_river_check = False

    if G.nodes[d]['type']=="river" and G.nodes[f]['type']=="river":
        up_river_check = False
    
    if G.nodes[g0]['type']=="river" and G.nodes[i0]['type']=="river":
        up_river_check = False


    replaceable_types= ["grass","empty"]


    if G.nodes[h]['type'] not in replaceable_types or G.nodes[b2]['type'] not in replaceable_types:
        down_river_check = False
    
    if G.nodes[b]['type'] not in replaceable_types or G.nodes[h0]['type'] not in replaceable_types:
        up_river_check = False


    if down_river_check or up_river_check:
        return True
        
    return False

def make_vertical_river(G,source_node):

    """

    a0 b0 c0

    d0 e0 f0

    g0 h0 i0

    a  b  c

    d  e  f

    g  h  i

    a2 b2 c2

    d2 e2 f2

    g2 h2 i2

    """


    x,y = source_node
    a = ((x-1),(y-1))
    a0 = ((x-4),(y-1))
    a2 = ((x+2),(y-1))
    b = ((x-1),y)
    b0 = ((x-4),y)
    b2 = ((x+2),y)
    c = ((x-1),(y+1))
    c0 = ((x-4),(y+1))
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

    #here we check that if we add the horizontal river, no nodes will become pooled

    #check if the nodes to the left or right have two river nodes next to each other
    
    # down river checks

    down_river_check = True
    up_river_check = True

    if G.nodes[d]['type']=="river" and G.nodes[g]['type']=="river":
       # print("fail d g")
        down_river_check = False
    #else:
      #  print("a is",G.nodes[a]['type'],"b is",G.nodes[b]['type'])
    
    if G.nodes[g]['type']=="river" and G.nodes[a2]['type']=="river":
      #  print("fail g a2")
        down_river_check = False
    
    if G.nodes[f]['type']=="river" and G.nodes[i]['type']=="river":
       # print("fail f i")
        down_river_check = False
    
    if G.nodes[i]['type']=="river" and G.nodes[c2]['type']=="river":
      #  print("fail i c2")
        down_river_check = False
    
    # check beyond ones just above and below as well

    if G.nodes[a2]['type']=="river" and G.nodes[d2]['type']=="river" and G.nodes[e2]['type']=="river":
        print("fail a2 d2")
        down_river_check = False
    
    if G.nodes[c2]['type']=="river" and G.nodes[e2]['type']=="river" and G.nodes[f2]['type']=="river":
        print("fail c2 e2")
        down_river_check = False
    
    if G.nodes[a]['type']=="river" and G.nodes[b]['type']=="river" and G.nodes[d]['type']=="river":
        print("fail a b")
        down_river_check = False
    
    if G.nodes[b]['type']=="river" and G.nodes[c]['type']=="river" and G.nodes[f]['type']=="river":
        print("fail b c")
        down_river_check = False

    # up river checks

    if G.nodes[a]['type']=="river" and G.nodes[d]['type']=="river":
        up_river_check = False

    
    if G.nodes[a]['type']=="river" and G.nodes[g0]['type']=="river":
        up_river_check = False
    
    if G.nodes[f]['type']=="river" and G.nodes[c]['type']=="river":
        up_river_check = False
    
    if G.nodes[c]['type']=="river" and G.nodes[i0]['type']=="river":
        up_river_check = False


        # check beyond ones just above and below as well

    if G.nodes[a]['type']=="river" and G.nodes[g0]['type']=="river" and G.nodes[h0]['type']=="river":
        up_river_check = False
    
    if G.nodes[h0]['type']=="river" and G.nodes[i0]['type']=="river" and G.nodes[c]['type']=="river":
        up_river_check = False
    
    if G.nodes[f]['type']=="river" and G.nodes[i]['type']=="river" and G.nodes[h]['type']=="river":
        up_river_check = False
    
    if G.nodes[d]['type']=="river" and G.nodes[g]['type']=="river" and G.nodes[h]['type']=="river":
        up_river_check = False


    replaceable_types= ["grass","empty"]


    if G.nodes[h]['type'] not in replaceable_types or G.nodes[b2]['type'] not in replaceable_types:
        down_river_check = False
    
    if G.nodes[b]['type'] not in replaceable_types or G.nodes[h0]['type'] not in replaceable_types:
        up_river_check = False

    choices = []

    if up_river_check:
        choices.append("u")

    if down_river_check:
        choices.append("d")

    try:

        choice = random.choice(choices)

    except:
        print("fuck")

    if choice == "u":
        alongside_nodes = [a,c]
        grass_nodes=[d,f,g0,i0]
        G.nodes[b]['type']="river"
        G.nodes[h0]['type']="river"

        print("make_vertical_river(G,",source_node,") going upwards")

    if choice == "d":
        alongside_nodes = [g,i]
        grass_nodes=[d,f,a2,c2]
        G.nodes[h]['type']="river"
        G.nodes[b2]['type']="river"

        print("make_vertical_river(G,",source_node,") going downwards")

    for node in alongside_nodes:
        if G.nodes[node]['type'] in replaceable_types:
            #G.nodes[node]['type']="irreplaceable_grass"
            G.nodes[node]['type']="grass"

    for node in grass_nodes:
        if G.nodes[node]['type'] in replaceable_types:
            G.nodes[node]['type']="grass"
    
    G.nodes[source_node]['type']="river"
    return G

def check_river_bridge(G, source_node):

    x,y = source_node

    a = ((x-1),(y-1))
    a2 = ((x+2),(y-1))
    b = ((x-1),y)
    b2 = ((x+2),y)
    c = ((x-1),(y+1))
    c2 = ((x+2),(y+1))
    d = (x,(y-1))
    d2 = (x+3,(y-1))
    e = source_node
    e0= ((x-3),y)
    e2 = ((x+3),(y))
    f = (x,(y+1))
    f2 = (x+3,(y+1))
    g = ((x+1),(y-1))
    g0 = ((x-2),(y-1))
    h = ((x+1),y)
    h0 = ((x-2),y)
    i = ((x+1),(y+1))
    i0 = ((x-2),(y+1))

    s = ((x-1),(y-2))

    j = ((x-1),(y+2))

    u = ((x+1),(y-2))

    p = ((x+1),(y+2))


    replaceable_types = ["grass","empty"]

    nodes_to_check =[a,a2,b,b2,c,c2,d,d2,f,f2,g,g0,h,h0,i,i0]

    for node in nodes_to_check:
        if node not in G.nodes:
            return False
        
        
    down_river_check = True
    up_river_check = True

    if G.nodes[d]['type']=="river" and G.nodes[g]['type']=="river":
        down_river_check = False

    if G.nodes[g]['type']=="river" and G.nodes[a2]['type']=="river":
        down_river_check = False
    
    if G.nodes[f]['type']=="river" and G.nodes[i]['type']=="river":
        down_river_check = False
    
    if G.nodes[i]['type']=="river" and G.nodes[c2]['type']=="river":
        down_river_check = False
    
    # check beyond ones just above and below as well

    if G.nodes[a2]['type']=="river" and G.nodes[d2]['type']=="river" and G.nodes[e2]['type']=="river":
        down_river_check = False
    
    if G.nodes[c2]['type']=="river" and G.nodes[e2]['type']=="river" and G.nodes[f2]['type']=="river":
        down_river_check = False
    
    if G.nodes[a]['type']=="river" and G.nodes[b]['type']=="river" and G.nodes[d]['type']=="river":
        down_river_check = False
    
    if G.nodes[b]['type']=="river" and G.nodes[c]['type']=="river" and G.nodes[f]['type']=="river":
        down_river_check = False

    if u in G.nodes:
        if G.nodes[u]['type']=="river":
            down_river_check = False


    if p in G.nodes:
        if G.nodes[p]['type']=="river":
            down_river_check = False

    # up river checks

    if G.nodes[a]['type']=="river" and G.nodes[d]['type']=="river":
        up_river_check = False

    
    if G.nodes[a]['type']=="river" and G.nodes[g0]['type']=="river":
        up_river_check = False
    
    if G.nodes[f]['type']=="river" and G.nodes[c]['type']=="river":
        up_river_check = False
    
    if G.nodes[c]['type']=="river" and G.nodes[i0]['type']=="river":
        up_river_check = False


        # check beyond ones just above and below as well

    if G.nodes[a]['type']=="river" and G.nodes[g0]['type']=="river" and G.nodes[h0]['type']=="river":
        up_river_check = False
    
    if G.nodes[h0]['type']=="river" and G.nodes[i0]['type']=="river" and G.nodes[c]['type']=="river":
        up_river_check = False
    
    if G.nodes[f]['type']=="river" and G.nodes[i]['type']=="river" and G.nodes[h]['type']=="river":
        up_river_check = False
    
    if G.nodes[d]['type']=="river" and G.nodes[g]['type']=="river" and G.nodes[h]['type']=="river":
        up_river_check = False

    if g0 in G.nodes:
        if G.nodes[g0]['type']=="river":
            up_river_check = False

    
    if i0 in G.nodes:
        if G.nodes[g0]['type']=="river":
            up_river_check = False


    replaceable_types= ["grass","empty"]


    if G.nodes[h]['type'] not in replaceable_types or G.nodes[b2]['type'] not in replaceable_types:
        down_river_check = False

    
    if G.nodes[b]['type'] not in replaceable_types or G.nodes[h0]['type'] not in replaceable_types:
        up_river_check = False

    choices = []

    if up_river_check:
        choices.append("u")

    if down_river_check:
        choices.append("d")

    if len(choices)==0:
        return False

    if G.nodes[d]['type']=="river" or G.nodes[f]['type']=="river":
        return False
    
    bad_types=["river","bridge"]

    choice = random.choice(choices)

    if choice == "u":

        if G.nodes[a]['type'] in replaceable_types and G.nodes[c]['type']in replaceable_types:
            if G.nodes[g0]['type']!="river" and G.nodes[i0]['type']!="river":
                if G.nodes[h0]['type']!="bridge" and G.nodes[e0]['type']!="bridge" and G.nodes[b]['type']!="bridge":
                    if G.nodes[e]['type']!="bridge" and G.nodes[h]['type']!="bridge" and G.nodes[b2]['type']!="bridge":
                        if G.nodes[s]['type'] not in bad_types  and G.nodes[j]['type']not in bad_types:
                            return True


    if choice == "d":
        if G.nodes[g]['type'] in replaceable_types and G.nodes[i]['type'] in replaceable_types:
            if G.nodes[a2]['type']!="river" and G.nodes[c2]['type']!="river":
                if G.nodes[b2]['type']!="bridge" and G.nodes[e2]['type']!="bridge" and G.nodes[h]['type']!="bridge":
                    if G.nodes[e]['type']!="bridge" and G.nodes[b]['type']!="bridge" and G.nodes[h0]['type']!="bridge":
                        if G.nodes[u]['type'] not in bad_types and G.nodes[p]['type'] not in bad_types :
                            return True

    return False

def make_river_bridge(G, source_node):

    x,y = source_node
    a = ((x-1),(y-1))
    a0 = ((x-4),(y-1))
    a2 = ((x+2),(y-1))
    b = ((x-1),y)
    b0 = ((x-4),y)
    b2 = ((x+2),y)
    c = ((x-1),(y+1))
    c0 = ((x-4),(y+1))
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

    replaceable = ["grass","empty","river"]

    nodes_to_check =[]

    for node in nodes_to_check:
        if node not in G.nodes:
            return False
        
    down_river_check = True
    up_river_check = True

    if G.nodes[d]['type']=="river" and G.nodes[g]['type']=="river":
       # print("fail d g")
        down_river_check = False
    #else:
      #  print("a is",G.nodes[a]['type'],"b is",G.nodes[b]['type'])
    
    if G.nodes[g]['type']=="river" and G.nodes[a2]['type']=="river":
      #  print("fail g a2")
        down_river_check = False
    
    if G.nodes[f]['type']=="river" and G.nodes[i]['type']=="river":
       # print("fail f i")
        down_river_check = False
    
    if G.nodes[i]['type']=="river" and G.nodes[c2]['type']=="river":
      #  print("fail i c2")
        down_river_check = False
    
    # check beyond ones just above and below as well

    if G.nodes[a2]['type']=="river" and G.nodes[d2]['type']=="river" and G.nodes[e2]['type']=="river":
        print("fail a2 d2")
        down_river_check = False
    
    if G.nodes[c2]['type']=="river" and G.nodes[e2]['type']=="river" and G.nodes[f2]['type']=="river":
        print("fail c2 e2")
        down_river_check = False
    
    if G.nodes[a]['type']=="river" and G.nodes[b]['type']=="river" and G.nodes[d]['type']=="river":
        print("fail a b")
        down_river_check = False
    
    if G.nodes[b]['type']=="river" and G.nodes[c]['type']=="river" and G.nodes[f]['type']=="river":
        print("fail b c")
        down_river_check = False

    # up river checks

    if G.nodes[a]['type']=="river" and G.nodes[d]['type']=="river":
        up_river_check = False

    
    if G.nodes[a]['type']=="river" and G.nodes[g0]['type']=="river":
        up_river_check = False
    
    if G.nodes[f]['type']=="river" and G.nodes[c]['type']=="river":
        up_river_check = False
    
    if G.nodes[c]['type']=="river" and G.nodes[i0]['type']=="river":
        up_river_check = False


        # check beyond ones just above and below as well

    if G.nodes[a]['type']=="river" and G.nodes[g0]['type']=="river" and G.nodes[h0]['type']=="river":
        up_river_check = False
    
    if G.nodes[h0]['type']=="river" and G.nodes[i0]['type']=="river" and G.nodes[c]['type']=="river":
        up_river_check = False
    
    if G.nodes[f]['type']=="river" and G.nodes[i]['type']=="river" and G.nodes[h]['type']=="river":
        up_river_check = False
    
    if G.nodes[d]['type']=="river" and G.nodes[g]['type']=="river" and G.nodes[h]['type']=="river":
        up_river_check = False


    replaceable_types= ["grass","empty"]


    if G.nodes[h]['type'] not in replaceable_types or G.nodes[b2]['type'] not in replaceable_types:
        down_river_check = False
    
    if G.nodes[b]['type'] not in replaceable_types or G.nodes[h0]['type'] not in replaceable_types:
        up_river_check = False

    choices = []

    if up_river_check:
        choices.append("u")

    if down_river_check:
        choices.append("d")

    choice = random.choice(choices)

    if choice=="u":

        G.nodes[b]['type']="bridge"
        G.nodes[h0]['type']="river"
        G.nodes[e]['type']="river"
        G.nodes[a]['type']="path"
        G.nodes[c]['type']="path"
        print("Making vertical bridged river")

    else:
        G.nodes[h]['type']="bridge"
        G.nodes[b2]['type']="river"
        G.nodes[e]['type']="river"
        G.nodes[g]['type']="path"
        G.nodes[i]['type']="path"
        print("Making vertical bridged river")
    return G

def check_long_vertical_river(G,source_node):    

    """

    a0 b0 c0

    d0 e0 f0

    g0 h0 i0

    a  b  c

    d  e  f

    g  h  i

    a2 b2 c2

    d2 e2 f2

    g2 h2 i2

    """
    
    x,y = source_node

    a = ((x-1),(y-1))
    a0 = ((x-4),(y-1))
    a2 = ((x+2),(y-1))
    b = ((x-1),y)
    b0 = ((x-4),y)
    b2 = ((x+2),y)
    c = ((x-1),(y+1))
    c0 = ((x-4),(y+1))
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

    extra_nodes = [a,b,c,d,e,f,g,h,i,a0,b0,c0,d0,e0,f0,g0,h0,i0,a2,b2,c2,d2,e2,f2,g2,h2,i2]

    for node in extra_nodes:
        if node not in G.nodes:
            return False

    #here we check that if we add the vertical river, no nodes will become pooled

    #check if the nodes to the left or right have two river nodes next to each other
    
    # down river checks

    down_river_check = True

    if G.nodes[d]['type']=="river" and G.nodes[g]['type']=="river":
        down_river_check = False
    
    if G.nodes[g]['type']=="river" and G.nodes[a2]['type']=="river":
        down_river_check = False

    if G.nodes[a2]['type']=="river" and G.nodes[d2]['type']=="river":
        down_river_check = False

    if G.nodes[f]['type']=="river" and G.nodes[i]['type']=="river":
        down_river_check = False
    
    if G.nodes[i]['type']=="river" and G.nodes[c2]['type']=="river":
        down_river_check = False

    if G.nodes[c2]['type']=="river" and G.nodes[f2]['type']=="river":
        down_river_check = False
    
    # check beyond ones just above and below as well

    if G.nodes[d2]['type']=="river" and G.nodes[g2]['type']=="river" and G.nodes[h2]['type']=="river":
        down_river_check = False
    
    if G.nodes[f2]['type']=="river" and G.nodes[i2]['type']=="river" and G.nodes[h2]['type']=="river":
        down_river_check = False
    
    if G.nodes[a]['type']=="river" and G.nodes[b]['type']=="river" and G.nodes[d]['type']=="river":
        down_river_check = False
    
    if G.nodes[b]['type']=="river" and G.nodes[c]['type']=="river" and G.nodes[f]['type']=="river":
        down_river_check = False

    if G.nodes[d2]['type']=="river" and G.nodes[f2]['type']=="river":
        down_river_check = False
    
    if G.nodes[d]['type']=="river" and G.nodes[f]['type']=="river":
        down_river_check = False

    # up river checks

    up_river_check = True

    if G.nodes[a]['type']=="river" and G.nodes[d]['type']=="river":
        up_river_check = False
    
    if G.nodes[a]['type']=="river" and G.nodes[g0]['type']=="river":
        up_river_check = False

    if G.nodes[g0]['type']=="river" and G.nodes[d0]['type']=="river":
        up_river_check = False
    
    if G.nodes[f]['type']=="river" and G.nodes[c]['type']=="river":
        up_river_check = False
    
    if G.nodes[c]['type']=="river" and G.nodes[i0]['type']=="river":
        up_river_check = False

    if G.nodes[i0]['type']=="river" and G.nodes[f0]['type']=="river":
        up_river_check = False

        # check beyond ones just above and below as well

    if G.nodes[a0]['type']=="river" and G.nodes[b0]['type']=="river" and G.nodes[d0]['type']=="river":
        up_river_check = False
    
    if G.nodes[b0]['type']=="river" and G.nodes[c0]['type']=="river" and G.nodes[f0]['type']=="river":
        up_river_check = False
    
    if G.nodes[f]['type']=="river" and G.nodes[i]['type']=="river" and G.nodes[h]['type']=="river":
        up_river_check = False
    
    if G.nodes[d]['type']=="river" and G.nodes[g]['type']=="river" and G.nodes[h]['type']=="river":
        up_river_check = False

    if G.nodes[d]['type']=="river" and G.nodes[f]['type']=="river":
        up_river_check = False
    
    if G.nodes[g0]['type']=="river" and G.nodes[i0]['type']=="river":
        up_river_check = False


    replaceable_types= ["grass","empty"]


    if G.nodes[h]['type'] not in replaceable_types or G.nodes[b2]['type'] not in replaceable_types:
        down_river_check = False
    
    if G.nodes[b]['type'] not in replaceable_types or G.nodes[h0]['type'] not in replaceable_types:
        up_river_check = False


    if down_river_check or up_river_check:
        return True
        
    return False

def make_vertical_river(G,source_node):

    """

    a0 b0 c0

    d0 e0 f0

    g0 h0 i0

    a  b  c

    d  e  f

    g  h  i

    a2 b2 c2

    d2 e2 f2

    g2 h2 i2

    """


    x,y = source_node
    a = ((x-1),(y-1))
    a0 = ((x-4),(y-1))
    a2 = ((x+2),(y-1))
    b = ((x-1),y)
    b0 = ((x-4),y)
    b2 = ((x+2),y)
    c = ((x-1),(y+1))
    c0 = ((x-4),(y+1))
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

    #here we check that if we add the horizontal river, no nodes will become pooled

    #check if the nodes to the left or right have two river nodes next to each other
    
    # down river checks

    down_river_check = True
    up_river_check = True

    if G.nodes[d]['type']=="river" and G.nodes[g]['type']=="river":
       # print("fail d g")
        down_river_check = False
    #else:
      #  print("a is",G.nodes[a]['type'],"b is",G.nodes[b]['type'])
    
    if G.nodes[g]['type']=="river" and G.nodes[a2]['type']=="river":
      #  print("fail g a2")
        down_river_check = False
    
    if G.nodes[f]['type']=="river" and G.nodes[i]['type']=="river":
       # print("fail f i")
        down_river_check = False
    
    if G.nodes[i]['type']=="river" and G.nodes[c2]['type']=="river":
      #  print("fail i c2")
        down_river_check = False
    
    # check beyond ones just above and below as well

    if G.nodes[a2]['type']=="river" and G.nodes[d2]['type']=="river" and G.nodes[e2]['type']=="river":
        print("fail a2 d2")
        down_river_check = False
    
    if G.nodes[c2]['type']=="river" and G.nodes[e2]['type']=="river" and G.nodes[f2]['type']=="river":
        print("fail c2 e2")
        down_river_check = False
    
    if G.nodes[a]['type']=="river" and G.nodes[b]['type']=="river" and G.nodes[d]['type']=="river":
        print("fail a b")
        down_river_check = False
    
    if G.nodes[b]['type']=="river" and G.nodes[c]['type']=="river" and G.nodes[f]['type']=="river":
        print("fail b c")
        down_river_check = False

    # up river checks

    if G.nodes[a]['type']=="river" and G.nodes[d]['type']=="river":
        up_river_check = False

    
    if G.nodes[a]['type']=="river" and G.nodes[g0]['type']=="river":
        up_river_check = False
    
    if G.nodes[f]['type']=="river" and G.nodes[c]['type']=="river":
        up_river_check = False
    
    if G.nodes[c]['type']=="river" and G.nodes[i0]['type']=="river":
        up_river_check = False


        # check beyond ones just above and below as well

    if G.nodes[a]['type']=="river" and G.nodes[g0]['type']=="river" and G.nodes[h0]['type']=="river":
        up_river_check = False
    
    if G.nodes[h0]['type']=="river" and G.nodes[i0]['type']=="river" and G.nodes[c]['type']=="river":
        up_river_check = False
    
    if G.nodes[f]['type']=="river" and G.nodes[i]['type']=="river" and G.nodes[h]['type']=="river":
        up_river_check = False
    
    if G.nodes[d]['type']=="river" and G.nodes[g]['type']=="river" and G.nodes[h]['type']=="river":
        up_river_check = False


    replaceable_types= ["grass","empty"]


    if G.nodes[h]['type'] not in replaceable_types or G.nodes[b2]['type'] not in replaceable_types:
        down_river_check = False
    
    if G.nodes[b]['type'] not in replaceable_types or G.nodes[h0]['type'] not in replaceable_types:
        up_river_check = False

    choices = []

    if up_river_check:
        choices.append("u")

    if down_river_check:
        choices.append("d")

    choice = random.choice(choices)

    if choice == "u":
        alongside_nodes = [a,c]
        grass_nodes=[d,f,g0,i0]
        G.nodes[b]['type']="river"
        G.nodes[h0]['type']="river"

        print("make_vertical_river(G,",source_node,") going upwards")

    if choice == "d":
        alongside_nodes = [g,i]
        grass_nodes=[d,f,a2,c2]
        G.nodes[h]['type']="river"
        G.nodes[b2]['type']="river"

        print("make_vertical_river(G,",source_node,") going downwards")

    for node in alongside_nodes:
        if G.nodes[node]['type'] in replaceable_types:
            #G.nodes[node]['type']="irreplaceable_grass"
            G.nodes[node]['type']="grass"

    for node in grass_nodes:
        if G.nodes[node]['type'] in replaceable_types:
            G.nodes[node]['type']="grass"
    
    G.nodes[source_node]['type']="river"
    return G
