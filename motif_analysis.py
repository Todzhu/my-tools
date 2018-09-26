#!/usr/bin/env python
#-*-coding:utf8-*-
# author: Todzhu
# Date: 2018/9/11 14:20

import os
import argparse
import requests
import xlsxwriter
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(prog='motif_analysis.py',description="Use local MoMo motif-x algorithm get the modification site motif.")
parser.add_argument('-i', action='store', dest='modification', help='Input the identified modification site information file. example: MS_identified_information.txt')
parser.add_argument('-f', action='store', dest='database', help='Input the database fasta file')
parser.add_argument('-a', action='store', dest='amino', help='Input the modification site amino acid, if phosphorylation the amino acid = "Pho", else amino acid = "K"')
parser.add_argument('-e', action='store', dest='evalue', help='Input the motif-x evalue. default: 1.0E-6')
parser.add_argument('-n', action='store', dest='occurrence', help='Input the motif-x min occurrence. default: 20')
parser.add_argument('--version', action='version', version='%(prog)s 1.0')

parse = parser.parse_args()

class Motif:

    def __init__(self,database,Msdata,amino):
        self.database = database
        self.Msdata = Msdata
        self.amino = amino
        self.short_prot = []
        self.fasta = {}
        self.motif_pep = {}
        self.motif_logo = {}
        self.weblog = {}
        self.firstnum = -10

    def database_filter(self):
        with open(self.database, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if line.startswith('>'):
                    name = line.split()[0]
                    if '|' in name:
                        name = '>' + line.split('|')[1]
                        self.fasta[name] = ''
                    else:
                        self.fasta[name] = ''
                else:
                    self.fasta[name] += line + '\n'

        with open('motif_database.fasta', 'w') as f:
            for key in self.fasta:
                # Filter sequences length less than 10
                if len(self.fasta[key]) > 10:
                    # Replace U amino acid to X
                    f.write(key + '\n' + self.fasta[key].replace('U', 'X'))
                else:
                    self.short_prot.append(key)

        print('Database filtering...   '
              '\n\tThere are '+str(len(self.short_prot))+' proteins sequence length < 10aa'
              '\n\tFormat background database to momo software done')


    def motif_peptide(self, probability=0.75):
        header = {}

        with open(self.Msdata, 'r') as Ms:
            head = Ms.readline().split('\t')
            for i in range(len(head)):
                header[head[i]] = i

            if self.amino == 'K':
                for line in Ms.readlines():
                    line = line.strip().split('\t')
                    prot = '>' + line[0]
                    position = int(line[1])
                    if prot in self.fasta.keys():
                        sequence = self.fasta[prot].replace('\n', '')
                        if position - 10 <= 0:
                            self.motif_pep[prot + '-' + str(position)] = (10 - position + 1) * '-' + sequence[:position] + sequence[position:position + 10]
                        elif position + 10 > len(sequence):
                            self.motif_pep[prot + '-' + str(position)] = sequence[position - 11:] + (position + 10 - len(sequence)) * '-'
                        else:
                            self.motif_pep[prot + '-' + str(position)] = sequence[position - 11:position + 10]
                with open('motif_peptide_K.fasta', 'w') as out:
                    for key in self.motif_pep:
                        out.write(key + '\n' + self.motif_pep[key] + '\n')

                print('\tWrite motif_peptide_K.fasta file done\n')

            if self.amino == 'Pho':
                self.firstnum = -6
                for line in Ms.readlines():
                    line = line.strip().split('\t')
                    prot = '>' + line[0]
                    position = int(line[1])
                    if prot in self.fasta.keys() and float(line[header['Localization probability']]) >= probability:
                        sequence = self.fasta[prot].replace('\n', '')
                        if position - 6 <= 0:
                            self.motif_pep[prot + '-' + str(position)] = (6 - position + 1) * '-' + sequence[:position] + sequence[position:position + 6]
                        elif position + 6 > len(sequence):
                            self.motif_pep[prot + '-' + str(position)] = sequence[position - 7:] + (position + 6 - len(sequence)) * '-'
                        else:
                            self.motif_pep[prot + '-' + str(position)] = sequence[position - 7:position + 6]

                    elif prot not in self.fasta.keys():
                        print(prot.replace('>','') + '\t' + 'not in the database ...')

                with open('motif_peptide_Pho.fasta', 'w') as pho:
                    for key in self.motif_pep:
                            pho.write(key + '\n' + self.motif_pep[key] + '\n')

                print('Write Phosphorylation motif peptide file done.\n')

    def momo(self,e=1.0E-6,occurrence=20):
        if self.amino == 'K':
            os.system('/home/download/meme/bin/momo motifx -oc ./motif --verbosity 1 --width 21 --protein-database motif_database.fasta --db-background '
                  '--eliminate-repeats 21 --min-occurrences %s --harvard --score-threshold %s motif_peptide_K.fasta' % (occurrence,e))
            print("MoMo Paramenters:\n\t\talgoithm: motif-x\n\t\tpost-translationally modified peptide filenames: motif_peptide_K.fasta\n\t\tprotein database filename: motif_database.fasta\n\t\tmotif width: 21\n\t\teliminate repeats: true\n\t\teliminate repeat width: 21\n\t\tmin occurrences: %s \n\t\tscore threshold: %s\n" % (occurrence, e))
		
        if self.amino == 'Pho':
            os.system('/home/download/meme/bin/momo motifx -oc ./motif --verbosity 1 --width 13 --protein-database motif_database.fasta --db-background '
                  '--eliminate-repeats 13 --min-occurrences %s --harvard --score-threshold %s motif_peptide_Pho.fasta' % (occurrence,e))
            print("MoMo Paramenters:\n\t\talgoithm: motif-x\n\t\tpost-translationally modified peptide filenames: motif_peptide_Pho.fasta\n\t\tprotein database filename: motif_database.fasta\n\t\tmotif width:13\n\t\teliminate repeats: true\n\t\teliminate repeat width: 13\n\t\tmin occurrences: %s \n\t\tscore threshold: %s\n" % (occurrence, e))

        try:
            os.system('rm ./motif/*.png')
        except:
            print("There are no motif find...")

    def parse_momo_result(self):
        row = 3
        col = 1
        pic_png = []

        workbook = xlsxwriter.Workbook('motif-x.xlsx')
        worksheet1 = workbook.add_worksheet('motif-x')
        worksheet1.set_column('F:F',18)
        worksheet2 = workbook.add_worksheet('motif annotation')
        worksheet2.set_column('A:A',10)
        worksheet2.set_column('D:D',18)

        head_format = workbook.add_format({
            'font_name': 'Times New Roman',
            'bold': True,
            'font_size': 11,
            'valign': 'vdistributed',
            'align': 'center',
            'border': 2,
            'bg_color': '#D7E4Bc',
            'left': 0,
            'right': 0
        })

        cell_format = workbook.add_format({
            'font_name':'Times New Roman',
            'font_size': 10,
            'align':'center',
            'valign': 'vdistributed',
            'border': 2,
            'left': 0,
            'right': 0
        })

        cell_format1 = workbook.add_format({
            'font_name':'Times New Roman',
            'font_size': 10,
            'align':'center',
            'valign': 'vdistributed'
        })


        worksheet1.merge_range(2, 1, 3, 4, "Motif Logo",head_format)
        worksheet1.merge_range(2, 5, 3, 5, "Motif",head_format)
        worksheet1.merge_range(2, 6, 3, 6, "Motif Score",head_format)
        worksheet1.merge_range(2, 7, 2, 8, "Foreground",head_format)
        worksheet1.merge_range(2, 9, 2, 10, "Background",head_format)
        worksheet1.merge_range(2, 11, 3, 11, "Fold Increase",head_format)
        worksheet1.write(3, 7, 'Matches',head_format)
        worksheet1.write(3, 8, 'Size',head_format)
        worksheet1.write(3, 9, 'Matches',head_format)
        worksheet1.write(3, 10, 'Size',head_format)

        # parser momo.html file to get the motif_annotation
        soup = BeautifulSoup(open('./motif/momo.html'),'html.parser')
        for li in soup.find_all(alt='sequence logo of motif'):
            motif_logo = li.parent.find('img')['src'].replace('.png','')
            motif_seq = li.parent.find(class_="console").get_text()
            self.weblog[motif_logo] = motif_seq
            for seq in motif_seq.split('\n'):
                if seq != '':
                    self.motif_logo[seq] = motif_logo

        origin_url = 'http://weblogo.berkeley.edu'
        referer_url = 'http://weblogo.berkeley.edu/logo.cgi'
        head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}


        for key in self.weblog:
            sequence = self.weblog[key].strip()
            data = {
            'sequence': sequence,'format': 'PNG', 'logowidth': 18, 'logoheight': 5, 'logounits': 'cm',
            'kind': 'AUTO', 'firstnum': self.firstnum, 'smallsamplecorrection': 'on', 'stretch': 'on', 'symbolsperline': 32,
            'res': 96,'res_units': 'ppi', 'antialias': 'on', 'yaxis_label': 'bits', 'xaxis': 'on', 'shrink': 0.5, 'ticbits': 1,
            'colorscheme': 'DEFAULT','symbol1': 'KRH', 'color1': 'green', 'symbol2': 'DE', 'color2': 'blue', 'symbol3': 'AVLIPWFM',
            'color3': 'red', 'color4': 'black','color5': 'purple', 'color6': 'orange', 'color7': 'black', 'color0': 'black', 'command': 'Create Logo'}

            response = requests.post(referer_url, data=data, headers=head, allow_redirects=False)

            png_location = origin_url + '/' + response.headers['Location']

            png = requests.get(png_location, headers=head)
            with open(key+'.png','wb') as f:
                print('Downloading motif picture: '+key)
                f.write(png.content)

        files = os.listdir('./')
        for file in files:
            if file.endswith('.png'):
                pic_png.append(file.replace('.png',''))

        with open('./motif/momo.tsv', 'r') as f:
            header = f.readline().split('\t')
            for line in f.readlines():
                if not line.startswith('#'):
                    line = line.strip().split('\t')
                    logo = line[0]
                    for i in range(len(line) - 1):
                        worksheet1.write(row + 1, col + i + 4, line[i], cell_format)
                        worksheet1.set_row(row + 1, 45)
                    if logo in pic_png:
                        worksheet1.insert_image(row + 1, col, logo+'.png', {'x_scale': 0.4, 'y_scale': 0.4, 'x_offset':-10, 'y_offset':0.5})
                    row += 1

        # Write motif annotation worksheet
        motif_annotation_header = ['Protein accession','Position','Amino acid','Motif logo']
        for i in range(len(motif_annotation_header)):
            worksheet2.write(0,i,motif_annotation_header[i],head_format)
        n = 1
        for prot in self.motif_pep:
            if self.motif_pep[prot] in self.motif_logo:
                seq = self.motif_pep[prot]
                position = prot.split('-')[1]
                worksheet2.write(n, 0, prot.split('-')[0].replace('>', ''), cell_format1)
                worksheet2.write(n, 1, position, cell_format1)
                worksheet2.write(n, 2, seq[int(len(seq) / 2)], cell_format1)
                worksheet2.write(n, 3, self.motif_logo[self.motif_pep[prot]],cell_format1)
            else:
                n -=1
            n += 1

        workbook.close()
        os.system('mv *.png motif-x.xlsx motif_database.fasta motif_peptide_*.fasta ./motif')


if __name__ == '__main__':

    motif = Motif(parse.database,parse.modification,parse.amino)
    motif.database_filter()
    motif.motif_peptide()
    
    if parse.evalue and parse.occurrence:
        motif.momo(parse.evalue, parse.occurrence)
    elif parse.evalue:
        motif.momo(parse.evalue)
    elif parse.occurrence:
        motif.momo(parse.occurrence)
    else:
        motif.momo()
    
    motif.parse_momo_result()
