####################
### todo for this file
# Goal: make this file readable. make it easier to read.
#> refactor method and function
#     >>use dataframe or numpy whenever possible.
# >write comment on important function/method/step
###################

import operator
import pandas as pd
import csv

def create_DO_mapping_from_source(): # there might be something wrong here.
    '''
    create mapping_dict from DO source extracted from disease_mappings.tsv (downloaed from the site)

    header = diseaseId,name,vocabulary,code,vocabularyName
    :return: dict: {header1: [list of val],.... }
    '''
    ###################33
    ## create mapping_dict
    ###################33
    mapping_file = "dataset/disease_mappings_umls/disease_mappings.tsv"
    with open(mapping_file, "r") as f:
        data_file = f.readlines()

    headers = data_file[0]
    header_list = headers.split("|")

    data = data_file[:-1]
    source_mapping_dict = {header: [] for header in header_list}
    # select row whose vocabulary belongs to Disease Ontology (DO)
    for i, line in enumerate(data[1:]):
        val_list = line.split("|")
        # only use map to DO vocabulary
        if val_list[2] == 'DO':
            for j, (header, val) in enumerate(zip(header_list, val_list)):
                source_mapping_dict[header].append(val)

    # #what is the code below doing?
    # dict = [[diseaseId, vocab, code, vocabName]for diseaseId, vocab, code, vocabName in zip(mapping_dict['diseaseId'],mapping_dict['vocabulary'], mapping_dict['code'], mapping_dict['vocabularyName\n'])]
    #
    # diseaseId_mapping = {}
    # # diseaseId_vocabName = {}
    # for key,val_list in DiseaseId_dict.items():
    #     for val in val_list:
    #         for mapped_list in dict:
    #             if val == mapped_list[0]:
    #                 diseaseId_mapping[val] = mapped_list

    return source_mapping_dict

def Map_uniq_CUIs_to_DO(source_mapping_dict):
    '''
    return dict of the following format
        {DO: [list of uniq_cuis]}

    :param source_mapping_dict: {}
    :return: dict: {DO: [list of cuis]}
    '''
    print("mapping uniq cui to DO from gene_disease_uniq and disease_mapping....")
    source_mapping_df = pd.DataFrame.from_dict(source_mapping_dict)
    # create_cuis_list_from_file is reused in the main. (I may be able to refactor this)
    gene_disease_uniq_file_path = "dataset/generated_dataset/gene_disease_uniq.txt"

    uniq_CUIs = create_cuis_list_from_file(gene_disease_uniq_file_path) #len = 9434

    # print(len(uniq_CUIs)) # 9434
    # exit()

    ##############
    ## checking length of various variables
    #############
    #convert to dataframe
    print("shape of disease_mapping.tsv dataframe=",source_mapping_df.shape) # there are 15675 row in disease_mapping.tsv
    uniq_CUIs_DO_df = source_mapping_df.loc[source_mapping_df['diseaseId'].isin(uniq_CUIs)] #10834 out of 15675 that have have mapping to disease_gene_uniq.txt
    uniq_cui_list = uniq_CUIs_DO_df['diseaseId'].unique() #disease_mapping has 6102 uniq cui outof 10834 total rows
    uniq_do_list = uniq_CUIs_DO_df['code'].unique() #disease_mapping has 4124 uniq do outof 10834 total rows

    print("num of row whose cui can map to gene_disease_uniq.txt = ",uniq_CUIs_DO_df.shape)
    import numpy as np
    print("num of uniq cui in disease_mapping.tsv dataframe=",len(uniq_cui_list)) #6102
    print("num of uniq DO in disease-mpping.tsv dataframe =",len(uniq_do_list)) #4124

    ###########
    ## get list of cui that have more than 1 mapping to DO
    ###########
    from itertools import groupby
    # y = [ len(list(group)) for key, group in groupby(pd.Series.tolist(uniq_CUIs_DO_df['diseaseId'])) ]
    cui_Do_1TOmany = [ key for key, group in groupby(pd.Series.tolist(uniq_CUIs_DO_df['diseaseId'])) if len(list(group)) >1]
    # print("list of cui that have more than 1 DO mapping", cui_Do_1TOmany)
    #######################################
    # ## create {DO: [list of cuis]}
    #######################################
    ##append freqency
    # use df slicing
    uniq_CUIs_DO_df = uniq_CUIs_DO_df.loc[~uniq_CUIs_DO_df['diseaseId'].isin(cui_Do_1TOmany)]
    print("len of cui that have 1 mapping to DO in disease_tsv.tsv and have mapping "
          "to gene_disease_uniq.txt=",uniq_CUIs_DO_df.shape[0]) #len = 9858

    uniq_CUIs_DO_df = uniq_CUIs_DO_df[['diseaseId','code']]
    uniq_CUIs_DO_dict = uniq_CUIs_DO_df.to_dict('list')
    return uniq_CUIs_DO_dict

