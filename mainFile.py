from all_gene_disease_pmid_associations import gene_disease_pmid as gene_disease_pmid

def readFile(file_name):
    dictionary = {}
    with open(file_name, "r") as f:
        for val_list in f.readlines():
            # print(val_list)
            val_list = val_list.split(",")
            key = val_list[0]
            val = val_list[1:]
            dictionary[key] = val
    return dictionary

#read uniq.txt, and gene_disease_data.txt files
def display(dict):
    for key, val in dict.items():
        print("key: ", key)
        print("         val:", val)

if __name__ == "__main__":
    # pub_annotator_data = readFile('PubAnnotator_uniq.txt')
    # display(pub_annotator_data)

    gene_disease_dict = {}
    gene_disease_association = gene_disease_pmid(gene_disease_dict)
    gene_disease_data, rt_total =  gene_disease_association.run()
    # gene_disease_data = gene_disease_association.run()
    exit()
    #it is too large so I need to directly gene_disease_pmid.run
    # gene_disease_data = readFile('gene_disease_data.txt')
