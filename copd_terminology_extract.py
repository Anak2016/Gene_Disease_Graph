import json
import requests
import time
######################
##### Goal is to collect terminology that have mapping in disease_mapping
######################
# query_start = ['copd', 'Chronic obstructive airway disease', 'Chronic Obstructive Airway Disease', 'Chronic Airflow Obstruction']
# vocab_query_dict = {'DO':[], 'EFO':[], 'HPO':[], 'ICD9CM': [], 'MSH':[], 'NCI OMIM':[], 'ORDO': []}
# copd_rel_term_list = []
# create dataframe from disease_gene.tsv, and Pubannotator
# while(query matches):
#   if query in "sentence" of Pubannotator
#       append matched word which has with all CAP to copd_rel_term_list(all CAP word is another terminology relted to copd)
#   if query in "diseaseName" of disease_gene.tsv
#       apppend to query_list
#   if query in "name": in disease_mappings
#         append "vocabularyName" to query_list
#     if query in "vocabularyName" in disease_mappings
#         append "name" to query_list

def merge_dict(dict1, dict2):

    # res = {**dict1, **dict2}
    key1 = set(dict1.keys())
    key2 = set(dict2.keys())

    for key in key2:
        if key not in dict1.keys():
            dict1[key] = dict2[key]
        else:
            dict1[key] = dict1[key] + dict2[key]

    return dict1

# def get_cui(disease_gene_file_path,doid_list):
#     '''
#
#     :param disease_gene_file_path: path to
#     :param doid_list: list of leaf_doid. (doid with no children)
#     :return:
#     '''
#

def create_cui2doid_dict(gene_disease_uniq_DO_mapping_file_path):
    '''

    :param gene_disease_uniq_DO_mapping_file_path: file has the following format
    col = diseaseId,code where diseaseId => cui and code => doid
            diseaseId,code
            cui1,doid1
            cui2,doid2
            ..., ...
    :return: {cui: doid}, {doid: [list of cui]}
    '''
    print("in def create_cui2doid_dict(gene_disease_uniq_DO_mapping_file_path):")
    print("creating {cui: doid}, {doid: [list of cui]}..........")
    doid2cui_dict = {}
    doid_ind = None
    cui_ind = None
    val_list = None
    col_list = None
    with open(gene_disease_uniq_DO_mapping_file_path) as f:
        for i, line in enumerate(f):

            if i == 0:
                col_list = line.split(',') #[cui, doid]
                for i,val in enumerate(col_list):
                    val = val.strip().lower()
                    if val == 'diseaseid':
                        cui_ind = i
                    if val == 'code':
                        doid_ind = i
            else:
                val_list = line.split(',')  # [cui, doid]
                if val_list[doid_ind] in doid2cui_dict.keys():
                    doid2cui_dict[val_list[doid_ind].strip()].append(val_list[cui_ind])
                else:
                    doid2cui_dict[val_list[doid_ind].strip()] = [val_list[cui_ind]]

    cui2doid_dict = {cui: doid for doid, cui_list in doid2cui_dict.items() for cui in cui_list}

    print("return {cui: doid}, {doid: [list of cui]}")
    return cui2doid_dict, doid2cui_dict

def create_label2cui_dict(all_label2leaf_dict, doid2cui_dict, save_path):
    '''

    :param all_label2leaf_dict: {label: [leaf_doid]}
    :param doid2cui_dict: {doid: [list of cui]}
    :param save_path:
    :return: {label: [list of cuis]}
    '''
    print("in def create_label2cui_dict(all_label2leaf_dict, doid2cui_dict, save_path):")
    print("creating {label: [list of cuis]}......")
    label2cui_dict = {}
    for label, leaf_list in all_label2leaf_dict.items():
        for doid in leaf_list:
            if doid in list(doid2cui_dict.keys()):
                if label in label2cui_dict.keys():
                    label2cui_dict[label] = label2cui_dict[label] + doid2cui_dict[doid]
                else:
                    label2cui_dict[label] = doid2cui_dict[doid]

    with open(save_path,'w') as f:
        print(f"writing {{label: [list of uniq_cui]}} to {save_path} ..... ")
        f.write("diseaseId,code")
        f.write("\n")
        for label, val_list in label2cui_dict.items():
            for cui in val_list:
                f.write(','.join([cui,label]))
                f.write('\n')

    print("return {label: [list of cuis]}")
    return label2cui_dict


