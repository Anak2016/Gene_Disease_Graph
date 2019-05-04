from igraph import *
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import parameters as param
import itertools
from itertools import combinations
from networkx.algorithms import community, bipartite
from networkx.algorithms.community.centrality import girvan_newman
from networkx.algorithms.community.kclique import k_clique_communities
from collections import Counter


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

    # HERE>> fix so tht setup() also setup for Graph
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
                >non-first word of the same val_list = value
                >same val_list = same value of the same key
        :param file_name:
            file_name: "file_name.txt"
        :return:
            dictionary: {key: [value], ..}
        '''
        dictionary = {}
        with open(file_name, "r") as f:
            for val_list in f.readlines():
                # print(val_list)
                val_list = val_list.split(",")
                key = val_list[0]
                val = val_list[1:]
                dictionary[key] = val
        return dictionary

    def getGraph_Degree_dist(self, G, verbose = False, plot = False):
        '''

        :param G: return list of degree distribution
        :param verbose:
        :param plot:
        :return:
        '''
        degree_list = [G.degree(n) for n in G.nodes()]
        if verbose:
            print("get degree distribution of G: ")
            uniq_degree = [key for key in Counter(degree_list).keys()]
            uniq_freq   = [val for val in Counter(degree_list).values()]

            for key, val in zip(uniq_degree, uniq_freq):
                print("degree={:d} has freq ={:d}".format(key,val))
        if plot:
            plt.hist(degree_list)
            plt.show()

    def getGraph_Clustering(self, G, plot= False , verbose = False):
        ###############3
        ## add report for average clustering and triangle clustering
        ###############
        triangle           = nx.triangles(G) #triangle
        transitivity       = nx.transitivity(G) #transitibity
        clustering         = nx.clustering(G) #clustering
        average_clustering = nx.average_clustering(G) #

        # the probability that two neighbors of node v share a common neighbor different from v
        square_clustering   = nx.square_clustering(G)

        # number of triangle an edges is pariticipated in
        generalized_degree = nx.generalized_degree(G)

        algo_name = nx.square_clustering.__name__

        x = [val for key,val in square_clustering.items()]
        uniq_coeff_val = Counter(x).keys()
        uniq_coeff_freq = Counter(x).values()

        if verbose:
            print("algo = {:s}".format(algo_name))
            print("total count = {:d}".format(len(x)))
            print("zero value clutering count = {:d}".format(len(x) - len(uniq_coeff_freq)))
            print("non zero value clusters are shown below:")
            for key, val in zip(uniq_coeff_val,uniq_coeff_freq):
                print("coeff value = {:f}".format(key))
                print("value count = {:d}".format(val))
        if plot:
            print("ploting clustering coeff value")
            x = [i for i in x if x != 0 ]
            plt.hist(uniq_coeff_val)
            plt.ylabel('frequency')
            plt.xlabel('uniq_coeff_value')
            plt.title('clustering using algo = "{:s}"'.format(algo_name))
            plt.show()

    def getDistance_Measure(self, G, verbose = False, plot = False):
        from networkx.algorithms import diameter, center, eccentricity, periphery, radius

        self.set_subgraph_disconnected(G)
        disconnected_subgraph_list = self.get_subgraph_disconnected()
        for subgraph in disconnected_subgraph_list:
            print("diameter     = {:d}".format(diameter(subgraph)))
            print("center       = ", center(subgraph))
            print("eccentricity = ", eccentricity(subgraph))
            print("    eccentricity:a node v is the maximum distance from v to all other nodes in G.")
            print("periphery    = ", periphery((subgraph)))
            print("    periphery   :the set of nodes with eccentricity equal to the diameter.")
            print("radius       = ", radius((subgraph)))
            print("    radius      :the minimum eccentricity.")

    def getGraph_Centrality(self, G, verbose = False, plot = False):
        algo_name = nx.closeness_centrality.__name__
        print("printing Graph_centrality using algo = {:s}".format(algo_name))
        print(nx.closeness_centrality(G))

    def set_subgraph_disconnected(self, G):
        disconnected_graph = list(nx.connected_component_subgraphs(G))
        disconnected_graph = [(disconnected_graph[i], len(g)) for i, g in enumerate(disconnected_graph)]

        from operator import itemgetter
        disconnected_graph = sorted(disconnected_graph, key=itemgetter(1), reverse=True)
        print(disconnected_graph)

        # disconnected_graph = [subgraph1, subgraph2, ....] #where subgraph is of type networkx
        disconnected_graph = [graph for graph, length in disconnected_graph]

        self.disconnected_graph = disconnected_graph
    def get_subgraph_disconnected(self):
        return self.disconnected_graph

    def graph_link_prediction(self, G):

        #useing jarcard to predict link between 2 nodes
        x = nx.jaccard_coefficient(G)
        # nx.resource_allocation_index(G)
        # nx.adamic_adar_index(G)
        # nx.preferential_attachment(G)
        # nx.cn_soundarajan_hopcroft(G)
        # nx.ra_index_soundarajan_hopcroft(G)
        # nx.within_inter_cluster(G)
        for i, (u,v, p) in enumerate(x):
            if i == 50:
                break
            # print the first 50
            print(u, " ", v , "-->", p)

    def graph_cut(self, G):
        '''
        :param G: connected component of directed graph
        :return:
        '''
        self.set_subgraph_disconnected(G)
        disconnected_subgraph_list = self.get_subgraph_disconnected()

        for subgrph in disconnected_subgraph_list:
            cutset = nx.all_node_cuts(subgrph)
            print(cutset)

    def graph_link_analysis(self, G):
        # use pagerank
        # alpha = Damping parameter; default = 0.85
        pr = nx.pagerank(G, alpha = 0.9)
        print(pr)

    #pass in connected graph of the
    def report_Graph_properties(self, G,
                                degree_dist        = None,
                                clustering    = None,
                                centrality    = None,
                                shortest_path = None):
        verbose = True
        plot = True

        # # need to be disconnected graph
        # self.getDistance_Measure(G, verbose = verbose, plot = plot)
        # self.getGraph_Centrality(G, verbose = verbose, plot = plot)
        # self.getGraph_Clustering(G, verbose = verbose, plot = plot)
        # self.getGraph_Degree_dist(G, verbose = verbose, plot = plot)
        # self.graph_link_prediction(G)
        # self.graph_link_analysis(G)
        self.graph_cut(G) # G must be directed only
        # exit()

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

    def createEdges(self, selected_col_list = None):
        '''

        :return:
            edges: [(node_1, node2), .... ] #(node_1, node2) = edges
        '''
        df = self.getDataFrame()
        # for all instance, create edges
        index_value = self.getDataFrame_index()
        edges = []

        # selected_col_list = ['geneId', 'diseaseId']
        if selected_col_list is None:
            selected_col_list = self.getDataFrame_col()
        else:
            selected_col_list = selected_col_list

        for i in index_value:
            #create edges
            features = df.iloc[i][selected_col_list]
            features = pd.Series.tolist(features)
            comb_list = [comb for comb in combinations(features,2)]
            edges = edges + comb_list

        return set(edges)

    def createBipartite_Edges(self, selected_keys = None):
        '''

        :return:
            edge_pairs_dict: {(pair):list of permutation edges }
        '''
        df = self.getDataFrame()
        if selected_keys is None:
            selected_keys = self.getDataFrame_col()
        else:
            selected_keys = selected_keys

        keys_pair_list = [list(comb) for comb in combinations(selected_keys, 2)]

        index_list = self.getDataFrame_index()
        #create clique for each each dataFrame_index -> 1 index: many keys
        edge_pairs_dict = {tuple(pair): [] for pair in keys_pair_list}

        for pair in keys_pair_list:
            # left = df[pair[0]]
            # right = df[pair[1]]
            for i, index in enumerate(index_list):
                val = tuple(pd.Series.tolist(df[pair].iloc[index]))
                if i == 0:
                    edge_pairs_dict[tuple(pair)] = [val]
                else:
                    edge_pairs_dict[tuple(pair)].append(val)

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

    def get_node_color(self):
        return self.color_list

    # fix so that set_node_color takes color_offset as argument.
    def set_node_color(self,vertices):
        '''
        :param
            vertices: [[val_1_list],[val_2_list],..] #easy to do when convert from dict
        :return:
            color_nodes: [1,1,1,1,1....,2,2,2,2,2,...3,3,3,3,....] where different num = diffrent_color
        '''
        color_nodes = []

        for i, arr in enumerate(vertices):
            for j in range(len(arr)):
                color_nodes.append(i)

        self.color_list = color_nodes

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

        jet = cm = plt.get_cmap('jet') #color map is used to later map color back to rgba
        cNorm = colors.Normalize(vmin=0, vmax=max(color_list)) #between 0-1

        scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)

        f = plt.figure(1)
        ax = f.add_subplot(1, 1, 1)
        labels = [l for l in color_legend]

        for label in color_legend:
            ax.plot([0], [0], color=scalarMap.to_rgba(color_legend[label][0]), label=label)

        # HERE>> color is not maped to its community
        nx.draw(G, node_color=color_list, vmin=0, vmax=max(color_list), cmap=jet, ax=ax)
        plt.axis('off')
        f.set_facecolor('w')

        plt.legend()
        f.tight_layout()
        plt.show()

    def plot_subplot(self, G ,nrows=2, ncols=2):
        '''

        :param G: type = networkx
        :param nrows: number of row to be plotted
        :param ncols: number of col to be plotted
        :return:
        '''

        ######## FIX THESE SO IT SET UP VARIABLE FOR DISCONNECTED GRAPH
        #sorted subgrph in order of its nodes member
        # disconnected_graph = list(nx.connected_component_subgraphs(G))
        # disconnected_graph = [(disconnected_graph[i],len(g)) for i,g in enumerate(disconnected_graph)]
        self.set_subgraph_disconnected(G)
        disconnected_graph = self.get_subgraph_disconnected()

        ######################
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

                    ###########################
                    bipartite_vertices = left_group
                    bipartite_vertices.update(right_group)

                    bipartite_len_offset = [len(left_group), len(right_group)]

                    self.setEdges_len_offset(bipartite_len_offset)
                    # [offset1, offset2, ... ]
                    biedges_len_offset = self.getEdges_len_offset()

                    #[(1, offset1), (2,offset2), ... ]
                    color_len_offset = [ (i,val) for i, val in enumerate(biedges_len_offset)]

                    self.setColor_list(bipartite_vertices, color_len_offset) # Fix this to be more modular
                    bipartite_color = self.getColor_list()
                    ##############################3

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


    def setColor_list(self, vertices_list, color_val_offset):
        '''

        :param all_vertices: flat_vertices = [node1, node2, ....]
        :param color_val_offset:  [(val1,offset1), (val1,offset2), ...] where offset = index of a list
        :return:
        '''
        color_list = []

        for i, v in enumerate(vertices_list):
            if i >= color_val_offset[0][1]:
                del color_val_offset[0]
            color_list.append(color_val_offset[0][0])

        self.color_list = color_list

    def getColor_list(self):
        return self.color_list

    def setColor_legend(self, keys, vertices):
        '''
        :param
            keys       : [key1, key2,...]
                        type = np or list
            vettices   : [[member of key1],..]

        :return:
            color_legend: {key1: (1, len_1), key2: (2, len_1 + len_2)}
        '''

        ####These two can be used to create color_offset
        ## vertices should be [[list_of_member of community1] ,... ]
        self.set_node_color(vertices)
        color_nodes = self.get_node_color()
        node_freq = Counter(color_nodes).values()  # [freq1, ...]
        uniq_color_node = Counter(color_nodes).keys()  # [0,1,2, ....]
        #############

        color_legend = {}
        index_offset = 0

        #move below to outside of the function and feed in color_node for COMMUNITY_DETECTION.
        for i, (node_color, freq) in enumerate(zip(uniq_color_node, node_freq)):
            index_offset += freq
            color_legend[keys[node_color]] = (i, index_offset)

        self.color_legend = color_legend

    def getColor_legend(self):
        return self.color_legend

    #######################3#
    #### GRAPH OBJECT
    #########################
    def setGraph_object(self, edges_list, vertices_flat, Isdirected = False):
        if Isdirected:
            self.G = nx.DiGraph()
            self.G.add_nodes_from(vertices_flat)
            self.G.add_edges_from(edges_list)
            return self.G
        else:
            self.G = nx.Graph()
            self.G.add_nodes_from(vertices_flat)
            self.G.add_edges_from(edges_list)

        return self.G

    def getGraph_object(self):
        return self.G

    def getGraph_object_nodes(self):
        return self.G.nodes

    def geGraph_object_edge(self):
        return self.G.edges

    # HERE>> figure out how to combine plot_netwoekx and plot_subgraph
    #    Goal: only take 1 time to select scope to be run. biaprtite and community_detection
    # def plot_networkx(self,vertices_flat, edges,color_legend):
    def plot_networkx(self, vertices_flat, edges_list,color_legend, bipartite =False,  community_detection = False):
        '''

        :param vertices_flat: [val_1_list,val_2_list,..] # 1 dimension
        :param edges: [('node1', 'node2'), .... ]
        :param color_legend: {key1: (1, len_1), key2: (2, len_1 + len_2}
        :return:
            null
        '''
        color_val_offset = [(val,offset) for key, (val,offset) in color_legend.items()]

        if type(vertices_flat) is np.ndarray:
            vertices_flat = np.ndarray.tolist(vertices_flat)
        else:
            vertices_flat = vertices_flat

        self.setColor_list(vertices_flat, color_val_offset)
        color_list = self.getColor_list()


        G = self.getGraph_object()

        # self.plotGraph_with_legend(G, color_list, color_legend)
        if bipartite:
            if community_detection:
                self.plot_subplot(G)
            else:
                self.plotGraph_with_legend(G, color_list, color_legend)
        else: # use setColor_list(all_vertices, color_val_offset)
            if community_detection: #change color_list to be separated by community
                comp = girvan_newman(G)
                comp = tuple(sorted(c) for c in next(comp))

                for i, x in enumerate(comp):
                    for node in x:
                        color_list.append(i)

                node_freq = Counter(color_list).values()  # [freq1, ...]
                uniq_color_node = Counter(color_list).keys()  # [0,1,2, ....]

                color_legend = {key_id:(key_id, freq) for key_id, freq in zip(uniq_color_node, node_freq)}

                #color_legend = {community1: (1,freq of community_1)}
                self.plotGraph_with_legend(G, color_list, color_legend)
            else:
                self.setColor_list(vertices_flat, color_val_offset)
                color_list = self.getColor_list()

                self.plotGraph_with_legend(G, color_list, color_legend)

    # def plot_bipartite(self):
    def run_Graph(self, bipartite = False, selected_keys = None, community_detection = False, report= False, plot = False):
        ###########################
        ## SET UP SHARED VARIABLES
        ###########################
        df = self.getDataFrame()
        vertices_dict = self.getUniq_Vertex()  # return dict
        keys = [key for key in vertices_dict.keys()]

        if selected_keys is not None:
            vertices = [val for key, val in vertices_dict.items() for sel in selected_keys if key in sel]
        else:
            vertices = [val for key, val in vertices_dict.items()]

        if plot:
            print("requesting for ploting.....")

            if bipartite is False:

                vertices_flat = self.get_vertices_flat(vertices)
                edges_list = self.createEdges(selected_keys)  # createEdges

                self.setGraph_object(edges_list, vertices_flat)
                G = self.getGraph_object()

                if report:

                    self.report_Graph_properties(G)

                if community_detection:

                    ### use algorithm avalibale in networkx
                    comp = girvan_newman(G)
                    community_membership_list = tuple(sorted(c) for c in next(comp))
                    community_id_list = [str(i) for i, _ in enumerate(community_membership_list)]

                    # HERE>> fix vertices to have shape of [[list_of_member of community1] ,... ]
                    self.setColor_legend(community_id_list, community_membership_list)
                    color_legend = self.getColor_legend()

                    # HERE>> pass in the correct color_legend here!!!!!!!
                    self.plot_networkx(vertices_flat, edges_list, color_legend, community_detection=community_detection)
                else:

                    self.setColor_legend(keys, vertices)
                    color_legend = self.getColor_legend()

                    self.plot_networkx(vertices_flat, edges_list, color_legend, community_detection=community_detection)
            else:
                edges_dict = self.createBipartite_Edges(
                    selected_keys)  # HERE>>fix it so it returns edges of selected keys

                for pair, edges_list in edges_dict.items():

                    vertices = [val for key, val in vertices_dict.items() if key in pair]

                    # if 'geneId' in pair and 'diseaseId' in pair:
                    # if 'pmid' in pair and 'diseasepId' in pair:
                    # if 'geneId' in pair and 'diseaseId' in pair:
                    # if 'geneSymbol' in pair and 'diseaseId' in pair:
                    # if 'geneId' in pair and 'diseaseName' in pair:
                    # if 'geneSymbol' in pair and 'diseaseName' in pair:
                    # if 'diseaseClass' in pair and 'diseaseName' in pair:
                    # if 'diseaseClass' in pair and 'geneId' in pair:
                    # if True:

                    left = df[pair[0]].unique()
                    right = df[pair[1]].unique()
                    vertices_flat = np.concatenate([left, right])

                    self.setGraph_object(edges_list, vertices_flat)
                    G = self.getGraph_object()
                    if report:
                        self.report_Graph_properties(G)

                    if community_detection:
                        comp = girvan_newman(G)

                        community_membership_list = tuple(sorted(c) for c in next(comp))
                        community_id_list = [str(i) for i, _ in enumerate(community_membership_list)]

                        self.setColor_legend(community_id_list, community_membership_list)
                        color_legend = self.getColor_legend()
                        #################################################
                        self.plot_networkx(vertices_flat, edges_list, color_legend,
                                           bipartite = bipartite,
                                           community_detection=community_detection)
                    else:
                        # vertices = [[member of keys1], [member of keys2], ... ]
                        self.setColor_legend(pair, vertices)
                        color_legend = self.getColor_legend()

                        self.plot_networkx(vertices_flat, edges_list, color_legend,
                                           bipartite=bipartite,
                                           community_detection=community_detection)

if __name__ == "__main__":

    ####################
    # setup_data
    ####################
    node_num = 50
    keys_name = param.keys_name
    num_val = param.num_val

    file_name = param.file_name

    # with open(file_name, "r") as f:
    #     val_lists = f.readlines()
    #     for line in val_lists:
    #         val_list = line.split(",")
    #         if "diseaseName" in val_list[0]:
    #             print("diseaseName  " ,val_list[1:10])
    #         if "diseaseClass" in val_list[0]:
    #             print("diseaseClass  ", val_list[1:10])
    #         if "geneSymbol" in val_list[0]:
    #             print("geneSymbol ", val_list[1:10])
    #         if "uniq_pmid" in val_list[0]:
    #             print("Uniq_pmid  ", val_list[1:10])
    #         if "uniq_geneId" in val_list[0]:
    #             print("Uniq_geneId  ", val_list[1:10])
    #         if "uniq_disease" in val_list[0]:
    #             print("Uniq_disease ", val_list[1:10])
    #         # print(val_list.split(",")[0], " ", len(val_list.split(",")))
    # exit()

    copd_graph = COPD_grpah(file_name,keys_name, num_val)
    data = copd_graph.data

    ####################
    # Graph & Bipartite & community detection
    ####################

    selected_keys = param.selected_keys
    community_detection = param.community_detection
    bipartite = param.bipartite
    plot = param.plot
    report = param.report

    # copd_graph.setup() # what is thsi even for?
    # exit()
    copd_graph.run_Graph(bipartite = bipartite,
                         selected_keys = selected_keys,
                         community_detection = community_detection,
                         report = report,
                         plot   = plot)
    exit()

    ###################3
    # PLOTTING
    ###################
    # selected_keys = param.selected_keys
    # copd_graph.plotGraph(selected_keys)
    # exit()

    # node = copd_graph.getNode()
    # print(node[:4])
    # exit()

