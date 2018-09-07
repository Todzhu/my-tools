#!/usr/bin/env python
#-*-coding:utf8-*-
# author: Todzhu
# Date: 2018/9/4 10:20

import re
import requests

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'}

url = 'https://web.expasy.org/cgi-bin/compute_pi/pi_tool'

dict_pi = {}
with open('p.fasta','r') as f:
    for line in f.readlines():
        if line.startswith('>'):
            name = line.strip().replace('>','')
            dict_pi[name] = ''
        else:
            dict_pi[name] += line.replace('\n','')

with open('prot_pi.txt','w') as f:
    for prot in dict_pi:
        data = {'protein': dict_pi[prot],'resolution':'average'}
        response = requests.post(url,data,headers=header)
        result = re.findall('Theoretical pI/Mw: (.*) / (.*)', response.text)
        if result:
            print(prot + '\t' + result[0][0] + '\t' + result[0][1])
        else:
            print(prot)











