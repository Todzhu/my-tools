#!/usr/bin/env python
#-*-coding:utf8-*-
# author: Todzhu
# Date: 2018/7/26 11:32
import numpy as np
import pandas as pd


def delete(dataframe):
    dataframe = dataframe[(dataframe['Reverse']!='+') & (dataframe['Potential contaminant']!='+')]
    return dataframe

header = ['Majority protein IDs']
for i in range(10):
    header.append('Reporter intensity ' + str(i))

for n in range(6):
    prot = pd.read_table('proteinGroups'+str(n+1)+'.txt', sep='\t', )
    prot = delete(prot)
    prot[header[1:]] = prot[header[1:]].apply(lambda x: x / sum(x))
    prot[header].to_csv(str(n+1)+'.xls', sep='\t', index=None)
