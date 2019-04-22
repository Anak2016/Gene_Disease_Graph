import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
# For color mapping
import matplotlib.colors as colors
import matplotlib.cm as cmx

G=nx.Graph()
G.add_node("kind1")
G.add_node("kind2")
G.add_node("kind3")
G.add_node("kind4")
G.add_node("kind5")
G.add_node("kind6")

# You were missing the position.
pos=nx.spring_layout(G)
val_map = {'kind1': 2,'kind2': 2,'kind3': 2,'kind4': 1,'kind5':4,'kind6': 3}
#I had this list for the name corresponding t the color but different from the node name
ColorLegend = {'Obsolete': 2,'Initialisation': 1,'Draft': 4,'Release': 3}
values = [val_map.get(node, 0) for node in G.nodes()]
# values = [val_map[node] for node in G.nodes()]

# Color mapping
# jet = cm = plt.get_cmap('jet')

jet = plt.get_cmap('jet')
cNorm  = colors.Normalize(vmin=0, vmax=max(values))

scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)

# Using a figure to use it as a parameter when calling nx.draw_networkx
f = plt.figure(1)
ax = f.add_subplot(1,1,1)
for label in ColorLegend:
    ax.plot([0],[0],color=scalarMap.to_rgba(ColorLegend[label]),label=label)

# Just fixed the color map
nx.draw_networkx(G,pos, cmap = jet, vmin=0, vmax= max(values),node_color=values,with_labels=True,ax=ax)
# nx.draw_networkx(G,pos, cmap = jet, vmin=0, node_color=values,with_labels=True,ax=ax)

# Setting it to how it was looking before.
plt.axis('off')
f.set_facecolor('w')

plt.legend()

f.tight_layout()
plt.show()