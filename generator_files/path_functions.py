"""
path

Functions for checking and creating path-related features.

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

def path_matchmaker(G,source_node):

    path_dict = {

        "make_path_L_bend":2,
        "make_t_junction":1,
        "make_forked_road":4,
        "make_horizontal_path":2,
        "make_vertical_path":2,
        "make_castle":8,
        "make_large_castle":13,
        "make_house":10

    }

    possible_replacements = []

    if check_path_L_bend(G,source_node):
        possible_replacements.append("make_path_L_bend")

    if check_t_junction(G,source_node):
        possible_replacements.append("make_t_junction")

    # if check_forked_road(G,source_node):
    #     possible_replacements.append("make_forked_road")

    if check_horizontal_path(G,source_node):
        possible_replacements.append("make_horizontal_path")
    
    if check_vertical_path(G,source_node):
        possible_replacements.append("make_vertical_path")

    if check_castle(G,source_node):
        possible_replacements.append("make_castle")

    if check_large_castle(G,source_node):
        possible_replacements.append("make_large_castle")

    if check_house(G,source_node):
        possible_replacements.append("make_house")

    if len(possible_replacements)>0:
        probabilities = probability_generator(path_dict,possible_replacements)
        return random.choices(possible_replacements, weights=probabilities, k=1)[0]

    else:

        return None

def check_path_L_bend(G, source_node):

    """
    checking for something like this
      #
    # #
    # <- source node
    
    """
    node_type = nx.get_node_attributes(G, 'type')

    x,y = source_node

    a = ((x-1),(y-1))
    b = ((x-1),y)
    c = ((x-1),(y+1))
    d = (x,(y-1))
    e = source_node
    f = (x,(y+1))
    g = ((x+1),(y-1))
    h = ((x+1),y)
    i = ((x+1),(y+1))

    adjacent_nodes = [a,b,c,d,f,g,i] #excluding h because it can be path too

    allowed_types = ["grass","empty"]

    allowed_types_h = ["grass","empty","path"]

    if G.nodes[h]['type'] in allowed_types_h and h in G.nodes:

        for node in adjacent_nodes:
            if (node in G.nodes) and (G.nodes[node]['type'] in allowed_types):
                continue
            else:
                return False
        
    else:
        return False


    return True

def make_path_L_bend(G, source_node):

    node_type = nx.get_node_attributes(G, 'type')
    
    x, y = source_node

    a = ((x-1),(y-1))
    b = ((x-1),y)
    c = ((x-1),(y+1))
    d = (x,(y-1))
    e = source_node
    f = (x,(y+1))
    g = ((x+1),(y-1))
    h = ((x+1),y)
    i = ((x+1),(y+1))

    total_list = [a,b,c,d,f,g,h,i]
    choice_list = [1,2,3]

    choice = random.choice(choice_list)

    total_list = [a,b,c,d,f,g,h,i]

    if choice==1:
        
        path_list = [e,a,b,i,h]

    elif choice == 2:

        path_list = [e,b,c,g,h]

    elif choice == 3:

        path_list = [e,c,f,g,h]


    for node in path_list:
        if node in G.nodes:
            G.nodes[node]['type']="path"

    other_list = list(set(total_list).difference(path_list))

    for node in other_list:
        if node in G.nodes and G.nodes[node]['type']!="path":
            G.nodes[node]['type']="grass"

    node_type = nx.get_node_attributes(G, 'type')

    return G     

def check_t_junction(G,source_node):

    
    """
    checking for something like this

        # # #
          #
          #
    
    """

    x,y = source_node

    a = ((x-1),(y-1))
    b = ((x-1),y)
    c = ((x-1),(y+1))
    d = (x,(y-1))
    e = source_node
    f = (x,(y+1))
    g = ((x+1),(y-1))
    h = ((x+1),y)
    i = ((x+1),(y+1))

    adjacent_nodes = [a,b,c,d,f,g,i] #excluding h because it can be path too, and e is source

    allowed_types = ["grass","empty"]

    allowed_types_h = ["grass","empty","path"]

    if h in G.nodes and G.nodes[h]['type'] in allowed_types_h:
        for node in adjacent_nodes:
            if (node in G.nodes) and (G.nodes[node]['type'] in allowed_types):
                continue
            else:
                return False
        
    else:
        return False


    return True

def make_t_junction(G, source_node):

    x, y = source_node

    a = ((x-1),(y-1))
    b = ((x-1),y)
    c = ((x-1),(y+1))
    d = (x,(y-1))
    e = source_node
    f = (x,(y+1))
    g = ((x+1),(y-1))
    h = ((x+1),y)
    i = ((x+1),(y+1))

    total_list = [a,b,c,d,f,g,h,i]
    path_list = [a,b,c,h]

    for node in path_list:
        G.nodes[node]['type']="path"

    other_list = list(set(total_list).difference(path_list))

    for node in other_list:
        if G.nodes[node]['type']=="empty":
            G.nodes[node]['type']="grass"

    if G.nodes[source_node]['type']!="bridge":
        G.nodes[source_node]['type']="path"
    node_type = nx.get_node_attributes(G, 'type')
    

    #print("Making a t-junction with source",source_node)
    print("make_t_junction(G,",source_node,")")

    return G


def check_forked_road(G,source_node):

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


    # extra_nodes = [a,b,c,d,e,f,g,h,i,j,k,m,n,p,q,s,t,u,v,w,z]

    # for node in extra_nodes:
    #     if node not in G.nodes:
    #         return False

    replaceable_types = ["grass","empty","river","bridge","path","irreplaceable_grass"]
    fork_nodes=[e,b,h0,d0,f0,a1,c1]
    surrounding_nodes=[a,c,i0,g0,d1,f1]

    river_check=False
    river_nodes=[]

    for node in surrounding_nodes:
        if node not in G.nodes:
            return False
        if G.nodes[node]['type']=="path":
            print("Fork failed bc surrounding path")
            return False

    for node in fork_nodes:
        # print("Fork type",G.nodes[node]["type"])
        if G.nodes[node]['type'] not in replaceable_types:
            print("Fork failed bc of replaceable types")
            return False
        if G.nodes[node]['type']=="river":
            river_nodes.append(node)
            river_check=True
    
    if river_check:

        for node in river_nodes:

            xr,yr = node
            left= (xr,(yr-1))
            right = (xr,(yr+1))
            up = ((xr-1),yr)
            down = ((xr+1),yr)

            if G.nodes[up]['type']=="river" and G.nodes[down]['type']=="river":
                print("Fork failed in up down river")
                return False

            elif G.nodes[left]['type']=="river" and G.nodes[right]['type']=="river":
                
                continue

            else:
                print("Fork failed in left right river")
                return False
    
    return True

def make_forked_road(G, source_node):

    x,y = source_node
    
    a = ((x-1),(y-1))
    a0 = ((x-4),(y-1))
    a2 = ((x+2),(y-1))    
    a1=  ((x-4),(y-2))
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
    d1=(x-3,(y-2))
    f1 = (x-3,(y+2))

    # extra_nodes = [a,b,c,d,e,f,g,h,i,j,k,m,n,p,q,s,t,u,v,w,z]

    # for node in extra_nodes:
    #     if node not in G.nodes:
    #         return False

    replaceable_types = ["grass","empty","river","irreplaceable_grass"]
    fork_nodes=[b,h0,d0,f0,a1,c1,e]
    grass_nodes=[a0,b0,c0,e0]
    surrounding_nodes=[a,c,g0,d1,f1]

    for node in surrounding_nodes:
        if G.nodes[node]['type'] =="grass" or G.nodes[node]['type']=="empty":
            G.nodes[node]['type']=="irreplaceable_grass"
    for node in grass_nodes:
        G.nodes[node]['type']="grass"

    for node in fork_nodes:
        if G.nodes[node]['type']=="river":
            xr,yr = node
            left= (xr,(yr-1))
            right = (xr,(yr+1))
            
            if G.nodes[left]['type']=="river" and G.nodes[right]['type']=="river":
                
                G.nodes[node]['type']="bridge"
            
            else:
                G.nodes[node]['type']="path"
                
        else:
            G.nodes[node]['type']="path"
    print("make_forked_road(G,",source_node,")")
    return G


def check_horizontal_path(G,source_node):
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

    # check right path (e f m)
    #here we check that if we add the horizontal path, no nodes will become pooled

    #check if the nodes above or below have two path nodes next to each other
    right_path_check = True
    left_path_check = True

    if G.nodes[b]['type']=="path" and G.nodes[c]['type']=="path":
        right_path_check = False
    #else:
      #  print("a is",G.nodes[a]['type'],"b is",G.nodes[b]['type'])
    
    if G.nodes[c]['type']=="path" and G.nodes[j]['type']=="path":
        right_path_check = False
    
    if G.nodes[h]['type']=="path" and G.nodes[i]['type']=="path":
        right_path_check = False
    
    if G.nodes[i]['type']=="path" and G.nodes[p]['type']=="path":
        right_path_check = False
    
    # check beyond ones just above and below as well

    if G.nodes[d]['type']=="path" and G.nodes[a]['type']=="path" and G.nodes[b]['type']=="path":
        right_path_check = False
    
    if G.nodes[d]['type']=="path" and G.nodes[g]['type']=="path" and G.nodes[h]['type']=="path":
        right_path_check = False
    
    if G.nodes[j]['type']=="path" and G.nodes[k]['type']=="path" and G.nodes[n]['type']=="path":
        right_path_check = False
    
    if G.nodes[n]['type']=="path" and G.nodes[p]['type']=="path" and G.nodes[q]['type']=="path":
        right_path_check = False

    if G.nodes[j]['type']=="path" and G.nodes[p]['type']=="path":
        right_path_check = False
    
    if G.nodes[b]['type']=="path" and G.nodes[h]['type']=="path":
        right_path_check = False



    # left path checks


    if G.nodes[s]['type']=="path" and G.nodes[a]['type']=="path":
        left_path_check = False
    #else:
      #  print("a is",G.nodes[a]['type'],"b is",G.nodes[b]['type'])
    
    if G.nodes[a]['type']=="path" and G.nodes[b]['type']=="path":
        left_path_check = False
    
    if G.nodes[u]['type']=="path" and G.nodes[g]['type']=="path":
        left_path_check = False
    
    if G.nodes[g]['type']=="path" and G.nodes[h]['type']=="path":
        left_path_check = False


        # check beyond ones just above and below as well

    if G.nodes[v]['type']=="path" and G.nodes[s]['type']=="path" and G.nodes[w]['type']=="path":
        left_path_check = False
    
    if G.nodes[w]['type']=="path" and G.nodes[z]['type']=="path" and G.nodes[u]['type']=="path":
        left_path_check = False
    
    if G.nodes[h]['type']=="path" and G.nodes[i]['type']=="path" and G.nodes[f]['type']=="path":
        left_path_check = False
    
    if G.nodes[b]['type']=="path" and G.nodes[c]['type']=="path" and G.nodes[f]['type']=="path":
        left_path_check = False

    
    if G.nodes[s]['type']=="path" and G.nodes[u]['type']=="path":
        left_path_check = False
    
    if G.nodes[b]['type']=="path" and G.nodes[h]['type']=="path":
        left_path_check = False


    replaceable_types= ["grass","empty"]

   # allowed_types = ["grass","empty","house","path"]

  #  adjacent_nodes = [a,b,c,d,f,g,h,i]

    # below we see if we can place the path legally, and we account for when we can place the path with a bridge

    if G.nodes[f]['type'] not in replaceable_types or G.nodes[m]['type'] not in replaceable_types:
        if G.nodes[f]['type']=="river" and G.nodes[m]['type'] in replaceable_types:
            right_path_check=True
        else:
            right_path_check = False
    
    if G.nodes[t]['type'] not in replaceable_types or G.nodes[d]['type'] not in replaceable_types:
        if G.nodes[t]['type'] in replaceable_types and G.nodes[d]['type']=="river":
            left_path_check=True
        else:
            left_path_check = False


    if right_path_check or left_path_check:
        return True
        
    return False

def make_horizontal_path(G, source_node):

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

    # check right path (e f m)
    #here we check that if we add the horizontal path, no nodes will become pooled

    #check if the nodes above or below have two path nodes next to each other
    right_path_check = True
    left_path_check = True

    if G.nodes[b]['type']=="path" and G.nodes[c]['type']=="path":
        right_path_check = False
    #else:
      #  print("a is",G.nodes[a]['type'],"b is",G.nodes[b]['type'])
    
    if G.nodes[c]['type']=="path" and G.nodes[j]['type']=="path":
        right_path_check = False
    
    if G.nodes[h]['type']=="path" and G.nodes[i]['type']=="path":
        right_path_check = False
    
    if G.nodes[i]['type']=="path" and G.nodes[p]['type']=="path":
        right_path_check = False
    
    # check beyond ones just above and below as well

    if G.nodes[d]['type']=="path" and G.nodes[a]['type']=="path" and G.nodes[b]['type']=="path":
        right_path_check = False
    
    if G.nodes[d]['type']=="path" and G.nodes[g]['type']=="path" and G.nodes[h]['type']=="path":
        right_path_check = False
    
    if G.nodes[j]['type']=="path" and G.nodes[k]['type']=="path" and G.nodes[n]['type']=="path":
        right_path_check = False
    
    if G.nodes[n]['type']=="path" and G.nodes[p]['type']=="path" and G.nodes[q]['type']=="path":
        right_path_check = False

    # left path checks


    if G.nodes[s]['type']=="path" and G.nodes[a]['type']=="path":
        left_path_check = False
    #else:
      #  print("a is",G.nodes[a]['type'],"b is",G.nodes[b]['type'])
    
    if G.nodes[a]['type']=="path" and G.nodes[b]['type']=="path":
        left_path_check = False
    
    if G.nodes[u]['type']=="path" and G.nodes[g]['type']=="path":
        left_path_check = False
    
    if G.nodes[g]['type']=="path" and G.nodes[h]['type']=="path":
        left_path_check = False


        # check beyond ones just above and below as well

    if G.nodes[v]['type']=="path" and G.nodes[s]['type']=="path" and G.nodes[w]['type']=="path":
        left_path_check = False
    
    if G.nodes[w]['type']=="path" and G.nodes[z]['type']=="path" and G.nodes[u]['type']=="path":
        left_path_check = False
    
    if G.nodes[h]['type']=="path" and G.nodes[i]['type']=="path" and G.nodes[f]['type']=="path":
        left_path_check = False
    
    if G.nodes[b]['type']=="path" and G.nodes[c]['type']=="path" and G.nodes[f]['type']=="path":
        left_path_check = False

    replaceable_types= ["grass","empty"]

   # allowed_types = ["grass","empty","house","path"]

  #  adjacent_nodes = [a,b,c,d,f,g,h,i]

    if G.nodes[f]['type'] not in replaceable_types or G.nodes[m]['type'] not in replaceable_types:
        if G.nodes[f]['type']=="river" and G.nodes[m]['type'] in replaceable_types:
            right_path_check=True
        else:
            right_path_check = False
    
    if G.nodes[t]['type'] not in replaceable_types or G.nodes[d]['type'] not in replaceable_types:
        if G.nodes[t]['type'] in replaceable_types and G.nodes[d]['type']=="river":
            left_path_check=True
        else:
            left_path_check = False

    choices = []
    if right_path_check:
        choices.append("r")

    if left_path_check:
        choices.append("l")

    path = random.choice(choices)

    if path == "l":
        alongside_nodes=[a,g]
        grass_nodes=[s,b,u,h]
        if G.nodes[d]['type']=="river":
            G.nodes[d]['type']="bridge"
        else:
            G.nodes[d]['type']="path"
        G.nodes[t]['type']="path"
        print("make_horizontal_path(G,",source_node,") going left")
        #print("Making a left horizontal path and replacing",t,"and",d,"with source",source_node)

    if path == "r":
        alongside_nodes = [c,i]
        grass_nodes =[b,j,h,p]
        G.nodes[m]['type']="path"
        if G.nodes[f]['type']=="river":
            G.nodes[f]['type']="bridge"
        else:
            G.nodes[f]['type']="path"
        print("make_horizontal_path(G,",source_node,") going right")
        #print("Making a right horizontal path and replacing",f,"and",m,"with source",source_node)

    for node in alongside_nodes:
        if G.nodes[node]['type'] in replaceable_types:
            G.nodes[node]['type']="irreplaceable_grass"

    for node in grass_nodes:
        if G.nodes[node]['type'] in replaceable_types:
            G.nodes[node]['type']="grass"

    if G.nodes[source_node]['type']!="bridge":
        G.nodes[source_node]['type']="path"
    node_type = nx.get_node_attributes(G, 'type')

    return G

def check_vertical_path(G,source_node):    

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
        
    up_side_nodes = [g0,a,d,f,c,i0]

    down_side_nodes = [d,g,a2,f,i,c2]

    #here we check that if we add the horizontal path, no nodes will become pooled

    #check if the nodes to the left or right have two path nodes next to each other
    
    # down path checks

    down_path_check = True
    up_path_check = True

    up_side_nodes = [g0,a,d,f,c,i0]

    down_side_nodes = [d,g,a2,f,i,c2]

    # for node in up_side_nodes:
    #     if count_neighbours(G,source_node,"river")>2:
    #         up_path_check=False

    # for node in down_side_nodes:
    #     if count_neighbours(G,source_node,"river")>2:
    #         down_path_check=False

    if G.nodes[d]['type']=="path" and G.nodes[g]['type']=="path":
        down_path_check = False
    #else:
      #  print("a is",G.nodes[a]['type'],"b is",G.nodes[b]['type'])
    
    if G.nodes[g]['type']=="path" and G.nodes[a2]['type']=="path":
        down_path_check = False
    
    if G.nodes[f]['type']=="path" and G.nodes[i]['type']=="path":
        down_path_check = False
    
    if G.nodes[i]['type']=="path" and G.nodes[c2]['type']=="path":
        down_path_check = False
    
    # check beyond ones just above and below as well

    if G.nodes[a2]['type']=="path" and G.nodes[d2]['type']=="path" and G.nodes[e2]['type']=="path":
        down_path_check = False
    
    if G.nodes[c2]['type']=="path" and G.nodes[e2]['type']=="path" and G.nodes[f2]['type']=="path":
        down_path_check = False
    
    if G.nodes[a]['type']=="path" and G.nodes[b]['type']=="path" and G.nodes[d]['type']=="path":
        down_path_check = False
    
    if G.nodes[b]['type']=="path" and G.nodes[c]['type']=="path" and G.nodes[f]['type']=="path":
        down_path_check = False


    if G.nodes[a2]['type']=="path" and G.nodes[c2]['type']=="path":
        down_path_check = False
    
    if G.nodes[d]['type']=="path" and G.nodes[f]['type']=="path":
        down_path_check = False

    # up path checks

    if G.nodes[a]['type']=="path" and G.nodes[d]['type']=="path":
        up_path_check = False
    
    if G.nodes[a]['type']=="path" and G.nodes[g0]['type']=="path":
        up_path_check = False
    
    if G.nodes[f]['type']=="path" and G.nodes[c]['type']=="path":
        up_path_check = False
    
    if G.nodes[c]['type']=="path" and G.nodes[i0]['type']=="path":
        up_path_check = False


        # check beyond ones just above and below as well

    if G.nodes[a]['type']=="path" and G.nodes[g0]['type']=="path" and G.nodes[h0]['type']=="path":
        up_path_check = False
    
    if G.nodes[h0]['type']=="path" and G.nodes[i0]['type']=="path" and G.nodes[c]['type']=="path":
        up_path_check = False
    
    if G.nodes[f]['type']=="path" and G.nodes[i]['type']=="path" and G.nodes[h]['type']=="path":
        up_path_check = False
    
    if G.nodes[d]['type']=="path" and G.nodes[g]['type']=="path" and G.nodes[h]['type']=="path":
        up_path_check = False

    if G.nodes[g]['type']=="path" and G.nodes[i]['type']=="path":
        up_path_check = False
    
    if G.nodes[g0]['type']=="path" and G.nodes[h0]['type']=="path":
        up_path_check = False


    replaceable_types= ["grass","empty"]


    if G.nodes[h]['type'] not in replaceable_types or G.nodes[b2]['type'] not in replaceable_types:
        down_path_check = False
    
    if G.nodes[b]['type'] not in replaceable_types or G.nodes[h0]['type'] not in replaceable_types:
        up_path_check = False


    if down_path_check or up_path_check:
        return True
        
    return False

def make_vertical_path(G,source_node):

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

    #here we check that if we add the horizontal path, no nodes will become pooled

    #check if the nodes to the left or right have two path nodes next to each other
    
    # down path checks

    down_path_check = True
    up_path_check = True

    up_side_nodes = [g0,a,d,f,c,i0]

    down_side_nodes = [d,g,a2,f,i,c2]

    # for node in up_side_nodes:
    #     if count_neighbours(G,source_node,"river")>2:
    #         up_path_check=False

    # for node in down_side_nodes:
    #     if count_neighbours(G,source_node,"river")>2:
    #         down_path_check=False

    if G.nodes[d]['type']=="path" and G.nodes[g]['type']=="path":
        down_path_check = False
    #else:
      #  print("a is",G.nodes[a]['type'],"b is",G.nodes[b]['type'])
    
    if G.nodes[g]['type']=="path" and G.nodes[a2]['type']=="path":
        down_path_check = False
    
    if G.nodes[f]['type']=="path" and G.nodes[i]['type']=="path":
        down_path_check = False
    
    if G.nodes[i]['type']=="path" and G.nodes[c2]['type']=="path":
        down_path_check = False
    
    # check beyond ones just above and below as well

    if G.nodes[a2]['type']=="path" and G.nodes[d2]['type']=="path" and G.nodes[e2]['type']=="path":
        down_path_check = False
    
    if G.nodes[c2]['type']=="path" and G.nodes[e2]['type']=="path" and G.nodes[f2]['type']=="path":
        down_path_check = False
    
    if G.nodes[a]['type']=="path" and G.nodes[b]['type']=="path" and G.nodes[d]['type']=="path":
        down_path_check = False
    
    if G.nodes[b]['type']=="path" and G.nodes[c]['type']=="path" and G.nodes[f]['type']=="path":
        down_path_check = False

    # up path checks

    if G.nodes[a]['type']=="path" and G.nodes[d]['type']=="path":
        up_path_check = False
    #else:
      #  print("a is",G.nodes[a]['type'],"b is",G.nodes[b]['type'])
    
    if G.nodes[a]['type']=="path" and G.nodes[g0]['type']=="path":
        up_path_check = False
    
    if G.nodes[f]['type']=="path" and G.nodes[c]['type']=="path":
        up_path_check = False
    
    if G.nodes[c]['type']=="path" and G.nodes[i0]['type']=="path":
        up_path_check = False


        # check beyond ones just above and below as well

    if G.nodes[a]['type']=="path" and G.nodes[g0]['type']=="path" and G.nodes[h0]['type']=="path":
        up_path_check = False
    
    if G.nodes[h0]['type']=="path" and G.nodes[i0]['type']=="path" and G.nodes[c]['type']=="path":
        up_path_check = False
    
    if G.nodes[f]['type']=="path" and G.nodes[i]['type']=="path" and G.nodes[h]['type']=="path":
        up_path_check = False
    
    if G.nodes[d]['type']=="path" and G.nodes[g]['type']=="path" and G.nodes[h]['type']=="path":
        up_path_check = False


    replaceable_types= ["grass","empty"]


    if G.nodes[h]['type'] not in replaceable_types or G.nodes[b2]['type'] not in replaceable_types:
        down_path_check = False
    
    if G.nodes[b]['type'] not in replaceable_types or G.nodes[h0]['type'] not in replaceable_types:
        up_path_check = False

    choices = []

    if up_path_check:
        choices.append("u")

    if down_path_check:
        choices.append("d")

    choice = random.choice(choices)

    if choice == "u":

        alongside_nodes = [a,c]
        grass_nodes = [g0,d,i0,f]
        G.nodes[b]['type']="path"
        G.nodes[h0]['type']="path"


        print("make_vertical_path(G,",source_node,") going upwards")
        #print("Making up vertical path")

    if choice == "d":
        alongside_nodes=[g,i]
        grass_nodes=[d,a2,c2,f]
        G.nodes[h]['type']="path"
        G.nodes[b2]['type']="path"
        print("make_vertical_path(G,",source_node,") going downwards")

    for node in alongside_nodes:
        if G.nodes[node]['type'] in replaceable_types:
            G.nodes[node]['type']="irreplaceable_grass"

    for node in grass_nodes:
        if G.nodes[node]['type'] in replaceable_types:
            G.nodes[node]['type']="grass"
    
    if G.nodes[source_node]['type']!="bridge":
        G.nodes[source_node]['type']="path"
    return G


def check_castle(G, source_node):

    bfs_neighbours = list(G.neighbors(source_node))

    grass_count=0
    path_count=0

    for neighbour in bfs_neighbours:
        if G.nodes[neighbour]['type']=="grass" or G.nodes[neighbour]['type']=="empty":
            grass_count+=1
        if G.nodes[neighbour]['type']=="path":
            path_count+=1

    if grass_count!=3:
        return False
    
    if path_count==0:
        return False

    x,y = source_node

    b = ((x-1),y)
    beyond_b = ((x-2),y)
    d = (x,(y-1))
    beyond_d = (x,(y-2))
    e = source_node
    f = (x,(y+1))
    beyond_f = (x,(y+2))
    h = ((x+1),y)
    beyond_h = ((x+2),y)

    allowed_types = ["grass","empty","tree","irreplaceable_grass"]

    nodes = [b,beyond_b,d,beyond_d,e,f,beyond_f,h,beyond_h]

    for node in nodes:
        if node not in G.nodes:
            
            return False

    # I am so sorry for the amount of nesting happening here

    check_castle_bool = False

    if G.nodes[d]['type'] in allowed_types and G.nodes[f]['type'] in allowed_types: # g p g

        
        check_castle_bool = True

        if G.nodes[h]['type']=="grass":
            castle_centre = beyond_h

        else:
            castle_centre = beyond_b

        eight_neighbours = eight_connected_neighbours(G,castle_centre)

        for neighbour in eight_neighbours:

            if G.nodes[neighbour]['type'] in allowed_types:
                continue

            else:
                check_castle_bool=False
        
        around_castle = beyond_eight_neighbours(G,castle_centre)

        for neighbour in around_castle:

            if neighbour in G.nodes:
                if G.nodes[neighbour]['type']=="wall":
                    check_castle_bool=False
    
    if check_castle_bool:
        return True
    

    if G.nodes[b]['type'] in allowed_types and G.nodes[h]['type'] in allowed_types: 

        # g 
        # p 
        # g

        check_castle_bool = True

        if G.nodes[f]['type'] in allowed_types:
            castle_centre = beyond_f

        else:
            castle_centre = beyond_d

        eight_neighbours = eight_connected_neighbours(G,castle_centre)

        for neighbour in eight_neighbours:

            if G.nodes[neighbour]['type'] in allowed_types:
                continue

            else:
                check_castle_bool=False


        around_castle = beyond_eight_neighbours(G,castle_centre)

        bad_types=["wall","path","bridge"]

        for neighbour in around_castle:

            if neighbour in G.nodes:
                if G.nodes[neighbour]['type'] in bad_types:
                    check_castle_bool=False
    

    if check_castle_bool:
        return True
    
    return False

def make_castle(G,source_node):
        
    x,y = source_node

    b = ((x-1),y)
    b2 = ((x+2),y)
    d = (x,(y-1))
    t = (x,(y-2))
    f = (x,(y+1))
    m = (x,(y+2))
    h = ((x+1),y)
    h0 = ((x-2),y)

    allowed_types=["grass","empty"]

    if G.nodes[d]['type'] in allowed_types and G.nodes[f]['type'] in allowed_types: 

        # g 
        # p 
        # g

        if G.nodes[b]['type'] in allowed_types:
            door = b
            castle_centre = h0

        else:
            door = h
            castle_centre = b2
    
    elif G.nodes[b]['type'] in allowed_types  and G.nodes[h]['type'] in allowed_types : 

        # g 
        # p 
        # g

        if G.nodes[d]['type'] in allowed_types:
            door=d
            castle_centre = t

        else:
            door=f
            castle_centre = m

    eight_neighbours = eight_connected_neighbours(G,castle_centre)

    for neighbour in eight_neighbours:
        G.nodes[neighbour]['type']="wall"

    G.nodes[castle_centre]['type']="indoors"

    G.nodes[door]['type']="doorway"
    print("make_castle(G,",source_node,"source_node")

    # if G.nodes[source_node]['type']!="path":
    #     G.nodes[source_node]['type']="path"

    return G

def check_house(G, source_node):

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

   # house_check=True

    if G.nodes[d]['type'] == "grass" and G.nodes[f]['type']=="grass":
        return True
    
    elif G.nodes[d]['type'] == "replaceable_grass" and G.nodes[f]['type']=="replaceable_grass":
        return True
    
    return False

def make_house(G,source_node):
    x,y=source_node
    d = (x,(y-1))
    f = (x,(y+1))
    house_side = random.choice([0,1])

    if house_side==0:

        G.nodes[d]['type']="house"

    else:
        G.nodes[f]['type']="house"

    print("make_house(G,",source_node,")")

    return G

def check_large_castle(G, source_node):

    bfs_neighbours = list(G.neighbors(source_node))

    grass_count=0
    path_count=0

    for neighbour in bfs_neighbours:
        if G.nodes[neighbour]['type']=="grass" or G.nodes[neighbour]['type']=="empty":
            grass_count+=1
        if G.nodes[neighbour]['type']=="path":
            path_count+=1

    if grass_count!=3:
        return False
    
    if path_count==0:
        return False

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

    
    extra_nodes = [a,b,c,d,e,f,g,h,i,j,k,m,n,p,q,s,t,u,v,w,z]

    for node in extra_nodes:
        if node not in G.nodes:
            return False

    allowed_types = ["grass","empty","tree","irreplaceable_grass"]
    new_allowed_types = ["grass","empty","tree","irreplaceable_grass","path"]

    check_castle_bool = False

    if G.nodes[d]['type'] in allowed_types and G.nodes[f]['type'] in allowed_types: # g p g

        
        check_castle_bool = True

        if G.nodes[h]['type']=="grass":
            castle_centre = b2

        else:
            castle_centre = h0

        eight_neighbours = eight_connected_neighbours(G,castle_centre)

        for neighbour in eight_neighbours:

            if G.nodes[neighbour]['type'] in allowed_types:
                continue

            else:
                check_castle_bool=False
        
        around_castle = beyond_eight_neighbours(G,castle_centre)

        for neighbour in around_castle:

            if neighbour in G.nodes:
                if G.nodes[neighbour]['type'] in new_allowed_types:
                    continue
                else:
                    check_castle_bool=False

        x,y =castle_centre
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

        next_to_castle = [v,w,z,j,m,p,d0,e0,f0,d2,e2,f2]

        for neighbour in next_to_castle:

            if neighbour in G.nodes:
                if G.nodes[neighbour]['type']!="wall":
                    continue
                else:
                    check_castle_bool=False
    
    if check_castle_bool:
        return True
    
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


    if G.nodes[b]['type'] in allowed_types and G.nodes[h]['type'] in allowed_types: 

        # g 
        # p 
        # g

        check_castle_bool = True

        if G.nodes[f]['type'] in allowed_types:
            castle_centre = m

        else:
            castle_centre = t

        eight_neighbours = eight_connected_neighbours(G,castle_centre)

        for neighbour in eight_neighbours:

            if G.nodes[neighbour]['type'] in allowed_types:
                continue

            else:
                check_castle_bool=False


        around_castle = beyond_eight_neighbours(G,castle_centre)

     #  bad_types=["wall","path","bridge"]

        for neighbour in around_castle:

            if neighbour in G.nodes:
                if G.nodes[neighbour]['type'] in new_allowed_types:
                    continue

                else:
                    check_castle_bool=False

        x,y =castle_centre
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

        next_to_castle = [v,w,z,j,m,p,d0,e0,f0,d2,e2,f2]

        for neighbour in next_to_castle:

            if neighbour in G.nodes:
                if G.nodes[neighbour]['type']!="wall":
                    continue
                else:
                    check_castle_bool=False
    
    if check_castle_bool:
        return True

    return False

def make_large_castle(G,source_node):

    x,y = source_node

    b = ((x-1),y)
    d = (x,(y-1))
    t = (x,(y-2))
    e = source_node
    f = (x,(y+1))
    m = (x,(y+2))
    h = ((x+1),y)
    b = ((x-1),y)
    b2 = ((x+2),y)
    d = (x,(y-1))
    f = (x,(y+1))
    h = ((x+1),y)
    h0 = ((x-2),y)

    allowed_types = ["grass","empty","tree","irreplaceable_grass"]

    if G.nodes[d]['type'] in allowed_types and G.nodes[f]['type'] in allowed_types: # g p g

        if G.nodes[h]['type']=="grass":
            door=h
            castle_centre = b2

        else:
            door=b
            castle_centre = h0

    elif G.nodes[b]['type'] in allowed_types and G.nodes[h]['type'] in allowed_types: 

        # g 
        # p 
        # g

        check_castle_bool = True

        if G.nodes[f]['type'] in allowed_types:
            door=f
            castle_centre = m

        else:
            door=d
            castle_centre = t

    eight_neighbours = eight_connected_neighbours(G,castle_centre)

    for neighbour in eight_neighbours:

        G.nodes[neighbour]['type']="indoors"

    around_castle = beyond_eight_neighbours(G,castle_centre)

    for neighbour in around_castle:
        G.nodes[neighbour]['type']="wall"

   # G.nodes[door]['type']="doorway"
    G.nodes[source_node]['type']="doorway"
    G.nodes[castle_centre]['type']="indoors"
    print("make_large_castle(G,",source_node,"source_node")

    return G