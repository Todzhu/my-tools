#!/usr/bin/env python
#-*-coding:utf8-*-
# author: Todzhu 2017.12.01
import time,requests,argparse,os

parser = argparse.ArgumentParser(description="Function: KEGG Automatic Annotation use for uniprot protein")
parser.add_argument('-p',required=True,help='Input uniprot protein list')
parser.add_argument('-t',required=True,help='Input the taxonomy id in KEGG')
args = parser.parse_args()

KO2Gene = '/home/ztt/Annotation/KO2Gene'
Uniprot2KO = '/home/ztt/Annotation/Uniprot2KO_all'
Uniprot2KEGG = '/home/ztt/Annotation/Uniprot2KEGG_all'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

def keggAnnotation(prot_list,taxonomy):
    dict_ko = {}
    dict_kegg = {}
    dict_path = {}
    path_name_list = []
    path_description_list = []
    dict_ko_gene = {}
    #Download the taxonomy whole pathway
    print time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())+'\n'
    print 'Now loading {} pathway information from KEGG...\n'.format(taxonomy)


    with open('%s_path.txt' % taxonomy,'w') as f:
        response = requests.get('http://rest.kegg.jp/link/pathway/{}'.format(taxonomy),headers=headers)
        f.write(response.text)

    with open('%s_path.txt' % taxonomy, 'rb') as f:
        for line in f:
            line = line.strip().split('\t')
            path = line[0]
            pathway = line[1].split(':')[1]
            dict_path.setdefault(path,[]).append(pathway)

    # Get the pathway name to pathway description
    response = requests.get('http://rest.kegg.jp/list/pathway/{}'.format(taxonomy),headers=headers)
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

    print 'Now writing results...\n'

    with open('KEGG_pathway_annotation.xls','w') as f:
        f.write('Protein accession'+'\t'+'KEGG KO No.'+'\t'+'KEGG Gene'+'\t'+'KEGG pathway'+'\n')
        with open(prot_list, 'rb') as list:
            header = list.readline()
            for line in list:
                prot = line.strip().split('\t')[0]
                if prot in dict_ko:
                    ko = dict_ko[prot]
                    if ko in dict_ko_gene:
                        f.write(prot + '\t' + ko + '\t')
                        f.write(dict_ko_gene[ko]+'\t')
                    else:
                        f.write(prot)
                    if dict_kegg[prot] in dict_path:
                        for path in dict_path[dict_kegg[prot]]:
                            f.write(path + ' ' + dict_path_description[path] + '; ')
                    f.write('\n')
                else:
                    f.write(prot+'\n')
    os.system('rm *_path.txt')
    print 'KEGG annotation done !\n'
    print time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())+'\n'

keggAnnotation(args.p,args.t)