def Write2file(save_path,dict, vertical=False):
    '''

    :param save_path:
    :param diseaseId_mapping:
    :param vertical:

        if vertical = True => write the following format to file
            key1,key2,key3
            val1,val1,val1 #val1 of each key
            val2,val2,val2 #val2 of each key
            val3,val3,val3 #val3 of each key

        if vertival = False => write the follwoing format to file
            key1,val1,val2,val3,...
            key2,val1,val2,val3,...
            key3,val1,val2,val3,...
    '''
    keys_list = [key.strip() for key in dict.keys()]
    if vertical:

        with open(save_path, "w") as f:
            header = ','.join(keys_list)
            f.write(header)
            f.write('\n')

            # dict = {key : [val_list]}

            #checking that all cols have the same length.
            len_val_list = [len(val) for val in dict.values()]
            for i,len_val in enumerate(len_val_list[:-1]):
                assert len_val == len_val_list[i+1], "not all cols have the same length"

            for i in range(len_val_list[0]):
                row = []
                for key in dict.keys():
                    # KeyError: 1
                    val = dict[key][i]
                    row.append(val)
                sent = ','.join(row)
                f.write(sent)
                f.write('\n')

    else:
        ##### code below is not yet fixed#####
        with open(save_path, "w") as f:
            # f.write("deseseId,vocab,code,vocabName")
            # f.write('\n')
            # diseaseId_mapping = {CUIS : [diseaseId, vocab, code, vocabName]}
            for key, val in dict.items():
                sent = ",".join(val)
                f.write(sent)

def read_json_from_url(file_path, save_path,col_names, verify_doid=False):
    '''

    :param file_path: file whose doid will be mapped to its parents
    :param save_path:
    :param col_names: list of col_names
    :param uniq_do_mapping_file_path: file containing mapping from doid to uniq_cui
    :param verify_doid: check that doid that will be mapped to parent_doid or parent_parent_doid is a valid doid
                    >valid doid is doid that has mapping to uniq_cuis
    :return:
    '''
    #############
    ## read
    # >parent_diseaseId_DO_mapping.txt  to mapt parent_doid to parent_parent_doid
    # >gene_disease_uniq_DO_mapping.txt to map doid to its parent_doid
    #############
    with open(file_path, 'r') as f:
        data = f.readlines()

        parent2doid_dict = {}
        DOID_code_list = []
        doid_ind = None
        valid_doid_ind = None
        for i, line in enumerate(data):
            val_list = line.split(",")
            # key: deseseId, vocab, code, vocabName
            if i ==0:
                for j, val in enumerate(val_list):
                    col = val.lower().strip()
                    # if val in ["parentId".lower(),'diseaseId'.lower()]:
                    if col in ["code", "parentid"]: #doid; col to be mapped to its parent
                        doid_ind = j
                    if col in ["diseaseid"]: #doid that has mapping to uniq_cuis
                        valid_doid_ind = j
            if i != 0:

                DOID_code_list.append(val_list[doid_ind])
                if verify_doid is True:
                    # create parent2doid_dict
                    if val_list[doid_ind] in parent2doid_dict.keys():
                        parent2doid_dict[val_list[doid_ind]].append(val_list[valid_doid_ind])
                    else:
                        parent2doid_dict[val_list[doid_ind]] = [val_list[valid_doid_ind]]

    x = [val for val_list in parent2doid_dict.values() for val in val_list]
    y = [val for val_list in parent2doid_dict.values() for val in set(val_list)]
    assert len(set(x)) == len(y), "some val in parent2doid_doid.values() are not uniq"


    ##map doid in doid_code_list to valid doids that have mapping to cui
    DOID_code_list = list(set(DOID_code_list)) #get uniq doid code

    #############
    import requests
    import json


    with open(save_path, "w") as f :
        f.write(col_names)
        print("writing to {:s}".format(save_path))
        # f.write("diseaseID,parentID, parentName")
        f.write("\n")
        fail_code = []
        for code in DOID_code_list:
            code = code.strip()
            # map uniq DIOD to its parents
            try:
                link = "http://www.disease-ontology.org/api/metadata/DOID:%s" % code
                response = json.loads(requests.get(link).text)
                # print(response['parents']) # ["relationship", "diseaseName", "DOID of diseaseName"]
                #
                # 'DOID:0050686'

                DOID_code = response['parents'][0][2].split(":")
                DOID_code = DOID_code[1]
                if verify_doid is True:
                    # DOID_code_list = list of valid doids #def of valid doid is define in function description
                    parent_doid = code
                    valid_doid_list = parent2doid_dict[parent_doid]

                    # # for some reason when testing outside of the loop
                    # # ['150','630','0014667'] appears to be in val of parent2doid_dict
                    # # However, it fails to show that ['150','630','0014667'] is in parent2doid_dict inside the loop
                    # for i in ['150','630','0014667']:
                    #     if i in valid_doid_list:
                    #         #fail: nothing is printed during the iterative process
                    #         print('{:s} is a val in parent2doid_dict'.format(i))

                    for valid_doid in valid_doid_list:
                        parent_DOID_Name = DOID_code +','+ response['parents'][0][1] # parent_doid, parent_name
                        line = valid_doid + "," + parent_DOID_Name  # valid_doid, parent_doid, parent_name
                        f.write(line)
                        f.write("\n")
                else:
                    parent_DOID_Name = DOID_code + ',' + response['parents'][0][1]  # parent_doid, parent_name
                    line = code + "," + parent_DOID_Name  # doid, parent_doid, parent_name
                    f.write(line)
                    f.write("\n")
                #map uniq DIOD to its parents
            except:
                print("link=", link)
                print("code=", code)
                fail_code.append(code)

            # print("fail_code",fail_code.append(code))