def get_children_url(col_names,doid_label_dict, save_path, verbose = False):
    '''
    1.use doid api to extract list of children_doid from url. (url is constructed in json format)
    2.write to file in the following format
            doid,label

            doid1,label1
            doid2,label2
            ...  , ....

    :param col_names: string of col name to be wirttinen to the save_apth
    :param doid_label_dict: {'doid': label_of_doid}
    :param save_path:
    :return: {label: [children_doid]}
    '''
    print("in def get_children_url(col_names,doid_label_dict, save_path, verbose = False)")
    print("creating {label: [children_doid]}.........")
    with open(save_path, "w") as f :
        print(f"writing {{label: [children_doid]}} to {save_path} ..... ")
        f.write(col_names)
        # f.write("diseaseID,parentID, parentName")
        f.write("\n")

        all_parent2children_dict = {} # {parent_doid: [list of children_doid]}
        all_children2parent_dict = {} # (child_doid: parent_doid }

        all_leaf2label_dict = {} # {child_doid: label}
        all_label2leaf_dict = {label: [] for label in doid_label_dict.keys()} # {label: [list of children_doid]}

        unsearch_doid_dict = {}

        for label in doid_label_dict.keys():

            # setting is_leaf_empty to true to get tpas s the fist while loop,
            is_non_leaf_empty = True
            # the first key is selected to be searched for children recursiely until all children are leaves
            unsearch_doid_list = [label]

            # True until all leaves of the doid_label_dict.keys() are collected
            while(is_non_leaf_empty):

                if len(unsearch_doid_list) == 0:
                    # for readbility to show that there is no more non leaf to be searched
                    is_non_leaf_empty = False
                    print("all children_doid of label = {:s} are searched===========".format(label))
                    break

                code = unsearch_doid_list[0] #for each uniq doid code
                code = code.strip()
                link = "http://www.disease-ontology.org/api/metadata/doid:%s" % code
                response = json.loads(requests.get(link).text)

                try:
                    #removed searched doid
                    unsearch_doid_list.remove(code)

                    # "children": [["viral infectious disease", "doid:934"], ["parasitic infectious disease", "doid:1398"], .... ]}
                    res = response['children']

                    doid_code_list = [res[i][1].split(":")[1] for i in range(len(res))]

                    parent2children_dict = {code: [doid_code_list] }
                    children2parent_dict = {child: [code] for child in doid_code_list}

                    ## add new children to its parent
                    all_parent2children_dict = merge_dict(all_parent2children_dict, parent2children_dict)
                    all_children2parent_dict = merge_dict(all_children2parent_dict, children2parent_dict)

                    doid_name_dict = {res[i][1].split(":")[1]: res[i][0]for i in range(len(res))}

                    # append children_doid to be search for its children, recursively.
                    unsearch_doid_dict = merge_dict(unsearch_doid_dict, doid_name_dict)

                    unsearch_doid_list = unsearch_doid_list + doid_code_list
                    if verbose is True:
                        print(" ")
                        # print(len(unsearch_doid_dict.keys()))
                        print("{:s} has {:d} unsearched doid".format(label, len(unsearch_doid_list)))
                        print(f"{code} has children as followed: {doid_code_list}")

                        # print(code)
                        # print(";;;;;;;;;;;;;;;;;;;;;;;;;;;;;")
                        # print("{doid: 'doid_name', .... } =====> ",doid_name_dict)
                        # print("[doid_code1,doid_code2 .....]",doid_code_list)
                        # print(";;;;;;;;;;;;;;;;;;;;;;;;;;;;;")

                except Exception as e :
                    ###############3
                    ## Error occurs on "res = response['children']" line
                    ## This implies that "code" is a leaf doid
                    ###############3
                    leaf2label_dict = {code: [label]}
                    label2leaf_dict = {label: [code]}

                    ## add new children to its parent
                    #HERE>> check merge_dict func.
                    all_leaf2label_dict = merge_dict(all_leaf2label_dict, leaf2label_dict)
                    all_label2leaf_dict = merge_dict(all_label2leaf_dict, label2leaf_dict)

                    if verbose is True:
                        print("doid:{:s} is a leaf".format(code))
                        print("len of unsearch_doid_list = {:d}".format(len(unsearch_doid_list)))

                    # write val to the given cols ---> col_names = 'doid,label'
                    f.write(",".join([code,label]))
                    f.write("\n")

    return all_label2leaf_dict, all_leaf2label_dict

def run_cui_label_mapping():
    doid_label_dict = {'3393': 'coronary artery disease',
                       '2841': 'Asthma',
                       '9351': 'diabetes mellitus',
                       '0060224': 'atrial fibrillation',
                       '6000': 'congestive heart failure',
                       '10763': 'hypertension',
                       '1168': 'familial hyperlipidemia',
                       '1596': 'mental depression',
                       '6713': 'cerebrovascular disease'}

    copd_children = {'9675': 'pulmonary emphysema',
                     '10030': 'interstitial emphysema',
                     '10031': 'hyperlucent lung',
                     '10032': 'com pensatory emphysema'}

    added_doid = {'8534': 'gastroesophageal reflux disease',
                  '8398': 'Osteoarthritis'}

    save_path = 'dataset/disease_mappings_umls/copd_comorbidities_label.txt'

    col_names = 'doid,label'

    #################33
    ## use doid api to extract list of children_doid from url. (url is constructed in json format)
    ##################
    t0 = time.time()
    all_label2leaf_dict, all_leaf2label_dict = get_children_url(col_names, doid_label_dict, save_path, verbose=False)
    t1 = time.time()
    total = t1 - t0
    print("total time to run {:s} = {:f} second".format(str(get_children_url.__name__), total), end="\n")

    ################
    ## creating {doid : [list_cui]}, {cui: doid}
    ###############
    gene_disease_uniq_DO_mapping_file_path = 'dataset/disease_mappings_umls/gene_disease_uniq_DO_mapping.txt'

    t0 = time.time()
    cui2doid_dict, doid2cui_dict = create_cui2doid_dict(
        gene_disease_uniq_DO_mapping_file_path=gene_disease_uniq_DO_mapping_file_path)
    t1 = time.time()
    total = t1 - t0
    print("total time to run {:s} = {:f} second".format(str(get_children_url.__name__), total), end="\n")

    ##################
    ## create {label: [cui]}
    ###############
    save_path = 'dataset/disease_mappings_umls/copd_uniq_cuis_label_mapping.txt'

    t0 = time.time()
    label2cui_dict = create_label2cui_dict(all_label2leaf_dict, doid2cui_dict=doid2cui_dict, save_path=save_path)
    t1 = time.time()
    total = t1 - t0
    print("total time to run {:s} = {:f} second".format(str(get_children_url.__name__), total), end="\n")

    print(label2cui_dict)


if __name__ == "__main__":
    run_cui_label_mapping()

