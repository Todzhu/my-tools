#!/usr/bin/env python
#-*-coding:utf8-*-
# author: Todzhu
# Date: 2018/7/20 15:04

import re
regx = re.compile(' - .*')

all_background = []
dict_path = {}
with open('KEGG_pathway_annotation.xls','r') as f:
    header = f.readline()
    for line in f.readlines():
        line = line.strip().split('\t')
        if len(line) >= 4:
            protein = line[0]
            all_background.append(protein)
            pathway = line[3].split('; ')
            for path in pathway:
                path = regx.sub('',path)
                dict_path.setdefault(path,[]).append(protein)
                dict_path[protein] = path

diff_prot = {}
allMapping = []
with open('diff.txt','r') as f:
    head = f.readline()
    ident_anno = 0

    for line in f.readlines():
        prot = line.strip().split('\t')[0]
        if prot in all_background:
            ident_anno += 1
            diff_prot[prot] = 1
        if prot in dict_path:
            allMapping.append(prot)

background_path = {}
mapping = {}
allMapping = {}
for path in dict_path:
    for i in diff_prot:
        if i in dict_path[path]:
            background_path.setdefault(path,[]).append(i)
    for prot in dict_path[path]:
        if prot in diff_prot:
           mapping.setdefault(path,[]).append(prot)





