def get_uniq_parent(file_path, name):
    '''

    :param file_path: file contain parent and diseaseID mapping
    :name: name of the varible
    :return:
    '''
    #########
    ## check how many uniq parents are there
    #########

    with open(file_path, 'r') as f:
        data = f.readlines()
    parents_list = []
    for i, line in enumerate(data):
        if i != 0:
            val_split = line.split(",")
            parents_list.append(val_split[1])

    print("{:s};all DOID  len = {:d}".format(name,len(parents_list)))  # 6078
    print("{:s};uniq parent DOID code len = {:d}".format(name,len(set(parents_list))))  # 1007
    print()
    return set(parents_list)

def get_keys(key_val_list, max_len=None ):
    '''
    print dictionary containing tuple {parent_DOID: children's count}
    :param key_val_list: [('parent_doid', 'number of children')]
    :return: list of parent_dodid: ['parent_doid',...]
    '''
    print()
    print("number of chosen uniq class mapping = ", len(key_val_list))
    key_list = []

    for i,key_val in enumerate(key_val_list):
        if max_len is not None:
            if i <= max_len:
                print(key_val[0],end=",")
                key_list.append(key_val[0])
        else:
            print(key_val[0], end=",")
            key_list.append(key_val[0])
    print()
    return key_list

def create_parent_children_DO_dict(parent_mapping_file_path, parent_parent_mapping_file_path):
    '''

    :return: {label_DOID: [list of children_DOID]}
    '''

    # parent_diseaseId_DO_mapping = 'dataset/disease_mappings_umls/parent_diseaseId_uniq_DO_mapping.txt'
    # get children DOID
    with open(parent_mapping_file_path, 'r') as f:
        parent_diseaseId_DO_mapping = f.readlines() # diseaseId is not uniq in this case

    with open(parent_parent_mapping_file_path, 'r') as f:
        parent_parent_diseaseId_DO_mapping = f.readlines() # diseaseId is not uniq in this case

    parent_ind = None
    children_ind = None

    parent_member_count = {parent: 0 for parent in parent_mapping}
    parent_parent_member_count = {parent: 0 for parent in parent_parent_mapping}
    parent_intersect_member_count = {parent: 0 for parent in parent_intersect}

    #only do the first 16 parents with most members because I only need 16 or less

    ############
    ## count number of member of each parent
    ############
    for i, line in enumerate(parent_diseaseId_DO_mapping):
        val_split = line.split(",")
        if i == 0:
            for j, val in enumerate(val_split):
                if val == 'parentID':
                    parent_ind = j
                if val == 'diseaseID' or val == '1diseaseID':
                    children_ind = j
        if i != 0:
            # note:
            #   diseaseId in the file such as gene_disese_1000 is not uniq because diseaseId being
            #   presented here have different atturiute such as geneId
            #   (geneId: dieaseId => many:1)

            # note:
            #   any of the dict_count below can be used because the first 16 members are the same
            #   and we only less than 14 labels.
            if val_split[parent_ind] in parent_member_count.keys():
                parent_member_count[val_split[parent_ind]] += 1

            if val_split[parent_ind] in parent_parent_member_count.keys():
                parent_parent_member_count[val_split[parent_ind]] += 1

            if val_split[parent_ind] in parent_intersect_member_count.keys():
                parent_intersect_member_count[val_split[parent_ind]] += 1

    sorted_parent_count = sorted(parent_member_count.items(), key=operator.itemgetter(1), reverse=True)
    sorted_parent_parent_count = sorted(parent_parent_member_count.items(), key=operator.itemgetter(1),reverse=True)
    sorted_parent_intersect_count = sorted(parent_intersect_member_count.items(),key=operator.itemgetter(1) ,reverse=True)

    ########
    ## create dict to map DOIDs that have the same parent or itself exists in the dataset
    ########
    # HERE>> modify paren_children_dict so that it all keys are qualify.
    parent_children_dict = create_uniq_parents_children_dict(sorted_parent_count, parent_diseaseId_DO_mapping)
    parent_parent_children_dict = create_uniq_parents_children_dict(sorted_parent_parent_count, parent_parent_diseaseId_DO_mapping)

    label_children_dict = remove_unqualify_key(parent_children_dict, parent_parent_children_dict)
    #######################3
    # Verbose
    ######################

    # #####
    # #print parent and children_count from dict
    # ####
    # print("print parent and children_count from dict....")
    # print(get_keys(sorted_parent_count,20))
    # print(get_keys(sorted_parent_parent_count,20))
    # print(get_keys(sorted_parent_intersect_count,20))
    # exit()
    #
    return label_children_dict

