import rogue_generator 
import test_generator 
import random_generator
import matplotlib.pyplot as plt
from helper_functions import count_neighbours

def control_metric(G):

    return [castle_test(G),house_test(G),tree_test(G),path_features_test(G),river_features_test(G),grass_test(G)]

def castle_test(G):

    for node in G.nodes:
        if G.nodes[node]['type']=="wall":
            return 1
    return 0
        
def house_test(G):
    house_count =0
    
    for node in G.nodes:
        if G.nodes[node]['type']=="house":
            house_count+=1
    
    if house_count>=3 and house_count<25:
        return 1
        
    return 0

def tree_test(G):
    tree_count =0
    
    for node in G.nodes:
        if G.nodes[node]['type']=="tree":
            tree_count+=1
    
    if tree_count>=3 and tree_count<25:
        return 1
        
    return 0

def path_features_test(G):

    t_junction_unfound= True
    L_bend_unfound = True
    bridge_unfound = True
    horizontal_path_unfound = True
    vertical_path_unfound = True

    for node in G.nodes:

        x,y = node

        a = ((x-1),(y-1))
        b = ((x-1),y)
        c = ((x-1),(y+1))
        d = (x,(y-1))
        e = node
        f = (x,(y+1))
        g = ((x+1),(y-1))
        h = ((x+1),y)
        i = ((x+1),(y+1))

        t_junction = True
        L_bend = True
        bridge = True
        horizontal_path = True
        vertical_path = True

        if t_junction_unfound:

            t_junc_nodes = [a,b,c,e,h]

            for t_j_node in t_junc_nodes:
                if t_j_node in G.nodes and G.nodes[t_j_node]['type']=="path":
                    continue
                else:
                    t_junction = False
                    break

            if t_junction:
                t_junction_unfound=False

        if L_bend_unfound:

            L_bend_list = [e,a,b,i,h]

            for l_node in L_bend_list:
                if l_node in G.nodes and G.nodes[l_node]['type']=="path":
                    continue
                else:
                    L_bend = False
                    break

            if L_bend:
                L_bend_unfound=False

            if L_bend==False:
                L_bend_list = [e,b,c,g,h]

                for l_node in L_bend_list:
                    if l_node in G.nodes and G.nodes[l_node]['type']=="path":
                        continue
                    else:
                        L_bend = False
                    
                        break

                if L_bend:
                    L_bend_unfound=False

            if L_bend==False:
                L_bend_list = [e,c,f,g,h]

                for l_node in L_bend_list:
                    if l_node in G.nodes and G.nodes[l_node]['type']=="path":
                        continue
                    else:
                        L_bend = False
                        break

                if L_bend:
                    L_bend_unfound=False

        if bridge_unfound:

            bridge_list = [d,f]

            for bridge_node in bridge_list:
                if bridge_node in G.nodes and G.nodes[bridge_node]['type']=="path":
                    continue
                else:
                    bridge = False
                    break

            if bridge:
                if G.nodes[e]['type']!="bridge":
                    bridge=False

                else:
                    bridge_unfound=False

        if horizontal_path_unfound:

            horizontal_path_list = [d,e,f]

            for hori_path_node in horizontal_path_list:
                if hori_path_node in G.nodes and G.nodes[hori_path_node]['type']=="path":
                    continue
                else:
                    horizontal_path = False
                    break

            if horizontal_path:
                horizontal_path_unfound=False

        if vertical_path_unfound:

            vertical_path_list = [b,e,h]

            for vert_path_node in vertical_path_list:
                if vert_path_node in G.nodes and G.nodes[vert_path_node]['type']=="path":
                    continue
                else:
                    vertical_path = False
                    break

            if vertical_path:
                vertical_path_unfound=False

    if t_junction_unfound or L_bend_unfound or bridge_unfound or horizontal_path_unfound or vertical_path_unfound:
        return 0
    
    else:
        return 1

def river_features_test(G):

    horizontal_unfound = True
    vertical_unfound = True

    for node in G.nodes:

        x,y = node

        b = ((x-1),y)
        d = (x,(y-1))
        e = node
        f = (x,(y+1))
        h = ((x+1),y)

        horizontal_river = True
        vertical_river= True

        if horizontal_unfound==True:

            horizontal_river_list = [d,e,f]

            for hori_river_node in horizontal_river_list:
                if hori_river_node in G.nodes and G.nodes[hori_river_node]['type']=="river":
                    continue
                else:
                    horizontal_river = False
                    break

            if horizontal_river:
                horizontal_unfound=False

        if vertical_unfound==True:

            vertical_path_list = [b,e,h]

            for vert_river_node in vertical_path_list:
                if vert_river_node in G.nodes and G.nodes[vert_river_node]['type']=="river":
                    continue
                else:
                    vertical_river = False
                    break

            if vertical_river:
                vertical_unfound=False


    if vertical_unfound or horizontal_unfound:
        return 0
    else:
        return 1
    

def grass_test(G):
    #checking for a 9 by 9 patch of grass, nothing major

    for node in G.nodes:
        count = count_neighbours(G,node,"grass")
        if G.nodes[node]['type']=="grass" and count == 8:
            return 1
        
    return 0