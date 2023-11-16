
import networkx as nx
import matplotlib.pyplot as plt

def probability_generator(prob_dict, feature_names):
    total_reciprocal_sum = sum(1.0 / rank for rank in prob_dict.values())
    probabilities = [(1.0 / prob_dict[feature])/ total_reciprocal_sum if feature in prob_dict else (1.0 /5)/ total_reciprocal_sum for feature in feature_names]
    normalized_probabilities = [prob / sum(probabilities) for prob in probabilities]
    return normalized_probabilities

def eight_connected_neighbours(G, node):
    directions = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
    eight_direction_neighbours = []
    for dx, dy in directions:
        neighbour_x, neighbour_y = node[0] + dx, node[1] + dy
        if (neighbour_x, neighbour_y) in G.nodes:
            eight_direction_neighbours.append((neighbour_x, neighbour_y))

    return eight_direction_neighbours

def count_neighbours(G,node,cell_type):

    node_type = nx.get_node_attributes(G, 'type')

    neighbours = eight_connected_neighbours(G,node)

    count = 0

    for node in neighbours:
        if node_type[node]==cell_type:
            count+=1

    return count

def beyond_eight_neighbours(G,node):
    # gets the nodes around the eight_connected neighbours
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

    beyond_list =[((x-1),(y-2)),(x,(y-2)),((x+1),(y-2)),
                  ((x-1),(y+2)),(x,(y+2)),((x+1),(y+2)),
                  ((x-2),(y-1)),((x-2),y),((x-2),(y+1)),
                  ((x+2),(y-1)), ((x+2),y),((x+2),(y+1)),
                  ((x-2),(y-2)),((x+2),(y+2)),((x-2),(y+2)),((x+2),(y-2))]

    return beyond_list



