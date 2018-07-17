rm(list = ls())
setwd('C:/Users/Todzhu/Desktop/Z8030TQ')
library(gmodels)
library(ggplot2)

# read the expr data
data = read.table('Z8030TQ.txt',sep = '\t',header = T,row.names = 1)
# delete the missing value rows
data = na.omit(data)
# transpose the data
data = t(as.matrix(log2(data)))
# PCA analysis
data.pca = fast.prcomp(data,retx = T,scale = T,center = T)
# get the proportion of PC1 and PC2
summ = summary(data.pca)
tmp = summ[4]$importance
pro1 = as.numeric(sprintf("%3f",tmp[2,1]))*100
pro2 = as.numeric(sprintf("%3f",tmp[2,2]))*100

# 将成分矩阵转换为数据框
pc = as.data.frame(summ$x)

# 给pc的数据框添加名称列和分组列（用来画图）
group = c('T','P')
pc$group = group
pc$names = rownames(pc)

# plot
xlab=paste("PC1(",pro1,"%)",sep="") 
ylab=paste("PC2(",pro2,"%)",sep="")
pca=ggplot(pc,aes(PC1,PC2)) + 
  geom_point(size=3,aes(shape=group,color=group)) + 
  geom_text(aes(label=names),size=4)+labs(x=xlab,y=ylab,title="PCA") + 
  geom_hline(yintercept=0,linetype=4,color="grey") + 
  geom_vline(xintercept=0,linetype=4,color="grey") + 
  theme_bw()

# 保存结果
ggsave("Z8030TQ_PCA.pdf",pca,width=10,height=8)