def create_uniq_parents_children_dict(sorted_parent_intersect_count, parent_diseaseId_DO_mapping):
    '''
    create dict to map DOIDs that have the same parent or itself exists in the dataset

    :param sorted_parent_intersect_count: [('parent_doid', 'number of children')]
    :param parent_diseaseId_DO_mapping:
    :return: uniq_parens_children_dict: {'parent_doid': [list of uniq_children doid,..] ,...}
    '''

    # select the first 15 paretns_doid
    # parent_children_dict = {parent: [] for i, parent in enumerate(get_keys(sorted_parent_intersect_count, 16))}

    #select all parents_doid
    parent_children_dict = {parent: [] for i, parent in enumerate(get_keys(sorted_parent_intersect_count))}

    parent_ind = None
    children_ind = None
    for i, line in enumerate(parent_diseaseId_DO_mapping):
        val_split = line.split(",")
        if i == 0:
            for j, val in enumerate(val_split):
                if val == 'parentID':
                    parent_ind = j
                if val == 'diseaseID' or val == '1diseaseID':
                    children_ind = j
        if i != 0:
            # append children_doid to the first 15 prents_dodid
            if val_split[parent_ind] in parent_children_dict.keys():
                parent_children_dict[val_split[parent_ind]].append(val_split[children_ind])

    # parent_children_count = [len(val) for val in parent_children_dict.values()] # sum of len = 1043
    # sorted_parent_children_count = sorted(parent_children_count, reverse=True)
    # print(sum(sorted_parent_children_count[:20]))

    ###############
    # checking uniq_children doid before moving on
    ##############
    # below should be the right one. sum len = 499
    # parent_children_count = [len(set(val)) for val in parent_children_dict.values()] # sumd of len = 499;
    # sorted_parent_children_count = sorted(parent_children_count, reverse=True)
    # #print(sorted_parent_children_count[:20])
    # print(sum(sorted_parent_children_count[:20]))

    # # parent_children_count = [val_list for val_list in list(parent_children_dict.values()) ]
    # parent_children_count = [val for val_list in parent_children_dict.values() for val in val_list]
    # print(len(parent_children_count))
    # print(len(set(parent_children_count)))
    # exit()

    return {key:set(val) for key,val in parent_children_dict.items()}

############
## this needs to be refactor
############
# def remove_parent_key(parent_children_dict,parent_list1, illegal_key_list, **kwargs):
#     '''
#     remove illegal key and append illegal key to legal parent key
#
#
#     :param parent_children_dict: [parent_doid: [uniq_children_doid]]
#                             param whose keys will be deleted and are appended new value
#     :param parent_list1: parent_children_list;
#                             list of keys of parent_children_dict
#     :param illegal_key_list:
#     :param **kwards: parent_list2: parent_parent_children_list
#     :return:
#     '''
#
#     parent_list2 = None
#
#     for key, val in kwargs.items():
#         parent_list2 = val
#
#     children2parent_dict1 = {val: key for key, val_list in parent_children_dict.items() for val in val_list}
#     children2parent_dict2 = {val: key for key, val_list in parent_children_dict.items() for val in val_list}
#
#     for key in parent_list1:
#         if key in illegal_key_list:
#             #append parent1_list[key] to the correct parent and remove illegal key
#             new_parent = children2parent_dict1[key]
#             print(key)
#             try:
#                 parent_children_dict = list(parent_children_dict)
#                 parent_children_dict[new_parent].append(parent_children_dict[key])
#
#                 del parent_children_dict[key]
#             except:
#                 print("children of {:s} key is already added to {:s} new_parent".format(key, new_parent))

