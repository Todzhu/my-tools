rm(list = ls())
setwd("C:/Users/Todzhu/Desktop")
library(ConsensusClusterPlus)
mydata = read.table("C:/Users/Todzhu/Desktop/Z8030TQ.txt",sep = '\t',header = TRUE,row.names = 1)
mydata = na.omit(mydata)
mydata = log2(mydata)
mydata = t(scale(t(mydata),center = TRUE,scale = TRUE))
results = ConsensusClusterPlus(mydata,maxK=6,reps=1000,pItem=0.8,pFeature=1,title="Z8030TQ_ConsensuseCluster",clusterAlg="kmdist",distance="pearson",seed=1262118388.71279,plot="png",writeTable = T)


