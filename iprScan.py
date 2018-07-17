#!/usr/bin/env python
#-*-coding:utf8-*-
# Function: InterProScan sequence search local service
import os,sys

fasta = sys.argv[1]

interproscan = '/home/download/interproscan-5.22-61.0/interproscan.sh -i {} -goterms -iprlookup -pa -f TSV -o out.ipr'
entry_list = '/home/database/interpro/entry_list.txt'

def iprScan(fasta):
    os.system(interproscan.format(fasta))
    os.system('rm -r temp')

def ipr_IO():
    dict_ipr = {}
    dict_go = {}
    dict_domain = {}
    dict_ipr_desc = {}
    dict = {}
    with open('out.ipr', 'rb') as ipr:
        for line in ipr:
            line = line.strip().split('\t')
            prot = line[0]
            if '|' in prot:
                prot = prot.split('|')[1]
            else:
                prot = prot.split()[0]
            for i in range(len(line)):
                if i == 11:
                    ipr_id = line[11]
                    ipr_desc = line[12]
                    dict_ipr.setdefault(prot, []).append(ipr_id)
                    dict_ipr_desc[ipr_id] = ipr_desc

                if i == 13 and line[13] != '':
                    go_id = line[13].split('|')
                    for go_id in go_id:
                        dict_go.setdefault(prot, []).append(go_id)

    with open(entry_list,'rb') as entry:
        for line in entry:
            line = line.strip().split('\t')
            if line[1] == 'Domain':
                dict_domain[line[0]] = line[1]
        for key in dict_ipr:
            for ipr in dict_ipr[key]:
                if ipr in dict_domain:
                    dict[key] = 1

    with open('ipr.xls', 'w') as f:
        for key1 in dict_ipr:
            for value in dict_ipr[key1]:
                if value in dict_domain:
                    f.write(key1+'\t'+value+'\n')

    with open('go.xls', 'w') as f:
        for key1 in dict_go:
            f.write(key1 + '\t')
            for key2 in list(set(dict_go[key1])):
                f.write(key2 + '\t')
            f.write('\n')

    with open('Domain_annotation.xls','w') as f:
        f.write('Protein accession'+'\t'+'IPR ID'+'\t'+'Domain description'+'\n')
        for prot in dict_ipr:
            if prot in dict:
                f.write(prot+'\t')
                for ipr in list(set(dict_ipr[prot])):
                    if ipr in dict_domain:
                        f.write(ipr+'; ')
                f.write('\t')
                for ipr in list(set(dict_ipr[prot])):
                    if ipr in dict_domain:
                        f.write(dict_ipr_desc[ipr]+'; ')
                f.write('\n')

iprScan(fasta)
ipr_IO()
