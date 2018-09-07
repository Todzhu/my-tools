#!/usr/bin/env python
#-*-coding:utf8-*-
# author: Todzhu
# Date: 2018/6/28 10:48

import pandas as pd
import numpy as np
import xlsxwriter
import re

# delete the reverse and potential contaminant peptides function
def del_reverse_contaminant(dataframe):
    data = dataframe[(dataframe['Reverse'] != '+') & (dataframe['Potential contaminant'] != '+')]
    return data

sampleName = []
dict_sample = {}
with open('sample','r') as sample:
    for s in sample.readlines():
        s = s.strip()
        if '/' not in s:
            lable = s.split('\t')[0]
            sample = s.split('\t')[1]
            sampleName.append(sample)
            dict_sample[sample] = 'Reporter intensity '+lable
        else:
            sampleName.append(s.split('\t')[1]+' Ratio')

peptide = pd.read_csv('peptides.txt',sep='\t')
peptide = del_reverse_contaminant(peptide)[['Sequence','Unique (Groups)']]

evidence = pd.read_csv('evidence.txt',sep='\t')
evidence = del_reverse_contaminant(evidence)
evidence = pd.merge(evidence,peptide,on='Sequence',how='left')
evidence.rename(columns={'id':'ID','Leading Razor Protein':'Protein accession','Gene Names':'Gene name',
                         'Protein Names':'Protein description','Uncalibrated - Calibrated m/z [ppm]':'mass error [ppm]',
                         'Unique (Groups)':'Unique [yes/no]'},inplace=True)


pep_quant_title = ['ID','Sequence','Proteins','Protein accession','Protein description','Charge','m/z',
                   'mass error [ppm]','PEP','Score','Unique [yes/no]']
pep_quant_title.extend(list(dict_sample.keys()))


evidence[list(dict_sample.keys())] = evidence[list(dict_sample.values())].replace(0,np.nan).apply(lambda x: x/x.mean(),axis=1)
evidence = evidence.fillna('')

workbook = xlsxwriter.Workbook('MS_identified_information.xlsx')
pep_quant = workbook.add_worksheet('Peptide_quant')


for i in range(len(pep_quant_title)):
    pep_quant.write(0, i, pep_quant_title[i])

for index, row in evidence.iterrows():
    for i in range(len(pep_quant_title)):
        pep_quant.write(index+1, i, row[pep_quant_title[i]])


prot_group = pd.read_csv('proteinGroups.txt',sep='\t',usecols=['Majority protein IDs','Peptides','Unique peptides',
                        'Sequence coverage [%]','Mol. weight [kDa]','Score','MS/MS Count'])
prot_group.rename(columns={'Majority protein IDs':'Protein accession','sequence coverage [%]':'Coverage [%]',
                           'Mol. weight [kDa]':'MW [kDa]','MS/MS Count':'PSMs'},inplace=True)
prot_group['Protein accession'] = prot_group['Protein accession'].replace(r';.*','',regex=True)

prot_group = pd.merge(evidence,prot_group,on='Protein accession',how='left')


prot_group.to_csv('test.xls',sep='\t',index=False)

























workbook.close()