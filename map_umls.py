####################
### todo for this file
# Goal: make this file readable. make it easier to read.
#> refactor method and function
# >write comment on important function/method/step
###################


import operator

def create_diseaseId_dict(file_path):
    with open(file_path, "r") as f:
        file = f.readlines()
    DiseaseId_dict = {}
    DiseaseId_dict = {}
    for line in file:
        line_split = line.split(",")

        key = line_split[0].strip()
        # if key == "diseaseId":
        if key == "code":
            val_list = line_split[1:]
            val_list[-1] = val_list[-1].strip()

            val_list = set(val_list)
            DiseaseId_dict[key] = val_list
    return DiseaseId_dict

def create_DO_mapping_from_source(DiseaseId_dict): # there might be something wrong here.
    '''
    create mapping_dict from DO source extracted from disease_mappings.tsv (downloaed from the site)
    :param DiseaseId_dict:
    :return:
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
    mapping_dict = {header: [] for header in header_list}
    for i, line in enumerate(data[1:]):
        val_list = line.split("|")
        # only use map to DO vocabulary
        if val_list[2] == 'DO':
            for j, (header, val) in enumerate(zip(header_list, val_list)):
                mapping_dict[header].append(val)

    dict = [[diseaseId, vocab, code, vocabName]for diseaseId, vocab, code, vocabName in zip(mapping_dict['diseaseId'],mapping_dict['vocabulary'], mapping_dict['code'], mapping_dict['vocabularyName\n'])]

    diseaseId_mapping = {}
    # diseaseId_vocabName = {}
    for key,val_list in DiseaseId_dict.items():
        for val in val_list:
            for mapped_list in dict:
                if val == mapped_list[0]:
                    diseaseId_mapping[val] = mapped_list

    return mapping_dict

def Write2file(save_path,diseaseId_mapping):
    ############3
    ## write to files
    ############3
    # save_path = "dataset/disease_mappings_umls/gene_disease_1000_DO_mapping.txt"

    # save_path = "dataset/disease_mappings_umls/PubAnnotator_DO_mapping.txt"
    # save_path = "dataset/disease_mappings_umls/diseaseId_DO_mapping.txt"
    with open(save_path, "w") as f:
        # f.write("deseseId,vocab,code,vocabName")
        f.write('\n')
        # diseaseId_mapping = {CUIS : [diseaseId, vocab, code, vocabName]}
        for key, val in diseaseId_mapping.items():
            sent = ",".join(val)
            f.write(sent)

def read_json_from_url(file_path, save_path):
    '''

    :param file_path: diseaseID_DO_mappings.
    :return:
    '''
    #############
    ## read file
    #############
    with open(file_path, 'r') as f:
        data = f.readlines()
    DOID_code_list = []
    ind = None
    for i, line in enumerate(data):
        val_list = line.split(",")
        # key: deseseId, vocab, code, vocabName
        if i ==0:
            for j, val in enumerate(val_list):
                if val == "parentID" or val == "code":
                    ind = j
        if i != 0:
            DOID_code_list.append(val_list[ind])

    #############
    import requests
    import json

    with open(save_path, "w") as f :
        f.write("diseaseID,parentID, parentName")
        f.write("\n")
        for code in DOID_code_list:
            try:
                link = "http://www.disease-ontology.org/api/metadata/DOID:%s" % code
                response = json.loads(requests.get(link).text)
                # print(response['parents']) # ["relationship", "diseaseName", "DOID of diseaseName"]
                #
                # 'DOID:0050686'
                DOID_code = response['parents'][0][2].split(":")
                DOID_code = DOID_code[1]
                parent_DOID_Name = DOID_code+','+ response['parents'][0][1]
                line = code+ "," +parent_DOID_Name
                f.write(line)
                f.write("\n")
                #map uniq DIOD to its parents
            except:
                print("code=", code)

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

def get_keys(key_val_list, max_len ):
    '''
    print dictionary containing tuple {parent_DOID: children's count}
    :param key_val_list: [('parent_doid', 'number of children')]
    :return: list of parent_dodid: ['parent_doid',...]
    '''
    print()
    print("number of chosen uniq class mapping = ", len(key_val_list))
    key_list = []
    for i,key_val in enumerate(key_val_list):
        if i <= max_len:
            print(key_val[0],end=",")

            key_list.append(key_val[0])
    print()
    return key_list

def get_children():
    '''

    :return: {parent_DOID: [list of children_DOID]}
    '''
    parent_diseaseId_DO_mapping = 'dataset/disease_mappings_umls/parent_diseaseId_DO_mapping.txt'
    # get children DOID
    with open(parent_diseaseId_DO_mapping, 'r') as f:
        parent_diseaseId_DO_mapping = f.readlines() # diseaseId is not uniq in this case

    parent_ind = None
    children_ind = None

    parent_member_count = {parent: 0 for parent in parent_mapping}
    parent_parent_member_count = {parent: 0 for parent in parent_parent_mapping}
    parent_intersect_member_count = {parent: 0 for parent in parent_intersect}

    #only do the first 16 because I only need 16

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

    # x = [freq for (id, freq) in sorted_parent_count]
    ## children count of the first 20 members:
    # print(x[:20])  # [151, 112, 93, 71, 68, 59, 50, 50, 48, 47, 46, 46, 42, 42, 40, 40, 38, 35, 34, 34]
    ########
    ## create dict to map DOIDs that have the same parent or itself exists in the dataset
    ########
    parent_children_dict = create_uniq_parents_children_dict(sorted_parent_count, parent_diseaseId_DO_mapping)

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
    return parent_children_dict

def create_uniq_parents_children_dict(sorted_parent_intersect_count, parent_diseaseId_DO_mapping):
    '''
    create dict to map DOIDs that have the same parent or itself exists in the dataset

    :param sorted_parent_intersect_count: [('parent_doid', 'number of children')]
    :param parent_diseaseId_DO_mapping:
    :return: uniq_parens_children_dict: {'parent_doid': [list of uniq_children doid,..] ,...}
    '''

    # select the first 15 paretns_doid
    parent_children_dict = {parent: [] for i, parent in enumerate(get_keys(sorted_parent_intersect_count, 16))}

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

def remove_unqualify_key(parent_children_dict):
    '''
    unqualified keys are keys that are both parentDOID and childrenDOID.
    class label (in this case parentDOID) must not be parent or children of other class label.
    In the other word, class labels must be independent to each other ( or at least appear to be independent to us, data sciencetist)

    :return: dict with keys that is unqualified. {}
    '''
    all_val_list = []
    temp = parent_children_dict
    for i, (key, val) in enumerate(temp.items()):
        # exclude class that are illegal
        parent_children_dict[key] = set(val)
        if key in ['225', '1826', '936']:
            pass
            # print(len(set(val)))
        else:
            all_val_list += set(val)

    parent_children_dict.pop('225', None)
    parent_children_dict.pop('1826', None)
    parent_children_dict.pop('936', None)

    ##  from total of 499 uniq_childrenDOID to 397 uniq_childrenDOID
    # print(len(set(all_val_list))) # 397 uniq_DOID of childrean_DOID
    # print(len(all_val_list)) # 397

    return parent_children_dict

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
    :return:
    '''
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
                uniq_CUIs = val_split[1:]
    else:
        uniq_CUIs = []
        for i, line in enumerate(data):
            val_split = line.split(",")
            key = val_split[0].strip()
            if key == 'diseaseId':
                uniq_CUIs = val_split[1:]

    return uniq_CUIs

# HERE>>how to deal with class_CUIs_dict. it is not passed in, but it is previously computed somewhere
# please change this. this is a bad coding
def create_class_CUIs_dict_from_file(file_path):
    '''

    :param file_path:
    :return:
    '''
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
                if val == 'code':
                    DO_ind = j
                if val == 'diseaseId':
                    CUI_ind = j
        if i != 0:

            for label in parent_children_dict.keys():
                if val_split[DO_ind] in parent_children_dict[label]:
                    class_CUIs_dict[label].append(val_split[CUI_ind])

    return class_CUIs_dict

if __name__ == "__main__":
    PubAnnotator_file_path = "dataset/demo_dataset/PubAnnotator_instances.txt"
    gene_disease_uniq_file_path = "dataset/generated_dataset/gene_disease_uniq.txt"
    gene_disease_1000_file_path = "dataset/generated_dataset/gene_disease_1000.txt"

    gene_disease_1000_label_file_path = "dataset/demo_dataset/gene_disease_1000_label.txt"
    gene_disease_50000_label_file_path = "dataset/demo_dataset/gene_disease_50000_label.txt"

    gene_disease_uniq_DO_mapping_file_path = 'dataset/disease_mappings_umls/gene_disease_uniq_DO_mapping.txt'
    # ##########
    # # map CUIs to DO and write to file
    # ##########
    # save_path = "dataset/disease_mappings_umls/gene_disease_uniq_DO_mapping.txt"
    # DiseaseId = create_diseaseId_dict(gene_disease_uniq_file_path)
    # mapping_dict = create_DO_mapping_from_source(DiseaseId)
    # Write2file(save_path, mapping_dict)

    # #######
    # # map DOID to its parents' diseaseId
    # #######
    # # disease_mapping_path = 'dataset/disease_mappings_umls/gene_disease_uniq_DO_mapping.txt'
    # disease_mapping_path= 'dataset/disease_mappings_umls/parent_diseaseId_DO_mapping.txt'
    # save_parent_mapping = 'dataset/disease_mappings_umls/parent_parent_diseaseId_DO_mapping.txt'
    # read_json_from_url(disease_mapping_path, save_parent_mapping)

    ########
    ## count uniq parent DOID
    ########
    parent_mapping_file_path = 'dataset/disease_mappings_umls/parent_diseaseId_DO_mapping.txt'
    parent_parent_mapping_file_path = 'dataset/disease_mappings_umls/parent_parent_diseaseId_DO_mapping.txt'

    parent_mapping = get_uniq_parent(parent_mapping_file_path, 'parent_mapping')
    parent_parent_mapping = get_uniq_parent(parent_parent_mapping_file_path, 'parent_parent_mapping')


    # ## check intersection of paretn an parent_parent set
    parent_intersect = parent_mapping.intersection(parent_parent_mapping)
    print("number of uniq parent mapping=", len(parent_mapping))
    print("number of uniq parent parent mpping =", len(parent_parent_mapping))
    print("number of uniq parent intersection =", len(parent_intersect))

    ##count number of childrem member of each parent member of set
    ##then pick number of subset that have the most member with least amount of uniq parent code
    # gene_disease_uniq_DO_mapping = 'dataset/disease_mappings_umls/gene_disease_uniq_DO_mapping.txt'

    ######################
    ## step to collect dataset that belongs to the given classes
    ######################

    #######
    # STEP1
    # 1.create dict to map DOIDs that have the same parent or itself exists in the dataset
    ######
    parent_children_dict = get_children() #return: {parent_DOID: [list of children_DOID]}
    # len of children count of the first 20 in decending order
    # = [151, (112), 93, (71), 68, 59, 50, 50, 48, 47, 46, (46), 42, 42, 40, 40, 38]
    #
    # below is the corresponding key of the above len.
    # 0050736,225,0050737,936,37,934,2256,0080015,0050338,5614,9252,1826,0050889,2978,2214,0060309,0050565,

    ###############33
    # remove keys that are both parentDOID and childrenDOID
    parent_children_dict = remove_unqualify_key(parent_children_dict)

    #######
    # STEP2
    # 2.create dict that map DOID to its corresponding uniq CUIs
    ######

    uniq_CUIs =  create_cuis_list_from_file(gene_disease_uniq_file_path)
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

    class_CUIs_dict = create_class_CUIs_dict_from_file(gene_disease_uniq_DO_mapping_file_path)
    exit()

    DO_ind = None
    CUI_ind = None
    count = 0

    with open(gene_disease_uniq_DO_mapping_file_path, 'r') as f:
        gene_disease_uniq_DO_mapping = f.readlines()

    for i, line in enumerate(gene_disease_uniq_DO_mapping): # there are 6109 uniq disease
        val_split = line.split(",")
        if i == 0:
            for j, val in enumerate(val_split):
                if val == 'code':
                    DO_ind = j
                if val == 'diseaseId':
                    CUI_ind = j
        if i != 0:

            for label in parent_children_dict.keys():
                if val_split[DO_ind] in parent_children_dict[label]:
                    class_CUIs_dict[label].append(val_split[CUI_ind])

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

    # below step shows how uniq_cuis got reduced from 6110 to 814
    # 1. cuis to do mapping (some cuis have no do mapping at all)
    # 2. some of the doid cannot be used with given API from DO website. (31 doids; RELATIVE SMALL NUMBER OF DOID  )
    # 3. some doid do not belong to any of the selcted 14 classes.

    # ###########33
    # # save {class: [list of diseaseId]} in file
    # ###########
    # save_path = 'dataset/disease_mappings_umls/uniq_CUIs_label_mapping.txt'
    #
    # with open(save_path, "w") as f:
    #     f.write("diseaseId,class")
    #     f.write('\n')
    #     # diseaseId_mapping = {class : [list of DO]}
    #     for key, val_list in class_CUIs_dict.items():
    #         for val in val_list:
    #             sent = val+','+key+'\n'
    #             f.write(sent)
    # exit()

    ##############
    ## STEP 4
    # 4. add class label gene_diesase file such as gene_disease_1000 (with None class) and gene_disease_1000_no_None (no None Class)
    #   > class label to append gene_disease_1000 >> called it gene_disease_1000_label.txt
    # >> HERE: if there is no mapping to cuis in gene_disease_1000, put None in it. (None represent no class label)
    # note: later we can use none class label to predict node classification
    ##############

    ##################3
    ## create label for gene_disease_1000 (with None class)
    ################
    with open(gene_disease_1000_file_path, 'r') as f:
        gene_disease_1000 = f.readlines()
    save_path = 'dataset/demo_dataset/gene_disease_1000_label.txt'

    from shutil import copyfile
    copyfile(gene_disease_1000_file_path, save_path)

    all_label_list = [label for label_list in class_CUIs_dict.values() for label in label_list]
    # print(len(all_label_list)) # there are 814 uniq_cuis
    # exit()

    with open(save_path, "a") as f:
        # diseaseId_mapping = {class : [list of DO]}
        label_1000_list = []

        gene_id = []
        gene_symbol = []
        diseaseId = []
        diseaseName=[]
        pmid=[]
        source=[]

        for line in gene_disease_1000:
            val_list = line.split(',')
            key = val_list[0].strip()
            val = val_list[1:]
            if key == 'geneId':
                gene_id.append(val)
            if key == 'geneSymbol': #geneSymbol is 1086 which is more
                gene_symbol.append(val)
            if key == 'diseaseId':
                diseaseId.append(val)
            if key == 'diseaseName':
                diseaseName.append(val)
            if key == 'pmid':
                pmid.append(val)
            if key == 'source':
                source.append(val)
            # if key == 'class':

            if key == 'diseaseId':
                cui_1000_list = val_list[1:]
                for i,cui in enumerate(cui_1000_list):
                    # print(i)
                    if cui in all_label_list:
                        for label in class_CUIs_dict.keys():
                            if cui in class_CUIs_dict[label]:
                                # print(cui)
                                # print(label)
                                label_1000_list.append(label)
                    else:
                        # print(cui)
                        label_1000_list.append("None")

        #there are 32 cuis out of 1000 that have mapping to 14 selected classes
        print(len(label_1000_list)) # 1000
        # exit()

        ## Sanity check that val length of all cols are the same.
        print(len(gene_id[0]), len(diseaseId[0]),len(diseaseName[0]),len(pmid[0]),len(source[0]),len(gene_symbol[0]))

        label_1000_list = ','.join(label_1000_list)
        f.write("class,"+label_1000_list)

    ##################3
    ## create label for
    # > gene_disease_50000_no_None (with None class)
    # > gene_disease_50000 (with None Class)
    ################
    gene_disease_50000_file_path = 'dataset/generated_dataset/gene_disease_50000.txt'

    with open(gene_disease_50000_file_path, 'r') as f:
        gene_disease_50000 = f.readlines()

    save_path = 'dataset/demo_dataset/gene_disease_50000_label_no_None.txt'

    from shutil import copyfile
    copyfile(gene_disease_50000_file_path, save_path)


    with open(save_path, "a") as f:
        # diseaseId_mapping = {class : [list of DO]}
        label_50000_list = []
        count = 0
        all_label_list = [label for label_list in class_CUIs_dict.values() for label in label_list]
        for line in gene_disease_50000:
            val_list = line.split(',')
            key = val_list[0].strip()
            val = val_list[1:]
            if key == 'diseaseId':
                cui_50000_list = val_list[1:]
                for i,cui in enumerate(cui_50000_list):
                    if cui in all_label_list:
                        for label in class_CUIs_dict.keys():
                            if cui in class_CUIs_dict[label]:
                                # print(cui)
                                # print(label)
                                count +=1
                                label_50000_list.append(label)
                    else:
                        # print(cui)
                        label_50000_list.append("None")

        # there are 1297 cuis out of 50000 that have mapping to 14 selected classes
        print("number of cuis that have mappting = ", count)  # 1297
        print(len(label_50000_list))

        label_50000_list = ','.join(label_50000_list)
        f.write("class,"+label_50000_list)




    ##################3
    ## create label for all_gene_disease (with None class)
    ################
