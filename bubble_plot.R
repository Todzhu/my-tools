rm(list=ls())
setwd('C:/Users/Todzhu/Desktop')
library(ggplot2)
#data <- read.table('path.txt',header = T,sep = '\t')
#ggplot(data,aes(FC,pathway))+geom_point(aes(size=count,color=P))+scale_color_gradient(low = 'blue',high = 'red')+labs(x='Fold enrichment',y='Pathway',color='P value',size='Protein Number',title='KEGG pathway enrichment')+theme_bw()

#data <- read.table('GO.txt',header = T,sep = '\t')
#ggplot(data,aes(FC,GO))+geom_point(aes(size=count,color=P))+scale_color_gradient(low = 'blue',high = 'red')+labs(x='Fold enrichment',y='GO Terms',color='P value',size='Protein Number',title='Gene Ontology enrichment')+theme_bw()


data <- read.table('DO.txt',header = T,sep = '\t')
ggplot(data,aes(FC,DO))+geom_point(aes(size=count,color=P))+scale_color_gradient(low = 'blue',high = 'red')+labs(x='Fold enrichment',y='Protein Domain',color='P value',size='Protein Number',title='Protein domain enrichment')+theme_bw()




