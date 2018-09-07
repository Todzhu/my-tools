#!/usr/bin/env python
#-*-coding:utf8-*-
# author: Todzhu
# Date: 2018/8/17 19:37

import xlsxwriter

dict_cog = {}
with open('KOG.txt','r') as f:
    head = f.readline()
    for line in f.readlines():
        line = line.strip().split('\t')
        category = line[1]
        prot = line[0]
        if len(category) == 1:
            dict_cog.setdefault(category,[]).append(prot)
        else:
            for i in category:
                dict_cog.setdefault(i,[]).append(prot)

dict_expr = {}
with open('LP2o.txt','r') as f:
    header = f.readline()
    for line in f.readlines():
        line = line.strip().split('\t')
        regulate = line[1]
        prot = line[0]
        dict_expr.setdefault(regulate,[]).append(prot)

dict_2d = {}
result_up = {}
result_down = {}
for key1 in dict_expr:
    if key1 == 'Up':
        for category in dict_cog:
            for key2 in dict_expr[key1]:
                if key2 in dict_cog[category]:
                    result_up.setdefault(category,[]).append(key2)
        dict_2d[key1] = result_up
    else:
        for category in dict_cog:
            for key2 in dict_expr[key1]:
                if key2 in dict_cog[category]:
                    result_down.setdefault(category,[]).append(key2)
        dict_2d[key1] = result_down


l = ['J','A','K','L','B','D','Y','V','T','M','N','Z','W','U','O','C','G','E','F','H','I','P','Q','R','S']
for key in dict_2d:
    print(key)
    for key1 in l:
        if key1 in dict_2d[key]:
            prot = ' '.join(dict_2d[key][key1])
            print(key1+'\t'+prot+'\t'+str(len(dict_2d[key][key1])))
        else:
            pass


# for key in dict_2d:
#     print(key)
#     for key1 in dict_2d[key]:
#         prot = ' '.join(dict_2d[key][key1])
#         print(key1+'\t'+prot+'\t'+str(len(dict_2d[key][key1])))













