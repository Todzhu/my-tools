rm(list=ls())
setwd('C:/Users/Todzhu/Desktop/Boxplot')
library(ggplot2)
datExp = read.table('data.txt',sep = '\t',header = T,row.names = 1)
datExp = na.omit(datExp)

proteins = rownames(datExp)
samples = colnames(datExp)
n = length(proteins)
m = length(samples)
sum = m*n
sum*3

temp = rep(0,sum*3)
dim(temp) = c(sum,3)

for (i in 1:n){
  for (j in 1:m)
  {
    index = j + (i-1)*m
    temp[index,] = c(proteins[i],samples[j],datExp[i,j])
  }
}

newexpr = data.frame(proteins=temp[,1],samples=temp[,2],Ratio=as.numeric(temp[,3]))

ggplot(newexpr,aes(samples,log2(Ratio))) + 
  geom_boxplot(outlier.size=-1,aes(fill=samples)) + 
  theme(legend.position="none",axis.text=element_text(size=6,colour="black")) + 
  labs(y=expression(log2(Ratio)),title="boxplot of 60 samples") +
  geom_hline(aes(yintercept=0))





