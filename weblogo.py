#!/usr/bin/env python
#-*-coding:utf8-*-
# Author: Todzhu
# Date: 2018/9/15 13:32

import requests

origin_url = 'http://weblogo.berkeley.edu'
referer_url = 'http://weblogo.berkeley.edu/logo.cgi'

head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

data = {
    'sequence':'EKWLEFKLQEKATVSHDSELF',
    'format':'PNG', 'logowidth':18, 'logoheight':5, 'logounits':'cm',
    'kind':'AUTO', 'firstnum':-10, 'smallsamplecorrection':'on', 'stretch':'on', 'symbolsperline':32, 'res':96,
    'res_units':'ppi', 'antialias':'on', 'yaxis_label':'bits', 'xaxis':'on', 'shrink':0.5, 'ticbits':1, 'colorscheme':'DEFAULT',
    'symbol1':'KRH', 'color1':'green', 'symbol2':'DE', 'color2':'blue', 'symbol3':'AVLIPWFM', 'color3':'red', 'color4':'black',
    'color5':'purple', 'color6':'orange', 'color7':'black', 'color0':'black', 'command':'Create Logo'}

response = requests.post(referer_url, data=data, headers=head,allow_redirects=False)

png_location = origin_url+'/'+response.headers['Location']

png = requests.get(png_location,headers=head)

with open('pic.png','wb') as p:
    p.write(png.content)
















