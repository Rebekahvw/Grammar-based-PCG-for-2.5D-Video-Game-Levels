# import rogue_generator 
import rogue_generator 
import test_generator 
import random_generator
import matplotlib.pyplot as plt
from controllability import control_metric
import numpy as np

def generate_levels(version, dimensions, level_num, folder_name):

    control_array=[]

    for i in range(level_num):
    
        graph = version.create_level(dimensions)
        graph_results = control_metric(graph)
        control_array.append(graph_results)
        
        level = version.represent_graph(graph)
        fig = plt.figure(frameon=False)

        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)

        ax.imshow(level, aspect='equal')
        plt.savefig(folder_name + "/level" + str(i) + ".png", bbox_inches='tight', pad_inches=0)

        print("Done " + str(i))

    return control_array

dimensions = [31,31]

level_number = 10

control_arrays = generate_levels(rogue_generator,dimensions,level_number,"../version_rogue")

control_point_list = ["Castle present","Between 3 and 25 houses present","Between 3 and 25","All desired path features present","All river features present","At least one 9 by 9 patch of grass present"]

summed_control_array = np.zeros(len(control_point_list))

for m in range(len(control_arrays)):
    for n in range(len(summed_control_array)):
        summed_control_array[n]+=control_arrays[m][n]

for n in range(len(summed_control_array)):
    summed_control_array[n]=(summed_control_array[n]/level_number)*100


# Open the file for writing
with open('controllability.txt', 'w') as f:
    
    for i in range(len(control_arrays)):
        item = control_arrays[i]
        string = "Graph: "+str(i)+'\n'
        f.write(string)
        for j in range(len(control_point_list)):
            line = control_point_list[j]+": "+str(item[j])
            f.write(line+'\n')
        f.write('\n')
    
    f.write("Percentage of levels per control category:\n")
    for j in range(len(control_point_list)):
        line = control_point_list[j]+": "+str(summed_control_array[j])
        f.write(line+'\n')

    


