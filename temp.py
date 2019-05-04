import networkx as nx
import matplotlib.pyplot as plt
G=nx.complete_graph(5)

nx.draw(G)
plt.show()

print(nx.triangles(G,0))

print(nx.triangles(G))

print(list(nx.triangles(G,(0,1)).values()))

