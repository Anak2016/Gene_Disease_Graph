###################
# community detection with girvan_newman
###################
import networkx as nx
from networkx.algorithms import community, bipartite
import matplotlib.pyplot as plt

# G = nx.barbell_graph(5, 3)
# G = nx.path_graph(8)

G = nx.Graph()
# Add nodes with the node attribute "bipartite"
G.add_nodes_from([1, 2, 3, 4, 11,22,33,44], bipartite=0)
G.add_nodes_from(['a', 'b', 'c', 'x','y','z'], bipartite=1)
# Add edges only between nodes of opposite node sets
G.add_edges_from([(1, 'a'), (1, 'b'), (2,'a'), (2, 'c'), (3, 'c'), (4, 'a')])
G.add_edges_from([(11, 'x'), (11, 'y'), (22,'x'), (22, 'z'), (33, 'z'), (44, 'x')])

# print(nx.is_connected(G))
# exit()

l, r = bipartite.sets(G)
# l = {n for n,d in G.nodes(data=True) if d['bipartite']==1}
# print(G.nodes(data=True))
'''
[(1, {'bipartite': 0}), ...]
'''
pos = dict()
pos.update((n,(1,i)) for i, n in enumerate(l))
pos.update((n,(2,i)) for i, n in enumerate(r))

# print(round(bipartite.density(G,l),2))
# print(l)
# print(r)
# exit()

communities_generator = community.girvan_newman(G) # community detection algorithm
# x = [val for val in communities_generator]
'''
[({}, ..., {} ) ,... , ]
    >{} is community;
    >() first uniq_community split;
    >[] = contain all uin_q community split
'''
top_level_communities = next(communities_generator)
next_level_communities = next(communities_generator)
communities = [com for com in communities_generator]

color_map = []
for nodes in G.nodes:
    for i, com in enumerate(next_level_communities):
        if nodes in com:
            color_map.append(i)


nx.draw(G, node_color  = color_map,  with_labels=True, pos= pos)
plt.draw()
plt.show()
##################
# PLOT DEGREE DISTRIBUTE
##################
# import collections
# import matplotlib.pyplot as plt
# import networkx as nx
#
# # G = nx.gnp_random_graph(100, 0.02)
# G= nx.erdos_renyi_graph(100, 0.1)
#
# degree_sequence = sorted([d for n, d in G.degree()], reverse=True)  # degree sequence
# # print "Degree sequence", degree_sequence
# degreeCount = collections.Counter(degree_sequence)
# # print(degreeCount)
# # print(*degreeCount.items())
# # print(*degreeCount)
# # exit()
# deg, cnt = zip(*degreeCount.items())
#
# fig, ax = plt.subplots()
# plt.bar(deg, cnt, width=0.80, color='b')
#
# plt.title("Degree Histogram")
# plt.ylabel("Count")
# plt.xlabel("Degree")
# ax.set_xticks([d + 0.4 for d in deg])
# ax.set_xticklabels(deg)
#
# # draw graph in inset
# plt.axes([0.4, 0.4, 0.5, 0.5])
# Gcc = sorted(nx.connected_component_subgraphs(G), key=len, reverse=True)[0]
# pos = nx.spring_layout(G)
# plt.axis('off')
# nx.draw_networkx_nodes(G, pos, node_size=20)
# nx.draw_networkx_edges(G, pos, alpha=0.4)
#
# plt.show()