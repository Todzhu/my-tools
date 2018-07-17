#!/usr/bin/env python
# -*-coding=utf8-*-
import argparse
from Bio import SeqIO

parser = argparse.ArgumentParser(description = 'Function:  Give a protein list then take out sequences from the fasta file !')
parser.add_argument('-f','--fasta',help='Input the total protein fasta file')
parser.add_argument('-l','--list',help='Input the target protein list')
parser.add_argument('-o','--out',help='Input the result file name')
args = parser.parse_args()

def choose_fasta(fasta, prot_list, out):
    dict_seq = {}
    dict_overwrite = {}
    with open(out, 'w') as f:
        for record in SeqIO.parse(fasta, 'fasta'):
            prot_name = record.name
            if '|' in record.name:
                prot_name = prot_name.split('|')[1]
            prot_seq = record.seq
            dict_seq[prot_name] = prot_seq
        with open(prot_list, 'rb') as list:
            for line in list:
                line = line.strip().split('\t')
                prot = line[0]
                if prot in dict_seq:
                    f.write('>' + prot + '\n' + str(dict_seq[prot]) + '\n')
                    del dict_seq[prot]
                    dict_overwrite[prot] = 1
                elif dict_overwrite:
                    pass
                else:
                    print prot+'\t'+'not in the fasta file !'

choose_fasta(args.fasta,args.list,args.out)
