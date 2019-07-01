from PubAnnotator import *
import re
import time
import pandas as pd
# printFile("uniq.txt")

class gene_disease_pmid:

    def __init__(self, gene_disease_dict):
        self.gene_disease_dict = gene_disease_dict

    def readRawData(self,fileDir):
        with open(fileDir, "r", encoding= "utf8")as f:
            data = f.readlines()
        return data

    def printFileToScreen(self,file_name):
        with open(file_name,"r") as f:
            for val_list in f.readlines():
                print(val_list)

    def get_CUI_lable_mapping(self, file_path):
        '''
        create dictionary containing {label: [list of CUIs]}
        from uniq_CUIs_label_mappings.txt

        :param file_path: file containing the following format

                diseaseId,class
                cui1,doid
                cui2,doid
                ..., ...

                such as disease_mappings_umls/uniq_CUIs_label_mappings.txt
        :return: dict:{label: [list of CUIs]}
        '''
        uniq_cui_label_dict = {}
        with open(file_path, 'r') as f:
            data = f.readlines()
            for line in data:
                cui = line.split(',')[0]
                label =line.split(',')[1]

                if label in uniq_cui_label_dict.keys():
                    uniq_cui_label_dict[label].append(cui)
                else:
                    uniq_cui_label_dict[label] = [cui]

        return uniq_cui_label_dict

    def appendClassToFile(self, save_path, uniq_cui_label_dict, dictionary):
        '''
        use gene_disease_uniq_DO_mapping.txt to map uniq_cui_label_dict to labels presented in the txt file.

        :param save_path:
        :param uniq_cui_label_dict:
        :param dictionary:
        :return:
        '''
        all_DO_list = [val for val_list in uniq_cui_label_dict.values() for val in val_list]
        cui2label_dict = {val: key for key, val_list in uniq_cui_label_dict.items() for val in val_list}
        # add class here
        label_list = []
        with open(save_path, "w") as f:
            df = pd.DataFrame.from_dict(dictionary)
            key = None
            for i, col in enumerate(df.columns):
                if col == 'diseaseId':
                    key = i
            for row in range(df.shape[0]):
                cui = df.iloc[row, key]
                try:
                    label_list.append(cui2label_dict[cui].strip('\n'))
                except:
                    label_list.append("None")

            df['class'] = label_list
            df = df.loc[df['diseaseId'].isin(all_DO_list)]
            csv = df.to_csv(index=False)
            f.write(csv)

    def writeToFile(self,save_path, dictionary, unique = False, **kwargs):
        '''
        (argument name is strange so please ignore and read param description)
        write row of values of selected columns that
        have mapping to gene_disease_uniq_DO_mapping.txt

        :param file_name: location to save file
        :param dictionary: any dict
        :param selected_dict:
            dict whose dict[key][i] correspond to the same instance where key is any keys in dict
            therefore, selected_dict must have the same len for all val.
        :return:
        '''

        #if uniq_cuis_label_mapping are specifiied
        if list(kwargs.keys())[0] == 'uniq_cuis_label_mapping_file_path':
            uniq_cuis_label_mapping_file_path = list(kwargs.values())[0]
        else:
            uniq_cuis_label_mapping_file_path = 'dataset/disease_mappings_umls/uniq_CUIs_label_mapping.txt'
        # print(uniq_cuis_label_mapping_file_path)
        # exit()
        uniq_cui_label_dict = self.get_CUI_lable_mapping(uniq_cuis_label_mapping_file_path)

        #fix all_do_lsit and all_label_list
        all_DO_list = [val for val_list in uniq_cui_label_dict.values() for val in val_list]

        all_label_list = [val for val in uniq_cui_label_dict.keys()]
        print("len of all_DO_list =",len(all_DO_list))
        print("len of all_label_list = ", len(all_label_list))

        if unique:
            with open(save_path,'w') as f:
                for key, val_list in dictionary.items():
                    sent = ','.join([key]+val_list)
                    f.write(sent)
                    f.write('\n')
        else:
            self.appendClassToFile(save_path,uniq_cui_label_dict, dictionary)


    def readFile(self,file_name):
        dictionary = {}
        with open(file_name,"r") as f:
            for val_list in f.readlines():
                # print(val_list)
                val_list = val_list.split(",")
                key = val_list[0]
                val = val_list[1:]
                dictionary[key] = val
        return dictionary

    def ContainNumber(self, x):
        ans = re.findall('[0-9]', x)
        if ans:
            return True
        else:
            return False


    # with open("./dataset/disease_gene/disease_gene.tsv", "r")as f:
    #     data = f.readlines()
    def GetDictVal_OLD(self, gene_disease_Dict, cols, iteration):
        #if value contain number; that value belong to diseaseClass
        #the value before diseaseClass = diseaseType
        #the value before diseaseType to the first value is diseaseName

        # geneId, geneSymbol, diseaseId, diseaseName, diseaseClass, pubmid, source
        # keys_list = ["diseaseName", "diseaseType", "diseaseClass", "pmid", "source"]
        keys_list = ["diseaseName", "diseaseClass", "pmid", "source"]

        prev_dict = gene_disease_Dict
        prev_len_list = [ len(gene_disease_Dict[key]) for key in keys_list]

        for i, val in enumerate(cols):
            x = re.findall("([C|F][0-9][0-9])", val)

            # check if diseaseClass have value
            # if yes, follow, use the same code
            # if no, create a new code that doesn ot rely on diseaseClass

            #only have case that diseaseClass exist (x = True)
            #but I already check that there is no case where x=False
            if x :

                # disease Type = phenotype,
                # diseaseName = Down Syndrome | diseaseType = disease

                # some of them does not have disease class. # FIX HERE
                gene_disease_Dict["diseaseClass"].append(cols[i])

                if re.findall("(C[0-9][0-9][0-9])", val):
                    print(iteration)
                    print(cols)
                    exit()

                gene_disease_Dict["diseaseType"].append(cols[i-1]) # we assume that this exist

                #### FIX HERE
                if len(cols[:i-1]) > 0:
                    # merge mulitple element into 1 element
                    sent = ""
                    for word in cols[:i-1]:
                        if sent:
                            sent += " " + word
                        else:
                            sent = word
                    # print(cols[:i-1])
                    if 'IL21R' in cols[:i-1]:
                        print(i)
                        # print(cols[i]) # expecting deseaseClass: get IL21R
                        print(cols)
                        print(iteration)
                        print(sent) #IL21R IMMUNODEFICIENCY disease Disease or Syndrome 0.70 2013 2013
                        exit()
                    gene_disease_Dict["diseaseName"].append(sent)

                offset = i+1
                addYear = True #garantee to add 1 time start from YearInitial
                addScore = True

                # print(iteration)
                # if iteration == 5:
                #     print(cols[offset:])
                #     print(gene_disease_Dict)
                #     exit()
                for j, element in enumerate(cols[offset:]):
                    # 1. get score
                    # 3. if val of ei (come after score) is not a year 20[0-9][0-9]
                    #     >if val is not a year, collect it as ei val,
                    #     >Otherwise, dont append anything to EI
                    # 2. get yearInitial, and cols that come after it

                    a = re.findall("[.]", element) #make sure it runs one time
                    # b = re.fullmatch("[0-9]", element)
                    c = re.fullmatch("(20[0-9][0-9]|19[0-9][0-9])", element)
                    if a and addScore:
                        addScore = False
                        gene_disease_Dict["score"].append(cols[offset + j])

                        if self.ContainNumber(cols[offset+j+1]):
                            gene_disease_Dict["EI"].append(cols[offset+j+1])

                        #diseaseSematicType sometimes append score in it. Why?
                        if len(cols[offset:offset + j]) > 0:
                            #merge mulitple element into 1 element
                            sent = ""
                            for word in cols[offset:offset + j]:
                                if sent:
                                    sent += " " + word
                                else:
                                    sent =  word

                            gene_disease_Dict["diseaseSemanticType"].append(sent)
                    # elif b:
                    #         gene_disease_Dict["EI"].append(cols[offset + j])
                    elif addYear:
                        if c:

                            gene_disease_Dict["YearInitial"].append(cols[offset+j])#12
                            gene_disease_Dict["YearFinal"].append(cols[offset+j+1])#13
                            #if cols[offset + j + 2] is not a number then
                            gene_disease_Dict["pmid"].append(cols[offset + j + 2]) #14 #index out of range

                            if len(cols[offset + j + 3:]) > 0:
                                #merge multiple element into 1 elemnt
                                sent = ""
                                for word in cols[offset + j + 3:]:
                                    if sent:
                                        sent += " " + word
                                    else:
                                        sent = word
                                gene_disease_Dict["source"].append(sent)

                            addYear = False
                    else:
                        #if there is no diseaseClass present
                        pass
                break

        current_len_list = [len(gene_disease_Dict[key]) for key in keys_list]

        # keys_list = ["geneId", "geneSymbol", "diseaseId", "diseaseName", "diseaseClass", "pubmid", "source"]
        # keys_list = ["diseaseName", "diseaseClass", "pmid", "source"]


        # print("prev_dict")
        # for name in keys_list:
        #     print("    ",name, prev_dict[name])
        #
        # print("current_dict")
        # for name in keys_list:
        #     print("    ",name, gene_disease_Dict[name])

        # if iteration == 1203339:
        #     print('lol')

        rollback = False #delete last element of ["geneId", "geneSymbol", "DSI", "DPI", "diseaseId"]

        # keys_list = ["diseaseName", "diseaseClass", "pmid", "source"]
        ignore = [True,True,True,True]
        for i, (current, prev) in enumerate(zip(current_len_list, prev_len_list)):
            if current == prev:
                rollback = True
                ignore[i] = False

        if rollback:
            #reset the geneId, geneSymbol, DSI, DPI, diseaseId (from
            keys14 = ["geneId", "geneSymbol", "DSI", "DPI", "diseaseId"]

            for i,key in enumerate(keys14):
                try:
                    del gene_disease_Dict[key][-1] # what does it do?
                except:
                    pass

            # roll element that ignore = True
            for i in range(len(ignore)):
                current_len_list[i] -= 1
                key = keys_list[i]#get key
                if ignore[i]:
                    del gene_disease_Dict[key][-1]

            #update current_len_list to have due to rollback
            current_len_list = [len(gene_disease_Dict[key]) for i,key in enumerate(keys_list)]
            #set
            for i, (current, prev) in enumerate(zip(current_len_list, prev_len_list)):
                # print("rollback = True")
                assert  current == prev , "iteration = {:d}, key = {:s} is not updated; current is {:d} != prev is {:d}".format(
                    iteration,keys_list[i], current, prev )
        else:
            for i, (current, prev) in enumerate(zip(current_len_list, prev_len_list)):
                # print("rollback = False")
                assert  current == prev+1, "iteration = {:d}, key = {:s} is not updated; current is {:d} != prev is {:d}".format(
                    iteration,keys_list[i], current, prev+1)



        # print(len(gene_disease_Dict['diseaseId']))
        # print(gene_disease_Dict['diseaseId'])
        # print("done")
        # exit()

    def ConcatWords(self,word_list):
        sent = ""
        for word in word_list:
            if sent:
                sent = sent + " " +word
            else:
                sent = word
        return sent

    def Pause(self, ind, val, toPrint = []):

        if ind == val:
            for x in toPrint:
                print(x)
            exit()

    def Debugging(self, columns,col_number, val):
        # return true if yes, otherwise no
        if columns[col_number] == val:
            print(columns)
            return True
        return False

    # option to display chosen list of columns
    # option to display top first n-th element of selected columns
    def displayColsVal(self, gene_disease_Dict ,i , cols_list = []):
        if cols_list:
            for col in cols_list:
                val_list = gene_disease_Dict[col][:i]
                print(val_list)
            exit()
        else:
            print("displayColsVal: no cols_list arg provided")
            exit()

    def Validate_len_equal(self, dict): #for some reason, len of diseaseSymbol is more than 1000
        #diseaseName is not checked #HERE
        keys_list = [key for key in dict.keys()]
        keys_list.append(keys_list[0])

        for key in keys_list[:-1]:
            print(key,len(dict[key]))
        for left, right in zip(keys_list[1:], keys_list[:-1]):
            assert len(dict[left]) == len(dict[right]), "length of {:s} is {:d} != length of {:s} is {:d}".format(
                left, len(dict[left]), right, len(dict[right]))
        print('len of value of all keys are equal ')

    def CreateUniq(self, dict, uniq):
        '''
        get uniq value of each dict[key] and create dict as followed
            {key: [list of uniq_value of dict[key]}
        :param dict: any dict
        :param uniq: selected keys that will be used to find uniq node
        :return: temp_uniq: {key: [list of uniq_value of dict[key]}
        '''
        temp_uniq = {}
        for i,vals in enumerate(dict.values()):
            # print(len(vals)) # 9
            try:
                # print(uniq[i])
                temp_uniq[uniq[i]] = list(set(vals))
            except:
                print("number of cols mismatch")
        for key in temp_uniq.keys():
            print("len(temp_uniq[{:s}]): ".format(key) , len(temp_uniq[key]))

        self.Validate_len_equal(dict)
        # self.Validate_len_equal(temp_uniq) #uniq value of each col will not be equal
        print("value of all uniq_keys are equal")

        # exit()
        # dict.update(temp_uniq)
        return temp_uniq

    def GetDictVal_NEW(self, gene_disease_Dict, cols, iteration):
        print(gene_disease_Dict)
        print(cols)
        print(iteration)
        exit()



    def run(self):

        # self.readFile('gene_disease_data.txt')
        # exit()
        gene_disease_Dict = self.gene_disease_dict
        data = self.readRawData("./dataset/disease_gene/disease_gene.tsv")
        gene_disease_association = gene_disease_pmid(gene_disease_Dict) # why would I call a class within a class like this?? forgot to change.


        start = time.time()
        # print(data[1325693])
        # exit()
        for i, sentence in enumerate(data):
            columns = sentence.split()
            if i == 0:
                for val in columns:
                    gene_disease_Dict[val] = []
                '''
                    ['geneId', 'geneSymbol', 'DSI', 'DPI', 'diseaseId', 'diseaseName', 'diseaseType', 'diseaseClass',
                     'diseaseSemanticType', 'score', 'EI', 'YearInitial', 'YearFinal', 'pmid', 'source']
                '''

            if i != 0:

                # if columns[4] in ['Simplex', 'B-Cell','Cell', 'Joint', 'Dystrophies','MYELODYSPLASTIC' ]:
                #     print("iteration:", i)
                #     print(columns)
                #     print(columns[4])
                #     exit()

                for j,val in enumerate(columns[2:5]):

                    x = re.fullmatch("([A-Z][0-9]+)", val)
                    if x:
                        diseaseId_index = j + 2
                        # print(iteration ,j, val)
                        gene_disease_Dict["geneId"].append(columns[0])
                        gene_disease_Dict["geneSymbol"].append(columns[1])
                        gene_disease_Dict["diseaseId"].append(columns[diseaseId_index])
                        #neew function
                        # gene_disease_association.GetDictVal_NEW(gene_disease_Dict, columns[diseaseId_index+1:], i)

                        # if i == 1325693:
                        #     print(columns)
                        #     print(val)
                        #     print(diseaseId_index+1)
                        #     exit()

                        # old function
                        gene_disease_association.GetDictVal_OLD(gene_disease_Dict, columns[diseaseId_index+1:], i)

                #incase there is no value in diseaseId
                # gene_disease_association.GetDictVal(gene_disease_Dict, columns[2:], i)

                # gene_disease_Dict["DSI"].append(columns[2])
                # gene_disease_Dict["DPI"].append(columns[3])


                # self.Pause(i, 5, [gene_disease_Dict["geneId"]] )
                # self.Pause(i, 5, [gene_disease_Dict] )
                # if i == 5:
                #     break

        selected_keys_list = ["geneId", "geneSymbol", "diseaseId", "diseaseName", "diseaseClass", "pmid", "source"]
        # selected_keys_list = ["diseaseName", "diseaseClass", "pmid", "source"]

        # replace ',' in val of diseaseClass with '-' in gene_disease_Dict
        for key in selected_keys_list:
            if key == 'diseaseName':
                for i,val in enumerate(gene_disease_Dict[key]):
                    if ',' in val:
                        res = val.replace(',','-')
                        gene_disease_Dict[key][i] = res

        selected_dict = {key: gene_disease_Dict[key] for key in selected_keys_list}
        # x = [ len(set(val)) for val in selected_dict.values()]
        # print(x)
        # print(len(set(selected_dict['diseaseId'])))
        # print(len(selected_dict['diseaseId']))
        # exit()

        gene_disease_Dict = selected_dict

        gene_disease_1000 = {key: val[:1000] for key, val in gene_disease_Dict.items()}
        gene_disease_50000 = {key: val[:50000] for key, val in gene_disease_Dict.items()}

        self.Validate_len_equal(gene_disease_1000)
        for key,val in gene_disease_1000.items():
            print(key,len(val))

        # self.Validate_len_equal(gene_disease_Dict)
        # exit()

        gene_disease_uniq  =  self.CreateUniq(selected_dict, selected_keys_list)

        # ###################3
        # ## CREATE DATASET
        # ###################3

        # ## create dataset containing all of data from disease_gene.tsv
        # self.writeToFile("all_gene_disease_pmid_data.txt", gene_disease_Dict) # too long
        end = time.time()
        total = end-start

        # HERE>> write to test file to inspect result
        t0 = time.time()

        ##currently doesnot exist, it must be generated first from copd_terminology_extract.py
        uniq_cuis_label_mapping_file_path = 'dataset/disease_mappings_umls/copd_uniq_cuis_label_mapping.txt'
        self.writeToFile("dataset/generated_dataset/copd_label.txt",gene_disease_Dict, uniq_cuis_label_mapping_file_path = uniq_cuis_label_mapping_file_path)
        t1 = time.time()
        total = t1 - t0
        print(f"writing to dataset/generated_dataset/copd_label.txt takes {total}")
        exit()
        ## create dataset contianing the first 1000 data from disease_gene.tsv
        # self.writeToFile("dataset/generated_dataset/gene_disease_50000_no_None.txt",gene_disease_50000)
        # self.writeToFile("dataset/generated_dataset/gene_disease_1000_no_None.txt",gene_disease_1000)

        # exit()
        ## create dataset containing uniq value from each selected column's key
        # self.writeToFile("dataset/generated_dataset/gene_disease_uniq.txt",gene_disease_uniq, unique=True)
        exit()
        return gene_disease_Dict, total

if __name__ == '__main__':

    gene_disease_Dict = {}
    gene_disease_association = gene_disease_pmid(gene_disease_Dict)

    # start = time.time()
    gene_disease_data, totoal_time = gene_disease_association.run()

    # end = time.time()
    # total = end - start
    # print("time = ", total) # 2.799

    # length = len(gene_disease_Dict["geneId"])
    # print(length) # 1548061
    # exit()

    # start = time.time()
    # # writing to file using pythonIO takes too long; use pickle instead
    # gene_disease_association.writeToFile("gene_disease_data.txt", gene_disease_Dict)
    # end = time.time()
    # total = start - end
    # print("total writing to File time = ", total)


