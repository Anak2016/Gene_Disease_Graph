import re

class PubAnotator:

    #copd_dict
    def __init__(self, copd_dict):
        self.copd_dict = copd_dict

    def readRawData(self,fileDir):
        with open(fileDir, "r", encoding= "utf8")as f:
            data = f.readlines()
        return data


    #print val_list to cmd
    def printFileToScreen(self,file_name):
        with open(file_name,"r") as f:
            for val_list in f.readlines():
                print(val_list)
    # printFile("uniq.txt")
    # exit()

    def readFile(self,file_name):
        self.copd_dict = {}
        with open(file_name,"r") as f:
            for val_list in f.readlines():
                # print(val_list)
                val_list = val_list.split(",")
                key = val_list[0]
                val = val_list[1:]
                copd_dict[key] = val
        return self.copd_dict

    # readFile("uniq.txt")



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

    # writeToFile("uniq.txt")

    # if x is a number return Ture, otherwise return False
    def IsNumber(self,x):
        try:
            x = int(x)
            return True
        except:
            return False

    def GetSent(self,columns, col_number):
        length = 0
        # if columns[col_number] == "Design":
        for col in columns[col_number:]: #count the first words to the last words
            if not self.IsNumber(col):
                length += 1
            else:
                break
        # print(columns)

        words_list = columns[col_number:length + 1]
        sent = self.ConcatWords(words_list) # HERE
        # print(sent)
        # exit()
        if length <= 0:
            shift = 0
        else:
            shift = length -1
        return sent, shift

    def AddToDict(self,copd_dict,sent_nospace, columns):
    # def AddToDict(self,sent_nospace, columns):
        x = re.findall("^.*copd", sent_nospace.lower())
        if x:
            # pmid, section, sentence_number, geneId, geneoffset, diseaseId, deseaseoffsets,sentence
            # copd_list.append(columns)
            # self.copd_dict['section'].append(columns[1])
            # self.copd_dict['sentence_number'].append(columns[2])

            self.copd_dict['pmid'].append(columns[0])
            self.copd_dict['geneId'].append(columns[3])
            self.copd_dict['diseaseId'].append(columns[5])


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

    # testing if columns[#] == val
    def Debugging(self, columns,col_number, val):
        # return true if yes, otherwise no
        if columns[col_number] == val:
            print(columns)
            return True
        return False

    def Validate_len_equal(self):
        keys_list = [key for key in self.copd_dict.keys()]
        keys_list.append(keys_list[0])

        for left, right in zip(keys_list[1:], keys_list[:-1]):
            assert len(self.copd_dict[left]) == len(self.copd_dict[right]), "length of {:s} != length of {:s}".format(
                left, right)
        print('value of all keys are equal ')

    def UpdateUniq(self, copd_dict, uniq):

        temp_uniq = {}
        for i,vals in enumerate(copd_dict.values()):
            # print(len(vals)) # 9
            try:
                # print(uniq[i])
                temp_uniq[uniq[i]] = set(vals)
            except:
                print("number of cols mismatch")

        self.Validate_len_equal()

        self.copd_dict.update(temp_uniq)

    def run(self):
        # copd_list = []
        #
        # pubAnotator = PubAnotator(copd_list)
        # copd_dict = self.copd_dict


        data = pubAnotator.readRawData("./dataset/Pubannotator/pubannotator.tsv")

        # geneId# diseaseId# section #sentence_number
        # self.copd_dict = {"geneId": [], "diseaseId": [], "section": [], "sentence_number": []}
        self.copd_dict = {"pmid":[], "geneId": [], "diseaseId": []}


        counter = 0
        counter1 = 0
        # extract geneId, diseaseId, section, and sentence_number columns into list
        for i, sentence in enumerate(data):

            # pmid, section, sentence_number, geneId, geneoffset, diseaseId, deseaseoffsets,sentence
            columns = sentence.split()
            col_sent_val = ""
            sent_nospace = ""

            sent, shift = pubAnotator.GetSent(columns, 1)  # col = Section
            # sent, length = GetSent(["Design","me"], 0) #col = Section
            if sent:
                columns[1] = sent

                # adjust cols so that index corresponds to the right value
                if i != 0 and shift != 0:
                    for j in range(2, len(columns) - shift):
                        new_cols = columns[j + shift]
                        columns[j] = new_cols

                    # Pause(counter1, 3, [columns])
                    counter1 += 1
                    # exit()

            # self.Pause(i, 5, [self.copd_dict] )
            # Debugging(columns, 1, "Design")

            for word in columns[7:]:
                # print(word)
                col_sent_val = col_sent_val + " " + word
                sent_nospace = sent_nospace + word

            pubAnotator.AddToDict(self.copd_dict,sent_nospace,columns)
            # pubAnotator.AddToDict(sent_nospace,columns)
            # print(self.copd_dict)

        # pubAnotator.Validate_len_equal()
        # exit()
        pubAnotator.writeToFile("PubAnnotator_instances.txt", self.copd_dict)
        exit()
        # uniq = ['uniq_geneId', 'uniq_disease', 'uniq_section', "uniq_sentence_number"]
        uniq = ['uniq_pmid', 'uniq_geneId', 'uniq_disease']

        pubAnotator.UpdateUniq(self.copd_dict, uniq)

        # print(self.copd_dict)


if __name__ == "__main__":

    # copd_list = []
    # pubAnotator = PubAnotator(copd_list)

    copd_dict = {"geneId": [], "diseaseId": [], "section": [], "sentence_number": []}
    pubAnotator = PubAnotator(copd_dict)

    data = pubAnotator.readRawData("./dataset/Pubannotator/pubannotator.tsv")

    pubAnotator.run()
