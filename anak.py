#
# ########
# # geneid.txt
# #########
# keys = {}
#
# col_list = ['geneId','geneSymbol','diseaseId','diseaseName','diseaseClass','pmid','source','class']
# dictionary = {i: [] for i,key in enumerate(col_list)}
# file_name = 'dataset/generated_dataset/TESTING'
# with open(file_name) as f:
#     for i,line in enumerate(f):
#         if i ==0:
#             val_list = line.split(",")
#             val_list = [val.strip().lower() for val in val_list]
#         else:
#             val_list = line.split(',')
#             for i,val in enumerate(val_list):
#                 dictionary[i].append(val)
#
# num_uniq_dict = {key: len(set(val)) for key,val in dictionary.items()}
# uniq_dict = {key: len(val) for key,val in dictionary.items()}
#
# file_name = 'dataset/generated_dataset/geneid.txt'
# with open(file_name, 'w') as f:
#     for i in set(dictionary[0]):
#         f.write(str(i) + ' ')

# print(num_uniq_dict)
# print(uniq_dict)
# print(dictionary.keys())
#
# # ##############
# # ## list of UniProtKB
# # ##############
# # file_name='dataset/mapa_geneid_4_uniprot_crossref/mapa_geneid_4_uniprot_crossref.tsv'
# # # file_name = 'dataset/generated_dataset/TESTING'
# # col_list = ['UniProtKB',"GENEID"]
# # dictionary = {i: [] for i,key in enumerate(col_list)}
# # with open(file_name) as f:
# #     for i,line in enumerate(f):
# #         if i ==0:
# #             val_list = line.split("\t")
# #             val_list = [val.strip().lower() for val in val_list]
# #         else:
# #             val_list = line.split('\t')
# #             for i,val in enumerate(val_list):
# #                 dictionary[i].append(val)
# # # print(dictionary)
# #
# # num_uniq_dict = {key: len(set(val)) for key,val in dictionary.items()}
# # uniq_dict = {key: len(val) for key,val in dictionary.items()}
# #
# # file_name = 'dataset/mapa_geneid_4_uniprot_crossref/uniprotkb.txt'
# #
# # print(len(set(dictionary[0])))
# # with open(file_name, 'w') as f:
# #     for i in set(dictionary[0]):
# #         f.write(str(i) + ' ')
# #
# # # print(num_uniq_dict)
# # # print(uniq_dict)
# # # print(dictionary.keys())
#
# ##################3
# ### extract GOID
# ##################
# # file_name = 'dataset/generated_dataset/TESTING'
# file_name = 'dataset/mapa_geneid_4_uniprot_crossref/uniprot-yourlist_M201906178471C63D39733769F8E060B506551E121E1FB6H.tab'
# col_list = ['yourlist:M201906178471C63D39733769F8E060B506551E121E1FB6H', 'Entry','Entry name','Status','Gene ontology (biological process)','Gene ontology (cellular component)','Gene ontology (GO)','Gene ontology (molecular function)','Gene ontology IDs','Length','Gene names']
# dictionary = {key.lower(): [] for i,key in enumerate(col_list)}
# col_name = None
# with open(file_name) as f:
#     for i,line in enumerate(f):
#         if i ==0:
#             col_name = line.split("\t")
#             col_name = [val.strip().lower() for val in col_name]
#         else:
#             val_list = line.split('\t')
#             for i,val in enumerate(val_list):
#                 if col_name[i] == list(dictionary.keys())[i]:
#                     # print('right col name')
#                     dictionary[col_name[i]].append(val.strip())
#                 else:
#                     print('wrong col name')
#
# num_uniq_dict = {key: len(set(val)) for key,val in dictionary.items()}
# uniq_dict = {key: len(val) for key,val in dictionary.items()}
#
# file_name = 'dataset/mapa_geneid_4_uniprot_crossref/go.txt'
#
# import pandas as pd
# df = pd.DataFrame.from_dict(dictionary)
# # print(df.head())
# # print(df.shape[1])
# with open(file_name, 'w') as f:
#     f.write(df.to_csv(index = False))
# # print(uniq_dict)
# # print(dictionary.keys())

import networkx as nx
import matplotlib.pyplot as plt
G = nx.bipartite.gnmk_random_graph(3, 5, 10, seed=123)
# G = nx.Graph()
# G.add_nodes_from([0,1,2])
# G.add_edges_from([(0,1),(0,2)])
top = nx.bipartite.sets(G)[0]
bottom = nx.bipartite.sets(G)[1]
# def vertices_flat(
# def createEdges(selected_keys)
# def setGraph_object(edge_list, vertices_flat)
# def setColor_legend
color = []
for i in range(len(top) + len(bottom)):
    if i<len(top):
        color.append(1)
    else:
        color.append(2)

# pos = nx.bipartite_layout(G, top)
# pos = nx.kamada_kawai_layout(G)
# G = nx.path_graph(4)
pos = nx.planar_layout(G)

nx.draw_networkx(G, pos=pos,node_color=color)
plt.show()

exit()

col_list = ['geneId','geneSymbol','diseaseId','diseaseName','diseaseClass','pmid','source','class']
dictionary = {key: [] for i,key in enumerate(col_list)}
file_name = 'dataset/generated_dataset/copd_label.txt'
with open(file_name) as f:
    for i,line in enumerate(f):
        if i ==0:
            val_list = line.split(",")
            val_list = [val.strip().lower() for val in val_list]
        else:
            val_list = line.split(',')
            for i,val in enumerate(val_list):
                dictionary[list(dictionary.keys())[i]].append(val)

uniq_val = {key:set(val) for  key,val in dictionary.items()}
uniq_val_len = {key:len(set(val)) for  key,val in dictionary.items()}
print(uniq_val_len)
exit()
# uniq_edge = set of(geneId, diseaseId)

import pandas as pd
df = pd.DataFrame(dictionary)
edges = df.loc[:][["geneId", "diseaseId"]]
file_name = 'dataset/generated_dataset/copd_edges.txt'
edges.to_csv(file_name, index=False)
edges = list(edges.itertuples(index=False, name=None))
print(len(set(edges))) #3687

x = {"geneId":list(uniq_val["geneId"]) }
y = {"diseaseId": list(uniq_val['diseaseId'])}
df_uniq = pd.concat([pd.DataFrame(x), pd.DataFrame(y)], axis =1)

file_name = 'dataset/generated_dataset/copd_uniq_node.txt'
df_uniq.to_csv(file_name, index=False)

# file_name = 'dataset/generated_dataset/gene_disease_uniq.txt'
# with open(file_name, 'r') as f:
#     data = f.readlines()
#     uniq_dict ={}
#     for i,line in enumerate(data):
#         key = line.split(',')[0]
#         val = [i.strip() for i in line.split(',')[1:]]
#         uniq_dict[key] = val
#
# import pandas as pd
# with open('dataset/generated_dataset/gene_disease_uniq_vertical.txt', 'w') as f:
#     keys = [key for key in uniq_dict.keys()]
#     f.write(','.join(list(keys)))
#     f.write('\n')
#     length = [len(val) for val in uniq_dict.values()]
#     max_len = max(length)
#     for i in range(max_len):
#         val_list = []
#         for key,val in uniq_dict.items():
#             try:
#                 val_list.append(val[i])
#                 if i ==16631:
#                     if key == 'geneId':
#                         print("here")
#             except:
#                 val_list.append('NA')
#         f.write(','.join(val_list))
#         f.write('\n')