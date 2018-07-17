rm(list=ls())
library(clusterProfiler)
library(DOSE)
library(org.Hs.eg.db)
gene <- read.table('C:/Users/Todzhu/Desktop/gene_list.txt',sep = '\t',header = FALSE)
gene <- as.character(gene[,1])
ids <- bitr(gene,fromType = "SYMBOL",toType = "ENTREZID",OrgDb = "org.Hs.eg.db")
genes <- ids[,2]
ego <- enrichGO(gene = genes,'org.Hs.eg.db',ont = "CC",pvalueCutoff = 0.5,readable = TRUE)
enrich_gobp <- as.data.frame(ego)
barplot(ego)