def remove_unqualify_key(parent_children_dict, parent_parent_children_dict):
    '''
    unqualified keys are keys that are both parentDOID and childrenDOID.
    class label (in this case parentDOID) must not be parent or children of other class label.
    In the other word, class labels must be independent to each other ( or at least appear to be independent to us, data sciencetist)

    :return: dict with keys that is qualified in the followign format
            {class_label: [list of uniq doid]}
    '''
    print()
    print("removing illegal keys from parent_children_dict...")
    parent1_list = list(parent_children_dict.keys())

    children1_list = [val for val_list in parent_children_dict.values() for val in val_list]

    parent2_list = list(parent_parent_children_dict.keys())
    children2_list = [val for val_list in parent_parent_children_dict.values() for val in val_list]

    #num of children in parent1_list
    print("len before illegal keys are remove = ", len(children1_list))

    illegal_key_list1 = set(parent1_list).intersection(set(children1_list))
    illegal_key_list2 = set(parent2_list).intersection(set(children2_list))
    illegal_key_list3 = set(parent2_list).intersection(set(children1_list))

    #if list of illegal keys are not 0, call remove_parent_key() to remove illegal key
    print("list of illegal keys set1 = ", len(illegal_key_list1))
    print("list of illegal keys set2 = ", len(illegal_key_list2))
    print("list of illegal keys set3 = ", len(illegal_key_list3))
    all_val_list = []
    removed_keys_list =[]

    #remove illegal key and append illegal key to legal parent key
    ###############
    ## function needs to be refactor
    ###############
    # remove_parent_key(parent_children_dict, parent1_list, illegal_key_list1)
    # remove_parent_key(parent_parent_children_dict, parent2_list, illegal_key_list2)
    # remove_parent_key(parent_parent_children_dict, parent1_list, illegal_key_list3, parent2_list=parent2_list)

    children2parent_dict1 = {val: key for key, val_list in parent_children_dict.items() for val in val_list}
    children2parent_dict2 = {val: key for key, val_list in parent_parent_children_dict.items() for val in val_list}

    # children2parent_dict3 contains keys of parent_parent_children_dict that is in val of parent_children_dict where val is valid_doid
    # children2parent_dict3 = {doid: parent_parent_key}
    children2parent_dict3 = {}
    parent_parent_valid_doid_dict = {} # {parent_parent_key: [list of valid doid]}
    with open('dataset/disease_mappings_umls/parent_parent_valid_diseaseId_uniq_DO_mapping.txt', 'r') as f:
        data = f.readlines()
        parent_ind = None
        valid_doid_ind = None

        for i, line in enumerate(data):
            val_list = line.split(",")
            # key: deseseId, vocab, code, vocabName
            if i == 0:
                for j, val in enumerate(val_list):
                    col = val.lower().strip()
                    # if val in ["parentId".lower(),'diseaseId'.lower()]:
                    if col in ["parentid"]:  # doid; col to be mapped to its parent
                        parent_ind = j
                    if col in ["valid_doid"]:  # doid that has mapping to uniq_cuis
                        valid_doid_ind = j
            if i != 0:
                # create parent_parent_valid_doid_dict
                if val_list[parent_ind] in parent_parent_valid_doid_dict.keys():
                    parent_parent_valid_doid_dict[val_list[parent_ind]].append(val_list[valid_doid_ind])
                else:
                    parent_parent_valid_doid_dict[val_list[parent_ind]] = [val_list[valid_doid_ind]]
                # create parent2doid_dict
                if val_list[valid_doid_ind] in children2parent_dict3.keys():
                    #check if doid maps to the same parent
                    assert val_list[parent_ind].strip() in children2parent_dict3[val_list[valid_doid_ind]], "doid = {:s} has more than 1 parents mapping".format(val_list[valid_doid_ind])
                else:
                    children2parent_dict3[val_list[valid_doid_ind]] = val_list[parent_ind]


    #remove key in the case of illegal_key_list1
    print("removing keys from illegal_keys_list1...")

    # candidate keys are keys whose parent is '7'
    # but 7 has too many big subset that can be used as label,
    # so I will not use 7 but use its candidate keys
    candidate_keys_list = []
    for key in parent1_list:
        if key in illegal_key_list1:
            #append parent1_list[key] to the correct parent and remove illegal key
            new_parent = children2parent_dict1[key]
            print(key)
            try:
                if new_parent == '7':
                    candidate_keys_list.append(key) #77,863,74,28,2914,1287,8633,17
                else:
                    parent_children_dict[new_parent] = list(parent_children_dict[new_parent])
                    parent_children_dict[new_parent].append(parent_children_dict[key])
                    del parent_children_dict[key]
            except:
                print("children of {:s} key is already added to {:s} new_parent".format(key, new_parent))

    #remove key in the case of illegal_key_list2
    print("removing keys from illegal_keys_list2...")


    for key in parent2_list:
        if key in illegal_key_list1:
            #append parent1_list[key] to the correct parent and remove illegal key
            new_parent = children2parent_dict2[key]
            print(key)

            try:
                parent_parent_children_dict[new_parent] = list(parent_parent_children_dict[new_parent])

                parent_parent_children_dict[new_parent] = parent_parent_children_dict[new_parent] + parent_parent_valid_doid_dict[key]

                del parent_parent_children_dict[key]
            except:
                print("children of {:s} key is already added to {:s} new_parent".format(key, new_parent))

    #HERE>> check whether children of parent_parent_children_dict is doid that has mapping to cui.
    #        if the answer is yes, one can append children of parent_children_dict to parent_parent_children_dict, not vice versa
    print("removing keys from illegal_keys_list3...")
    for key in parent2_list:
        if key in illegal_key_list3:
            #append parent2_list[key] to the correct parent and remove illegal key

            # [150,630,0014667] does not recognized as valid_doid.
            #  The exact problem is stated in the read_json_from_url
            # KeyError: '150' and '630' and '0014667'
            if key in children2parent_dict3.keys():
                new_parent = children2parent_dict3[key]  # key = valid_doid and new parent = key of parent_parent_children_dict

            else:
                print("{:s} is not a key in chidren2parent_dict3".format(key))
            try:
                if key in candidate_keys_list: #77,863,74,28,2914,1287,8633,17
                    parent_parent_children_dict[key] = parent_parent_valid_doid_dict[key]
                else:
                    parent_parent_children_dict[new_parent] = list(parent_parent_children_dict[new_parent])
                    parent_parent_children_dict[new_parent] = parent_parent_children_dict[new_parent] + parent_parent_valid_doid_dict[key]

                    del parent_parent_children_dict[key]
            except:
                print(key)
                print(new_parent)
                print("children of {:s} key is already added to {:s} new_parent".format(key, new_parent))

    ## check length of val whose key of parent_parent_children_dict is candidate keys
    # for key in candidate_keys_list:
    #     print("label = {:s}, count ={:d}".format(key, len(parent_parent_children_dict[key])))

    ########3
    ## print out len of uniq val after illegal keys are removed
    #########
    # for i, (key, val) in enumerate(parent_parent_children_dict.items()):
    #     # exclude class that are illegal
    #     parent_parent_children_dict[key] = set(val)
    #     if key in illegal_key_list:
    #         print("removing key={:s} which has {:d} doids mapping".format(key,len(val)))
    #         removed_keys_list.append(key)
    #     else:
    #         for v in val:#all v should be uniq
    #             if v not in illegal_key_list:
    #                 if v in parent_children_dict.keys():
    #                     uniq_doid_list = list(parent_children_dict[v]) + [v]
    #                     all_val_list += set(uniq_doid_list)
    #                 else:
    #                     all_val_list += v

    # #remove illegal keys_list from label_children_dict
    # for key in removed_keys_list:
    #     if key in parent_parent_children_dict.keys():
    #         parent_parent_children_dict.pop(key, None)

    label_children_dict = parent_parent_children_dict
    return label_children_dict

