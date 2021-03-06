rm(list=ls())
library(corrplot)
data <- read.table('C:/Users/Todzhu/Desktop/7946TQ_rawdata.txt',header = T,sep = '\t',row.names = 1)
data <- log2(data)
data <- t(scale(t(data),center = T, scale = F))
pearson <- cor(data,use="complete",method = "pearson")
write.table(pearson,file = "C:/Users/Todzhu/Desktop/Pearson.txt",sep = '\t')
col=colorRampPalette(c("green", "white", "firebrick3"))
corrplot(pearson,method = "circle",title="Pearson's correlation coefficient",tl.col='black',col = col(10))