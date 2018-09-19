#!/usr/bin/env python
#-*-coding:utf8-*-
# author: Todzhu
# Date: 2018/9/11 14:20

import os
import requests
import xlsxwriter
from bs4 import BeautifulSoup


class Motif:

    def __init__(self,database,Msdata):
        self.database = database
        self.Msdata = Msdata
        self.short_prot = []
        self.fasta = {}
        self.motif_pep = {}
        self.motif_logo = {}
        self.weblog = {}

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
              '\nThere are '+str(len(self.short_prot))+' proteins sequence length < 10aa;'
              '\nFormat background database to momo software done.')


    def motif_peptide(self, amino, probability=0.75):
        header = {}

        with open(self.Msdata, 'r') as Ms:
            head = Ms.readline().split('\t')
            for i in range(len(head)):
                header[head[i]] = i

            if amino == 'K':
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

                print('\nWrite motif_peptide_K.fasta file done.')


            if amino == 'Pho':
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

                with open('motif_peptide_S.fasta', 'w') as S:
                    with open('motif_peptide_T.fasta', 'w') as T:
                        with open('motif_peptide_Y.fasta', 'w') as Y:
                            for key in self.motif_pep:
                                if self.motif_pep[key][6] == 'S':
                                    S.write(key + '\n' + self.motif_pep[key] + '\n')
                                elif self.motif_pep[key][6] == 'T':
                                    T.write(key + '\n' + self.motif_pep[key] + '\n')
                                elif self.motif_pep[key][6] == 'Y':
                                    Y.write(key + '\n' + self.motif_pep[key] + '\n')

                print('\nWrite Phosphorylation motif peptide file done.')

    # def momo(self):
    #     os.system('/home/ztt/biosoft/bin/momo motifx -oc ./motif --verbosity 1 --width 21 --protein-database motif_database.fasta --db-background '
    #               '--eliminate-repeats 21 --min-occurrences 20 --harvard --score-threshold 1.0E-6 motif_peptide_K.fasta')


    def parse_momo_result(self):
        row = 0
        col = 2
        pic_png = []
        workbook = xlsxwriter.Workbook('motif-x.xlsx')
        worksheet1 = workbook.add_worksheet('motif-x')
        worksheet2 = workbook.add_worksheet('motif annotation')
        # files = os.listdir('./')
        # for file in files:
        #     if file.endswith('.png'):
        #         png.append(file.replace('.png',''))

        # for i in range(len(png)):
        #     worksheet1.insert_image(row,0,png[i]+'.png',{'x_scale': 0.5, 'y_scale': 0.35,'x_offset': 65, 'y_offset': 0})
        #     row += 5

        worksheet1.set_column('B:B', 45.75)
        worksheet1.set_column('C:C',23)
        worksheet1.set_row(0,30)

        worksheet2.set_column('A:A', 15)
        worksheet2.set_column('C:C',10)
        worksheet2.set_column('D:D', 25)
        worksheet2.set_row(0,25)

        head_format = workbook.add_format()
        cell_format = workbook.add_format()
        head_format.set_font_name('Times New Roman')
        head_format.set_font_size(11)
        head_format.set_bold()
        head_format.set_align('center')
        head_format.set_align('vdistributed')

        cell_format.set_font_name('Times New Roman')
        cell_format.set_align('center')
        cell_format.set_align('vdistributed')


        # with open('momo.tsv','r') as f:
        #     header = f.readline().split('\t')
        #     for i in range(len(header)):
        #         worksheet1.write(row,col+i,header[i].capitalize(),head_format)
        #     for line in f.readlines():
        #         if not line.startswith('#'):
        #             line = line.strip().split('\t')
        #             logo = line[0]
        #             for i in range(len(line)):
        #                 worksheet1.write(row+1,col+i,line[i],cell_format)
        #                 worksheet1.set_row(row+1,73)
        #             if logo in pic_png:
        #                 worksheet1.insert_image(row+1,col-1,logo+'.png',{'x_scale': 0.5, 'y_scale': 0.5})
        #             row += 1


        # parser momo.html file to get the motif_annotation
        soup = BeautifulSoup(open('momo.html'),'html.parser')
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
            'kind': 'AUTO', 'firstnum': -6, 'smallsamplecorrection': 'on', 'stretch': 'on', 'symbolsperline': 32,
            'res': 96,'res_units': 'ppi', 'antialias': 'on', 'yaxis_label': 'bits', 'xaxis': 'on', 'shrink': 0.5, 'ticbits': 1,
            'colorscheme': 'DEFAULT','symbol1': 'KRH', 'color1': 'green', 'symbol2': 'DE', 'color2': 'blue', 'symbol3': 'AVLIPWFM',
            'color3': 'red', 'color4': 'black','color5': 'purple', 'color6': 'orange', 'color7': 'black', 'color0': 'black', 'command': 'Create Logo'}

            response = requests.post(referer_url, data=data, headers=head, allow_redirects=False)

            png_location = origin_url + '/' + response.headers['Location']

            png = requests.get(png_location, headers=head)
            with open(key+'.png','wb') as f:
                f.write(png.content)






        files = os.listdir('./')
        for file in files:
            print(file)
            if file.endswith('.png'):
                pic_png.append(file.replace('.png',''))

        with open('momo.tsv','r') as f:
            header = f.readline().split('\t')
            for i in range(len(header)):
                worksheet1.write(row,col+i,header[i].capitalize(),head_format)
            for line in f.readlines():
                if not line.startswith('#'):
                    line = line.strip().split('\t')
                    logo = line[0]
                    for i in range(len(line)):
                        worksheet1.write(row+1,col+i,line[i],cell_format)
                        worksheet1.set_row(row+1,73)
                if logo in pic_png:
                        worksheet1.insert_image(row+1,col-1,logo+'.png',{'x_scale': 0.5, 'y_scale': 0.5})
                row += 1



        # Write motif annotation worksheet
        motif_annotation_header = ['Protein accession','Position','Amino acid','Motif logo']
        for i in range(len(motif_annotation_header)):
            worksheet2.write(0,i,motif_annotation_header[i],head_format)
        n = 1
        for prot in self.motif_pep:
            seq = self.motif_pep[prot]
            position = prot.split('-')[1]
            worksheet2.write(n, 0, prot.split('-')[0].replace('>', ''),cell_format)
            worksheet2.write(n, 1, position,cell_format)
            worksheet2.write(n, 2, seq[int(len(seq) / 2)],cell_format)
            if self.motif_pep[prot] in self.motif_logo:
                worksheet2.write(n, 3, self.motif_logo[self.motif_pep[prot]],cell_format)
            n += 1

        workbook.close()


if __name__ == '__main__':

    motif = Motif('3847_PR_Glycine_201707.fasta','MS_identified_information.txt')
    #motif.database_filter()
    #motif.motif_peptide('Pho')
    motif.parse_momo_result()