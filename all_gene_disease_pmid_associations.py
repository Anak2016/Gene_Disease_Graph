from PubAnnotator import *
import re
import time
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

    def writeToFile(self,file_name, dictionary):
        with open(file_name,"w") as f:
            # f.write(str(copd_dict))
            for i, key in enumerate(dictionary.keys()):
                val_list = ""
                val_list = val_list + " " + key # write the col's name
                #write the col's val
                for vals in dictionary[key]:
                    val_list = val_list + "," + vals
                val_list = val_list + "\n"
                f.write(val_list)

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
    def GetDictVal(self, gene_disease_Dict, cols, iteration):
        #if value contain number; that value belong to diseaseClass
        #the value before diseaseClass = diseaseType
        #the value before diseaseType to the first value is diseaseName

        # geneId, geneSymbol, diseaseId, diseaseName, diseaseClass, pubmid, source
        # keys_list = ["diseaseName", "diseaseType", "diseaseClass", "pmid", "source"]
        keys_list = ["diseaseName", "diseaseClass", "pmid", "source"]

        prev_dict = gene_disease_Dict
        prev_len_list = [ len(gene_disease_Dict[key]) for key in keys_list]

        for i, val in enumerate(cols):
            x = re.findall("([A-Z][0-9][0-9])", val)
            if x:
                gene_disease_Dict["diseaseClass"].append(cols[i])
                gene_disease_Dict["diseaseType"].append(cols[i-1])

                if len(cols[:i-1]) > 0:
                    # merge mulitple element into 1 element
                    sent = ""
                    for word in cols[:i-1]:
                        if sent:
                            sent += " " + word
                        else:
                            sent = word
                    gene_disease_Dict["diseaseName"].append(sent)

                offset = i+1
                addYear = True #garantee to add 1 time start from YearInitial
                addScore = True

                #Error is below here
                for j, element in enumerate(cols[offset:]): # I see this is weird!!!!!!
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
                del gene_disease_Dict[key][-1] #

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



        # print(gene_disease_Dict) # if this if not work
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

    def Validate_len_equal(self, dict):
        #diseaseName is not checked #HERE
        keys_list = [key for key in dict.keys()]
        keys_list.append(keys_list[0])

        for key in keys_list[:-1]:
            print(key,len(dict[key]))
        exit()
        for left, right in zip(keys_list[1:], keys_list[:-1]):
            assert len(dict[left]) == len(dict[right]), "length of {:s} is {:d} != length of {:s} is {:d}".format(
                left, len(dict[left]), right, len(dict[right]))
        print('value of all keys are equal ')

    def CreateUniq(self, dict, uniq):

        temp_uniq = {}
        for i,vals in enumerate(dict.values()):
            # print(len(vals)) # 9
            try:
                # print(uniq[i])
                temp_uniq[uniq[i]] = set(vals)
            except:
                print("number of cols mismatch")
        for key in temp_uniq.keys():
            print("len(temp_uniq[{:s}]): ".format(key) , len(temp_uniq[key]))

        # self.Validate_len_equal(dict)
        print("value of al uniq_keys are equal")
        # dict.update(temp_uniq)
        return temp_uniq

    def run(self):
        # self.readFile('gene_disease_data.txt')
        # exit()
        gene_disease_Dict = self.gene_disease_dict

        data = self.readRawData("./dataset/disease_gene/disease_gene.tsv")

        gene_disease_association = gene_disease_pmid(gene_disease_Dict)


        start = time.time()
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
                gene_disease_Dict["geneId"].append(columns[0])
                gene_disease_Dict["geneSymbol"].append(columns[1])
                gene_disease_Dict["DSI"].append(columns[2])
                gene_disease_Dict["DPI"].append(columns[3])
                gene_disease_Dict["diseaseId"].append(columns[4])

                iteration = i
                gene_disease_association.GetDictVal(gene_disease_Dict, columns[5:], iteration)

                # self.Pause(i, 5, [gene_disease_Dict["geneId"]] )
                # self.Pause(i, 5, [gene_disease_Dict] )
                # if i == 5:
                #     break

        selected_keys_list = ["geneId", "geneSymbol", "diseaseId", "diseaseName", "diseaseClass", "pmid", "source"]
        selected_dict = {key: gene_disease_Dict[key] for key in selected_keys_list}
        gene_disease_Dict = selected_dict

        gene_disease_1000 = {key: val[:1000] for key, val in gene_disease_Dict.items()}
        self.Validate_len_equal(gene_disease_1000)

        self.Validate_len_equal(gene_disease_Dict)
        gene_disease_uniq  =  self.CreateUniq(selected_dict, selected_keys_list)

        # self.writeToFile("all_gene_disease_pmid_data.txt", gene_disease_Dict) # too long
        end = time.time()
        total = end-start


        self.writeToFile("gene_disease_1000.txt",gene_disease_1000)
        exit()
        self.writeToFile("gene_disease_uniq.txt",gene_disease_uniq)
        exit()
        return gene_disease_Dict,gene_disease_uniq, total

if __name__ == '__main__':

    gene_disease_Dict = {}
    gene_disease_association = gene_disease_pmid(gene_disease_Dict)

    # start = time.time()
    gene_disease_data= gene_disease_association.run()

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


