#!/bin/usr/env python
# -*-coding=utf8-*-
import os,sys

blast_io = 'awk \'{print $1"\t"$2}\' blast.raw | uniq > blast_hit.txt'
prot_list = "cat blast.raw |sed 's/\t..|/\t/'|sed 's/|.*//'"

def blast(fasta):
    os.system('/home/download/ncbi-blast-2.2.28+/bin/blastp -query '+fasta+' -db /home/database/UniprotKB/UniprotKB_2017.11.15.fasta -evalue 1e-10 -num_threads 50 -max_target_seqs 1 -outfmt 6 -out blast.raw')
    os.system(blast_io)

blast(sys.argv[1])
