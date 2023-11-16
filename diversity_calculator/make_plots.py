import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
import seaborn as sns

random = [0, 0, 0,0, 42,0]
grammar_based =  [80, 95, 84, 49, 100,98]
index = ['castle', 'houses', 'trees','paths', 'rivers', 'grass']
df = pd.DataFrame({'random': random,'grammar-based': grammar_based}, index=index)
ax = df.plot.barh()
# Adding labels to the axes
ax.set_xlabel('Percentage of levels that satisfy each category')
ax.set_ylabel('Controllability Categories')

# Display the plot
plt.show()
plt.savefig("new_controllability_metrics.png")

"""
Distance metrics
"""

# Sample data
categories = ['Grammar-based', 'Random']
values = [0.43320995699179293, 0.6419667236602132]

# Set Seaborn style
sns.set(style="whitegrid")

# Set up the figure and axis
fig, ax = plt.subplots()

# Plot the bars using Seaborn
sns.barplot(x=categories, y=values, color='blue', ax=ax)

# Add labels, title, and axis labels
ax.set_ylabel('Diversity')
ax.set_title('Method')

# Show the plot
plt.show()
plt.savefig("new_hamming_bar_graph.png")

# Cosine Similarity



# Sample data
categories = ['Grammar-based', 'Random']
values = [0.839829849330898, 0.79802947206022]

# Set Seaborn style
sns.set(style="whitegrid")

# Set up the figure and axis
fig, ax = plt.subplots()

# Plot the bars using Seaborn
sns.barplot(x=categories, y=values, color='blue', ax=ax)

# Add labels, title, and axis labels
ax.set_ylabel('Diversity')
ax.set_title('Method')

# Show the plot
plt.show()
plt.savefig("new_cosine_similarity.png")