### I may have to change mehtod name to something else
## or I may have to create read file for all of the different cases that encounter the way
def create_cuis_list_from_file(file_path=None, selected_key=None):
    '''
    file's format must be as follow to be qualified as "horizontal"

        key,val1,val2,val3,....
        key1,val1,val2,val3,....
        key2,val1,val2,val3,....
        key3,val1,val2,val3,....

    :param file_path:
    :param selected_key:
    :return: list of uniq_CUIs
    '''
    print("creating cuis_list from {:s}".format(file_path))
    data = None
    dict_key_val = {}

    if file_path is None:
        print("path to file is not specified. Please specified file_path to be read.")
    else:
        with open(file_path, 'r') as f:
            data = f.readlines()

    if selected_key is None:
        uniq_CUIs = []
        for i, line in enumerate(data):
            val_split = line.split(",")
            key = val_split[0].strip()
            if key == 'diseaseId':
                uniq_CUIs = set(val_split[1:])
    else:
        #####fix code block below#####
        uniq_CUIs = []
        for i, line in enumerate(data):
            val_split = line.split(",")
            key = val_split[0].strip()
            if key == 'diseaseId':
                uniq_CUIs = val_split[1:]

    return uniq_CUIs

def create_class_CUIs_dict_from_file(file_path, label_list):
    '''

    :param file_path:
    :param label_list: list of class_labels: [label1,label2,....]
    :return: dict: {label: [list of uniq_cuis]}
    '''
    print("creating label: [list of uniq_cuis]...")
    class_CUIs_dict = {label: [] for label in label_list}
    DO_ind = None
    CUI_ind = None
    count = 0

    with open(file_path, 'r') as f:
        data = f.readlines()

    for i, line in enumerate(data):  # there are 6109 uniq disease
        val_split = line.split(",")
        if i == 0:
            for j, val in enumerate(val_split):
                val = val.strip().lower()
                if val == 'code'.lower():
                    DO_ind = j
                if val == 'diseaseid':
                    CUI_ind = j
        if i != 0:

            for label in parent_children_dict.keys():
                val_split[DO_ind] = val_split[DO_ind].strip()
                if val_split[DO_ind] in parent_children_dict[label]:
                    class_CUIs_dict[label].append(val_split[CUI_ind])

    return class_CUIs_dict

