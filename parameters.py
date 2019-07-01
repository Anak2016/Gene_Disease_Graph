# report = True
report = False

plot   = True
# plot   = False

# keys_list = [ "geneId", "geneSymbol", "diseaseId" , "diseaseName", "diseaseClass", "pmid", "source"]
# keys_name = [ "geneId", "geneSymbol", "diseaseId" , "diseaseName", "diseaseClass", "pmid", "source"]
# keys_name = [ "geneSymbol", "diseaseName", "diseaseClass"]
# keys_name = [ "geneId","ran domassword ","pmid", "diseaseId"]
keys_name = [ "geneId","diseaseId"]
# keys_name = ['geneId','geneSymbol','diseaseId','diseaseName','diseaseClass','pmid','source','class']

# selected_keys = ["geneId", "pmid"]
# selected_keys = ["geneId", "diseaseId"]

selected_keys = None

num_val = 5000
# num_val = None


# community_detection = True
community_detection = False

# bipartite = True  #subplot
bipartite = False

#####3
# option is available when bipartite is True
######
subplot = True
# subplot = False

#file format:
vertical = True
# vertical = False #horizontal

###############33
## specified file in dataset/demo dataset/ folder to be run
###############33
# file_name = 'dataset/demo_dataset/gene_disease_1000_label_no_None.txt'
# file_name = 'dataset/demo_dataset/gene_disease_50000_label_no_None.txt'
file_name = 'dataset/generated_dataset/copd_label.txt'
# file_name = 'dataset/demo_dataset/PubAnnotator_instances.txt' #horizontal format
# file_name = 'dataset/demo_dataset/gene_disease_testing.txt' #horizontal format

# original dataset
# file_name = 'dataset/generated_dataset/gene_disease_uniq.txt'
# file_name = 'dataset/generated_dataset/PubAnnotator_uniq.txt'


###################
## specify type of uniq_cuis_label_mapping to be used
###################
uniq_cuis_label_mapping_file_path = 'dataset/disease_mappings_umls/copd_uniq_cuis_label_mapping.txt'