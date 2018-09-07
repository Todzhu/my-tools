#!/usr/bin/env python
#-*-coding:utf8-*-
# author: Todzhu
# Date: 2018/7/4 16:12

from scipy.stats import hypergeom

dict_cor = {}
with open('hippie_current.txt','r') as f:
    for line in f.readlines():
        line = line.split('\t')
        node1 = line[0]
        node2 = line[2]
        dict_cor.setdefault(node1,[]).append(node2)
        dict_cor.setdefault(node2,[]).append(node1)

diff = []
with open('diff.txt','r') as f:
    for line in f.readlines():
        gene = line.strip().split('\t')[1]
        diff.append(gene)

all_dp = len(diff)
all = len(dict_cor.keys())

with open('out.xls','w') as f:
    for i in diff:
        if i in dict_cor:
            cor_node = len(set(dict_cor[i]))
            related = ''
            diff_node = 0
            for j in set(dict_cor[i]):
                related = related + " " + j
                if j in diff:
                    diff_node += 1
            pvalue = hypergeom.sf(diff_node-1,all,all_dp,cor_node)
            f.write(i+'\t'+str(diff_node)+'\t'+str(cor_node)+'\t'+str(all_dp)+'\t'+str(all)+'\t'+str(pvalue)+'\t'+related+'\n')














