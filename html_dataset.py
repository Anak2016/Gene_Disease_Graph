'''
This file generated data for html page
such as
1. bipartite gene-disease graph
2. Degree distribution of COPD Bipartite Graph
3. list of node degree and number of node frequency
4.
'''
data_path = 'dataset/demo_dataset/copd_label.txt'

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


def write_to_csv(dict, path):
    df = pd.DataFrame(dict)
    cols = ['diseaseId', 'class']
    uniq_df = df[cols].drop_duplicates()
    uniq_df.to_csv(path, index=False)

def main():
    col_list = ['geneId', 'geneSymbol', 'diseaseId', 'diseaseName', 'diseaseClass', 'pmid', 'source', 'class']
    dictionary = {key: [] for i, key in enumerate(col_list)}  # add name to the key currently i is used as key name
    file_name = 'dataset/generated_dataset/TESTING'
    with open(file_name) as f:
        for i, line in enumerate(f):
            if i == 0:
                val_list = line.split(",")
                val_list = [val.strip().lower() for val in val_list]
            else:
                val_list = line.split(',')
                for i, val in enumerate(val_list):
                    val = val.strip()
                    dictionary[list(dictionary.keys())[i]].append(val)

    path = r"C:\Users\Anak\Desktop\NSF project\html dataset website\csv\disease_and_labels.txt"

    # write to csv
    write_to_csv(dictionary, path)

if __name__ == "__main__":
    main()

