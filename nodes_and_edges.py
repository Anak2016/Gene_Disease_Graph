from igraph import *
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import parameters as param
import itertools
from itertools import combinations
from networkx.algorithms import community, bipartite

class COPD_grpah:
    def __init__(self,file_name, keys_name, num_val):
        self.setup()

    def setDict(self):
        dict  = self.data
        temp = {}
        num_val = self.num_val
        for i,(key,val) in enumerate(dict.items()):
            key = key.replace(" ","")
            if key in self.keys_name:
                temp[key] = val[:num_val]

        self.dict = temp

    def setup(self):
        self.keys_name = [key.replace(" ", "") for key in keys_name]
        self.num_val = num_val

        self.dict = {}
        self.data = self.readFile(file_name)

        # set up Dict, dict_name
        self.dict_keyname = keys_name
        self.setDict()

        self.df = None
        self.dataFrame_col = []
        self.dataFrame_index = []

        #set up DataFrame()
        self.setDataframe()


    def getDict(self):
        return self.dict

    def getDict_keyname(self):
        '''
            not iteratble:
            must perform the following
                keys_list = [key for key in self.dict_keyname]
        :return:
        '''
        return self.dict_keyname

    def getDataFrame(self):
        return self.df

    def getDataFrame_col(self):
        return self.dataFrame_col

    def getDataFrame_index(self):
        return self.dataFrame_index

    def setDataframe(self):
        '''
            df[col].iloc[index]
                >col = str(keys_name)
                >index = int #in order that it's key got placed in DataFrame
        :return:
        '''
        # print(self.getDict().keys())
        # exit()

        dict = self.getDict()
        dict_key = self.getDict_keyname()
        key_list = [key for key in dict_key]

        df = pd.DataFrame.from_dict(dict)
        col_list  = self.keys_name
        index_list = self.num_val

        temp = []
        for col in col_list:
            if col in key_list:
                temp.append(col)
        col_list = temp

        self.df = df[col_list][:index_list]
        self.dataFrame_col = df.columns.values
        self.dataFrame_index = df.index.values


    def readFile(self,file_name):
        '''
            file must be separated by ','
                >first word = key
                >non-first word of the same line = value
                >same line = same value of the same key
        :param file_name:
            file_name: "file_name.txt"
        :return:
            dictionary: {key: [value], ..}
        '''
        dictionary = {}
        with open(file_name, "r") as f:
            for line in f.readlines():
                # print(line)
                val_list = line.split(",")
                key = val_list[0]
                val = val_list[1:]
                dictionary[key] = val
        return dictionary

    def getGraph_Degree_dist(self, G, plot = False):
        return G.degree

    def getGraph_Clustering(self, G):
        from networkx.algorithms.approximation import average_clustering
        return average_clustering(G, trials = 5)

    # def getGraph_Centrality(self, algorithms_list):
        # return

    # def getGraph_shortest_path(self):
    # def getIsolated_nodes(self)

    # def report_Graph_properties(self,
    #                     `        degree        = None,
    #                             clustering    = None,
    #                             centrality    = None,
    #                             shortest_path = None):
    #     self.getGraph_Degree_dist()
    #     self.getGraph_Clustering()
    #     self.getGraph_Centrality()
    #     self.getGraph_shortest_path()

    # def graph_link_prediction(self):
    # def grpah_link_analysis(self): #pagerank
    # def graph_cut(self, algorithms_list):
    # def graph_centrality_partition(self): #girvan_newman algorithm

    # def getGraph_disconnected(self, vertices, edges):


    def displayDict(self,dict):
        '''
            display dict on the screen with a certain format

        :param dict: {key: [val],... }
        :return:
        '''
        for key, val in dict.items():
            print("key: ", key)
            print("         val:", val)


    def getUniq_Vertex(self):
        '''

        :return:
            uniq_node_dict: {key: [uniq_value] , ...}
        '''
        dict = self.dict
        uniq_node_dict = {}
        #uniq keys have distint color
        for key, val in dict.items():
            uniq_node_dict[key] = set(val)
            uniq_node_dict[key] = list(uniq_node_dict[key])

        return uniq_node_dict

    def getVertex_len_list(self):
        '''

        :return:
            keys_len_offset: [val_1_len,val_2_len,...  ]
        '''
        df = self.getDataFrame()
        col_list = self.getDataFrame_col()

        keys_len_offset = []
        for col in col_list:
            val = df[col].unique()
            keys_len_offset.append(len(val))

        return  keys_len_offset

    def getUniq_Edge(self):
        '''
            IN PROGRESS: NOT FUNCTIONAL LIKE IT SUPPOSE TO
        :return:
            uniq_edges: dataframe;  since val in col is not the same, it is padded with Nan
            kes_len_offset: list; value = [len value_1, len value_2, ..  ]
        '''
        df = self.getDataFrame()
        col_list = self.getDataFrame_col()
        # uniq_edges = []
        df_uniq_vertex = None

        uniq_edge_dict = {}
        for col in col_list:
            # uniq_edge_dict[col] = np.ndarray.tolist(df[col].unique())
            val = df[col].unique()
            uniq_edge_dict[col] = pd.Series(val)

        df_uniq_vertex = pd.DataFrame(uniq_edge_dict)

        return df_uniq_vertex

    def createEdges(self):
        '''

        :return:
            edges: [(node_1, node2), .... ] #(node_1, node2) = edges
        '''
        df = self.getDataFrame()
        # for all instance, create edges
        col_values = self.getDataFrame_col()
        index_value = self.getDataFrame_index()
        edges = []

        for i in index_value:
            #create edges
            features = df.iloc[i]
            features = pd.Series.tolist(features)
            comb_list = [comb for comb in combinations(features,2)]
            edges = edges + comb_list

        return set(edges)

    def createBipartite_Edges(self):
        '''

        :return:
            edge_pairs_dict: {(pair):list of permutation edges }
        '''
        keys_pair_list = [list(comb) for comb in combinations(self.getDataFrame_col(), 2)]
        edges = []

        index_list = self.getDataFrame_index()

        df = self.getDataFrame()

        #create clique for each each dataFrame_index -> 1 index: many keys
        edge_pairs_dict = {tuple(pair): [] for pair in keys_pair_list}
        pair_list = [tuple(pair) for pair in keys_pair_list ]

        for pair in keys_pair_list:
            left = df[pair[0]]
            right = df[pair[1]]
            for i, index in enumerate(index_list):
                val = tuple(pd.Series.tolist(df[pair].iloc[index]))
                if i == 0:
                    edge_pairs_dict[tuple(pair)] = [val]
                else:
                    edge_pairs_dict[tuple(pair)].append(val)
                pair_list.append(pair)

        return edge_pairs_dict

    def get_vertices_flat(self, vertices):
        '''

        :param
            vertices: [[val_1_list],[val_2_list],..] #easy to do when convert from dict
        :return:
            vertices_flat: [val_1_list, val_2_list,_val_2_list] # 1 dimension
        '''

        vertices_flat = [val for arr in vertices for val in arr]
        return vertices_flat

    def get_node_color(self,vertices):
        '''
        :param
            vertices: [[val_1_list],[val_2_list],..] #easy to do when convert from dict
        :return:
            color_nodes: [1,1,1,1,1....,2,2,2,2,2,...3,3,3,3,....] where different num = diffrent_color
        '''
        # color_map = [i for i in range(3)]
        color_nodes = []
        # print(vertices)
        # exit()
        for i, arr in enumerate(vertices):
            for j in range(len(arr)):
                color_nodes.append(i)

        # print(color_nodes)
        # exit()

        return color_nodes

    def getCommunity_color(self, G):
        '''

        :param G: type = networkx
        :return:
        '''
        communities_generator = community.girvan_newman(G)
        #only get the first one; I think its order is ranked by probability
        top_level_communities = next(communities_generator)

        color_map = []
        for nodes in G.nodes:
            for i, com in enumerate(top_level_communities):
                if nodes in com:
                    color_map.append(i)
        return color_map

    def plotGraph_with_legend(self, G, color_list, color_legend):
        '''

        :param G: type = networkx
        :param color_list: [1,1,1,2,2,2,2,2,...............]
        :param color_legend: {key1:(1, len(val1}}
        :return:
        '''
        import matplotlib.cm as cmx
        import matplotlib.colors as colors

        jet = cm = plt.get_cmap('jet')
        cNorm = colors.Normalize(vmin=0, vmax=max(color_list))
        scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)

        f = plt.figure(1)
        ax = f.add_subplot(1, 1, 1)
        # for label in ColorLegend:
        for label in color_legend:
            ax.plot([0], [0], color=scalarMap.to_rgba(color_legend[label][0]), label=label)

        nx.draw(G, node_color=color_list, vmin=0, vmax=max(color_list), cmap=jet, ax=ax)
        plt.axis('off')
        f.set_facecolor('w')

        plt.legend()

        f.tight_layout()

    def plot_subplot(self, G ,nrows=2, ncols=2):
        '''

        :param G: type = networkx
        :param nrows: number of row to be plotted
        :param ncols: number of col to be plotted
        :return:
        '''

        #sorted subgrph in order of its nodes member
        disconnected_graph = list(nx.connected_component_subgraphs(G))
        disconnected_graph = [(disconnected_graph[i],len(g)) for i,g in enumerate(disconnected_graph)]
        from operator import itemgetter
        disconnected_graph = sorted(disconnected_graph,key =itemgetter(1), reverse = True)

        #disconnected_graph = [subgraph1, subgraph2, ....] #where subgraph is of type networkx
        disconnected_graph = [ graph for graph, length in disconnected_graph]

        count_disconnected = [ i+1 for i, sg in enumerate(disconnected_graph)]

        #count_disconnected = int(#nodes of the disconnected_graphs)
        count_disconnected = count_disconnected[-1]



        if count_disconnected < nrows *ncols:
            left_num = count_disconnected % nrows
            mul_num = int(count_disconnected / nrows)
            pos = str(nrows) + str(mul_num+1)
            pos_list= [int(pos+str(i+1)) for i in range(count_disconnected)]

            for i, pos in enumerate(pos_list):
                nodes_list = disconnected_graph[i].nodes
                edges_list = disconnected_graph[i].edges
                num_nodes = disconnected_graph[i].number_of_nodes()
                num_edges = disconnected_graph[i].number_of_edges()

                print("subplot[{:d}]: ".format(i))
                print("     nodes_list: ", nodes_list)
                print("     edges_list: ", edges_list )
                print("     number of nodes:", num_nodes)
                print("     number of edges:", num_edges)

                # self.setColor_list(nodes_list)
                # self.setColor_legend(nodes_list)

                plt.subplot(pos)
                plt.title('subplot_{:d}'.format(i))
                nx.draw(disconnected_graph[i])
            plt.show()

        else:
            pos = str(nrows) + str(ncols)
            pos_list = [int(pos + str(i+1)) for i in range(nrows * ncols)]
            num_graph_display = int(nrows * ncols /2) # community color long with biprtite color

            count = 0
            while(111 >= count +2):

                # for i,pos in enumerate(pos_list):
                for i in range(num_graph_display):

                    subgraph = disconnected_graph[int(count)+i]
                    ############################
                    #### VERBOSE
                    ############################
                    print("subplot[{:d}]: ".format(i))
                    print("     nodes_list: ", subgraph.nodes)
                    print("     edges_list: ", subgraph.edges)
                    print("     number of nodes:", subgraph.number_of_nodes())
                    print("     number of edges:", subgraph.number_of_edges())

                    ############################
                    #### PLOT WITH BIPARTITE_COLOR
                    ############################
                    from networkx.algorithms import bipartite

                    left_group, right_group = bipartite.sets(subgraph)

                    bipartite_vertices = left_group
                    bipartite_vertices.update(right_group)

                    bipartite_len_offset = [len(left_group), len(right_group)]

                    self.setEdges_len_offset(bipartite_len_offset)
                    # [offset1, offset2, ... ]
                    biedges_len_offset = self.getEdges_len_offset()

                    #[(1, offset1), (2,offset2), ... ]
                    color_len_offset = [ (i,val) for i, val in enumerate(biedges_len_offset)]

                    self.setColor_list(bipartite_vertices, color_len_offset) #
                    bipartite_color = self.getColor_list()

                    plt.subplot(pos_list[i])
                    plt.title('subplot_{:d}'.format(int(count + i)))

                    nx.draw(subgraph, node_color=bipartite_color)  # add community_color
                    # self.setColor_legend(()) # where can I get keys tuple from?
                    # color_legend = self.getColor_legend()
                    # self.plotGraph_with_legend(subgraph, color_list, color_legend)


                    #############################
                    # plot with community_color
                    ##############################
                    communities_color = self.getCommunity_color(subgraph)
                    # plt.subplot(pos)
                    plt.subplot(pos_list[i+2])


                    plt.title('subplot_{:d}'.format(int(count+i)))
                    # nx.draw(subgraph) # add community_color
                    nx.draw(subgraph, node_color = communities_color) # add community_color
                count += (nrows * ncols/2)
                plt.show()


    def plot_bipartite(self):

        edges_dict = self.createBipartite_Edges()
        # print(edges_dict)
        # exit()
        df = self.getDataFrame()
        for pair,edges_list in edges_dict.items():

            B = nx.Graph()
            left = df[pair[0]].unique()
            right = df[pair[1]].unique()
            all_vertices = np.concatenate([left,right])

            # color_legend = {pair[0]: (1,len(left)), pair[1]: (2,len(left)+len(right))}

            #edges_len_list = [len(key1.val), len(key2.val),...]
            edges_len_list = [len(left), len(right)]

            self.setEdges_len_offset(edges_len_list)
            edges_len_offset =  self.getEdges_len_offset()
            # for i,val in enumerate(edges_len_list):
            #     if i > 0:
            #         offset = edges_len_list[i] +  edges_len_list[i - 1]
            #         edges_len_offset.append(offset)
            #     else:
            #         edges_len_offset.append(edges_len_list[0])

            self.setColor_legend(pair, edges_len_offset)
            color_legend = self.getColor_legend()
            # print(color_legend)
            # exit()

            # x = self.get_color_legend(pair,edges_list)

            # print(x)

            # self.plot_networkx(all_vertices,edges_list, color_list,community_detectsion=True)
            self.plot_networkx(all_vertices,edges_list, color_legend,community_detection=True)
    def setEdges_len_offset(self, edges_len_list):
        '''
        :param edges_len_list: [len(edges1_list), len(edges2_list),....]
        '''
        edges_len_offset = []
        for i, val in enumerate(edges_len_list):
            if i > 0:
                offset = edges_len_list[i] + edges_len_list[i - 1]
                edges_len_offset.append(offset)
            else:
                edges_len_offset.append(edges_len_list[0])
        self.edges_len_offset = edges_len_offset

    def getEdges_len_offset(self):
        '''
        :return:
            self.edges_len_offset = [offset1, offset2, ... ] where offest_i is the first index of type_i
        '''
        return self.edges_len_offset


    def setColor_list(self, all_vertices, color_val_offset):
        '''

        :param all_vertices: flat_vertices = [node1, node2, ....]
        :param color_val_offset:  [(val1,offset1), (val1,offset2), ...] where offset = index of a list
        :return:
        '''
        color_list = []
        print(len(all_vertices))

        for i, v in enumerate(all_vertices):
            if i >= color_val_offset[0][1]:
                del color_val_offset[0]
            color_list.append(color_val_offset[0][0])
        self.color_list = color_list


    def getColor_list(self):
        return self.color_list

    def setColor_legend(self, keys_tuple, edges_len_offset):
        '''
        :param
            keys_tuple: (key1, key2, ... )
            edges_len_list = [len(key1.val), len(key2.val),...]
        :return:
            color_legend: {key1: (1, len_1), key2: (2, len_1 + len_2)}
        '''

        df = self.getDataFrame()
        #get [len(key1.val), len(key2.val),... ]

        color_legend = {key: (i,val) for i, (key, val) in enumerate(zip(keys_tuple, edges_len_offset))}

        self.color_legend = color_legend
        # return self.color_legend

    def getColor_legend(self):
        return self.color_legend

    # def plot_networkx(self,vertices_flat, edges,color_nodes, community_detection = False):
    def plot_networkx(self,vertices_flat, edges,color_legend, community_detection = False):
        '''

        :param vertices_flat: [val_1_list,val_2_list,..] # 1 dimension
        :param edges: [('node1', 'node2'), .... ]
        :param color_legend: {key1: (1, len_1), key2: (2, len_1 + len_2}
        :return:
            null
        '''
        # color_offset = [color_code1, color_code2]
        color_val_offset = [(val,offset) for key, (val,offset) in color_legend.items()]
        all_vertices = np.ndarray.tolist(vertices_flat)

        self.setColor_list(all_vertices, color_val_offset)
        color_list = self.getColor_list()

        G = nx.Graph()
        G.add_nodes_from(vertices_flat)
        G.add_edges_from(edges)

        self.plotGraph_with_legend(G,color_list, color_legend)
        # plt.show()
        # exit()

        if community_detection:
            #plot disconnected graph defult = grid 3*3

            self.plot_subplot(G)
    # def bipartite_community_detector(self):


    def plotGraph(self):

        # nodes = self.node
        vertices_dict =  self.getUniq_Vertex() # return dict
        vertices      = [val for key, val in vertices_dict.items()]
        #turn vertices into [[val_1_list], [val_2_list],... ]

        vertices_flat = self.get_vertices_flat(vertices)
        color_nodes = self.get_node_color(vertices)
        edges         = self.createEdges() # createEdges

        self.plot_networkx(vertices_flat,edges,color_nodes) # fix this



if __name__ == "__main__":

    ####################
    # setup_data
    ####################
    node_num = 50
    keys_name = param.keys_name
    num_val = param.num_val

    file_name = param.file_name
    copd_graph = COPD_grpah(file_name,keys_name, num_val)

    data = copd_graph.data

    ####################
    # Bipartite & community detection
    ####################

    # dataMatrix_col = copd_graph.getMatrix_col()
    # dataMatrix_row = copd_graph.getMatrix_row()
    # print(dataMatrix_col)
    # print(dataMatrix_row)

    # copd_graph.bipartite_community_detector()
    copd_graph.plot_bipartite()
    exit()

    ###################3
    # PLOTTING
    ###################
    # copd_graph.plotGraph()
    # exit()

    # node = copd_graph.getNode()
    # print(node[:4])
    # exit()

