#!/usr/bin/env python
#-*-coding:utf8-*-
import sys,requests

prot_list = sys.argv[1]
taxonomy = sys.argv[2]

KO2Gene = '/home/ztt/Annotation/KO2Gene'
Uniprot2KO = '/home/ztt/Annotation/Uniprot2KO_all'
Uniprot2KEGG = '/home/ztt/Annotation/Uniprot2KEGG_all'

def keggAnnotation(prot_list,taxonomy):
    dict_ko = {}
    dict_kegg = {}
    dict_path = {}
    path_name_list = []
    path_description_list = []
    dict_ko_gene = {}
    # Download the taxonomy whole pathway
    with open('%s_path.txt' % taxonomy,'w') as f:
        response = requests.get('http://rest.kegg.jp/link/pathway/%s'% taxonomy)
        f.write(response.text)

    with open('%s_path.txt' % taxonomy, 'rb') as f:
        for line in f:
            line = line.strip().split('\t')
            path = line[0]
            pathway = line[1].split(':')[1]
            dict_path.setdefault(path,[]).append(pathway)

    # Get the pathway name to pathway description
    response = requests.get('http://rest.kegg.jp/list/pathway/%s' % taxonomy)
    result = response.content.replace('\n', '\t').strip().split('\t')
    for line in result:
        if 'path:' in line:
            path_name_list.append(line.split(':')[1])
        else:
            path_description_list.append(line)
    dict_path_description = dict(zip(path_name_list, path_description_list))

    with open(Uniprot2KO, 'rb') as ko:
        for line in ko:
            line = line.strip()
            prot = line.split('\t')[0]
            ko = line.split('\t')[1]
            dict_ko[prot] = ko

    with open(Uniprot2KEGG, 'rb') as f:
        for line in f:
            line = line.strip()
            prot = line.split('\t')[0]
            kegg = line.split('\t')[1]
            dict_kegg[prot] = kegg

    with open(KO2Gene, 'rb') as f:
        for line in f:
            line = line.strip()
            if 'ko:' in line:
                ko_id = line.split('\t')[0]
                ko_id = ko_id.split(':')[1]
                gene = line.split('\t')[1]
                dict_ko_gene[ko_id] = gene

    with open('KEGG_pathway_annotation.xls','w') as f:
        f.write('Protein accession'+'\t'+'KEGG KO No.'+'\t'+'KEGG Gene'+'\t'+'KEGG pathway'+'\n')
        with open(prot_list, 'rb') as list:
            header = list.readline()
            for line in list:
                prot = line.strip().split('\t')[0]
                if prot in dict_ko:
                    ko = dict_ko[prot]
                    f.write(prot+'\t'+ko+'\t')
                    if dict_ko_gene[ko]:
                        f.write(dict_ko_gene[ko]+'\t')
                    else:
                        continue
                    if dict_kegg[prot] in dict_path:
                        for path in dict_path[dict_kegg[prot]]:
                            f.write(path+' '+dict_path_description[path]+'; ')
                    f.write('\n')
                else:
                    f.write(prot+'\n')

keggAnnotation(prot_list,taxonomy)







# Download KEGG KO id and gene information
# with open('KO2Gene.txt','w') as f:
#     ko_database_information = requests.get('http://rest.kegg.jp/info/ko')
#     f.write(ko_database_information.text)
#     response = requests.get('http://rest.kegg.jp/list/orthology/')
#     f.write(response.text)