if __name__ == "__main__":
    PubAnnotator_file_path = "dataset/demo_dataset/PubAnnotator_instances.txt"
    gene_disease_uniq_file_path = "dataset/generated_dataset/gene_disease_uniq.txt"
    gene_disease_1000_file_path = "dataset/generated_dataset/gene_disease_1000_no_None.txt"

    gene_disease_uniq_DO_mapping_file_path = 'dataset/disease_mappings_umls/gene_disease_uniq_DO_mapping.txt'

    # ##########
    # # map CUIs from gene_disesae_uniq.txt to DO in disease_mappings and write to file
    # ##########
    # save_path = "dataset/disease_mappings_umls/gene_disease_uniq_DO_mapping.txt"
    #
    # source_mapping_dict = create_DO_mapping_from_source()
    # all_CUIs_Do_dict = Map_uniq_CUIs_to_DO(source_mapping_dict)#map uniq_cuis_to_do
    # Write2file(save_path, all_CUIs_Do_dict, vertical=True)

    # #######
    # # map DOID to its parents' diseaseId
    # #######
    # disease_mapping_path= 'dataset/disease_mappings_umls/gene_disease_uniq_DO_mapping.txt'
    # save_parent_mapping = 'dataset/disease_mappings_umls/parent_diseaseId_uniq_DO_mapping.txt'
    # read_json_from_url(disease_mapping_path, save_parent_mapping, "diseaseID,parentID,parentName")
    #######
    # map parent DOID to its parents' diseaseId
    #######
    # disease_mapping_path = 'dataset/disease_mappings_umls/parent_diseaseId_uniq_DO_mapping.txt'
    # save_parent_mapping = 'dataset/disease_mappings_umls/parent_parent_diseaseId_uniq_DO_mapping.txt'
    # # "diseaseID,parentID,parentName" is equvalent of "parentID,parent_parentID,parent_parentName"
    # read_json_from_url(disease_mapping_path, save_parent_mapping, "diseaseID,parentID,parentName")

    #######
    # map valid doid to parent parent doid
    # > valid_doid is doid that has mapping to uniq_cuis
    #   (or doid that contains in gene_disease_uniq_DO_mapping.txt"
    #######
    # uniq_do_mapping_file_path = 'dataset/disease_mappings_umls/gene_disease_uniq_DO_mapping.txt'
    # disease_mapping_path = 'dataset/disease_mappings_umls/parent_diseaseId_uniq_DO_mapping.txt'
    # save_parent_mapping = 'dataset/disease_mappings_umls/parent_parent_valid_diseaseId_uniq_DO_mapping.txt'
    # read_json_from_url(disease_mapping_path, save_parent_mapping, "valid_doid,parentID,parentName", verify_doid=True)
    ########
    ## count uniq parent DOID
    ########
    parent_mapping_file_path = 'dataset/disease_mappings_umls/parent_diseaseId_uniq_DO_mapping.txt'
    parent_parent_mapping_file_path = 'dataset/disease_mappings_umls/parent_parent_diseaseId_uniq_DO_mapping.txt'

    parent_mapping = get_uniq_parent(parent_mapping_file_path, 'parent_mapping')
    parent_parent_mapping = get_uniq_parent(parent_parent_mapping_file_path, 'parent_parent_mapping')


    # ## check intersection of paretn an parent_parent set
    parent_intersect = parent_mapping.intersection(parent_parent_mapping)
    print("number of uniq parent mapping=", len(parent_mapping))
    print("number of uniq parent parent mpping =", len(parent_parent_mapping))
    print("number of uniq parent intersection =", len(parent_intersect))

    ##count number of childrem member of each parent member of set
    ##then pick number of subset that have the most member with least amount of uniq parent code

    ######################
    ## step to collect dataset that belongs to the Mega_classes:
    ##
    ## >TOP Down serch started from Mega class and link its children to it
    ######################

    # HERE>>

    ######################
    ## step to collect dataset that belongs to the given classes
    ######################

    #######
    # STEP1
    # 1.create dict to map DOIDs that have the same parent or itself exists in the dataset
    # select 8 qualify labels that has the most number of uniq_doid
    ######
    parent_children_dict = create_parent_children_DO_dict(parent_mapping_file_path, parent_parent_mapping_file_path) #return: {parent_DOID: [list of children_DOID]}

    parent_member_count = {key:len(val) for key, val in parent_children_dict.items()}
    sorted_parent_count = sorted(parent_member_count.items(), key=operator.itemgetter(1), reverse=True)

    # for (label, count) in sorted_parent_count[:15]:
    #     print("label = {:s}, count = {:d}".format(label, count))

    # selected_label = ['0050686','16','3093','0080001','863','77','0050117','66']# file with these classes haven't created yet

    ##############33
    ## here>> figure out whether or notselected_albel above has been mapping to uniq_cuis and write to file.
    ## > I don't think i did that yet
    ###############
    # append parent of other classes that is a children to these classes
    # print("at 783")
    # exit()

    # (label, uniq_doid_count) of the first 20 in decending order
    # ('7', 28), ('0050686', 26), ('225', 15), ('1492', 14), ('0050687', 12), ('0050828', 12), ('18', 12), ('0050338', 11)
    #
    # below is the corresponding key of the above len.
    # 0050736,225,0050737,936,37,934,2256,0080015,0050338,5614,9252,1826,0050889,2978,2214,0060309,0050565,

    #######
    # STEP2
    # 2.create dict that map DOID to its corresponding uniq CUIs
    ######

    uniq_CUIs =  create_cuis_list_from_file(gene_disease_uniq_file_path)
    # </editor-fold>
    #santiy check before moving on
    assert len(uniq_CUIs) == len(set(uniq_CUIs)), "some CUIs in 'uniq_CUIs' are not uniq."

    ###########
    ## >> get diseaseId/cuis of gene_disease_1000
    ###########
    cui_1000_list = create_cuis_list_from_file(gene_disease_1000_file_path)
    # print(len(cui_1000_list)) #1000 cuis
    # print(len(set(cui_1000_list))) #240 uniq cuis
    # exit()

    parent_ind = None
    children_ind = None

    ###################
    # checking number of uniq_children_doid and uniq_class_label before moving on to step 3
    ###################

    # list of len of uniq doid children
    len_uniq_children = [len(val_list) for val_list in parent_children_dict.values()]
    '''
        [64, 62, 27, 47, 16, 26, 25, 22, 20, 3, 11, 16, 24, 34]
    '''

    label_list = [parent for parent in parent_children_dict.keys()]
    # print(len(label_list)) # 14 labels

    DO_list = [child for child_list in parent_children_dict.values() for child in child_list]
    # print(len(DO_list)) # total len of uniq dodid children  = 397
    # exit()

    ###################################3
    ## STEP 3
    # 3. create file containing all uniq_diseaseid and its class in the following format
    #  diseaseid,class >> file = CUIs_label_mapping.txt
    #
    #####################################

    class_CUIs_dict = create_class_CUIs_dict_from_file(gene_disease_uniq_DO_mapping_file_path, label_list)

    # #######
    # ## check number of tototal number of uniq_cuis that have mappping to its label
    # #######
    # x = [val for vals in class_CUIs_dict.values() for val in vals]
    # # print(x) # { label: [list of cuis]}
    #
    # # from uniq cuis of 6110, there are 814 cuis that have a mapping to 14 chosen classes.
    # print("number of uniq cuis that have mapping to selected classes: ", len(x))
    # print()
    # exit()
    ##################

    # below step explais how uniq_cuis got reduced from 9434 to 813
    # 1. cuis to do mapping (some cuis have no do mapping at all)
    # 2. some of the doid cannot be used with given API from DO website. (31 doids; RELATIVE SMALL NUMBER OF DOID  )
    # 3. some doid do not belong to any of the selcted 14 classes.

    ###########33
    # save {class: [list of diseaseId]} in file
    ###########
    print("at 897")
    exit()
    save_path = 'dataset/disease_mappings_umls/uniq_CUIs_label_mapping.txt'
    # Write2file(save_path, class_CUIs_dict, vertical =True)

    with open(save_path, "w") as f:
        f.write("diseaseId,class")
        print("writing to {:s}".format(save_path))
        f.write('\n')
        # diseaseId_mapping = {class : [list of DO]}
        for key, val_list in class_CUIs_dict.items():
            for val in val_list:
                sent = val+','+key+'\n'
                f.write(sent)

    ##############
    ## STEP 4
    # 4. add class label gene_diesase file such as gene_disease_1000 (with None class) and gene_disease_1000_no_None (no None Class)
    #   > class label to append gene_disease_1000 >> called it gene_disease_1000_label.txt
    # >> HERE: if there is no mapping to cuis in gene_disease_1000, put None in it. (None represent no class label)
    # note: later we can use none class label to predict node classification
    ##############

