#!/usr/bin/env python
#-*-coding:utf8-*-
# author: Todzhu
# Date: 2018/9/4 14:13

content = []
with open('string_name.txt','r') as f:

    for line in f.readlines():
        line = line.strip()
        content.append(line)

    for i in range(len(content)):
        if content[i].endswith(':'):
            prot = content[i].replace('\'','').replace(':','')
            print(prot + '\t' + content[i+1])




































