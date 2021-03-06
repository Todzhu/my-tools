rm(list=ls())
setwd('C:/Users/Todzhu/Desktop/Z8079TQ')
library("Mfuzz");
args=commandArgs(T);
mydata=read.table(file='Z8079TQ.txt',sep="\t",header=T,row.names=1);
mydata=log10(mydata);
mydata=as.matrix(mydata);
set=ExpressionSet(assayData=mydata);
set.r=filter.NA(set,thres=0.25);
set.f=fill.NA(set.r,mode="mean");
tem=filter.std(set.f,min.std=0.05,visu=F);
set.s=standardise(tem);
cut=as.numeric(4);
cl=mfuzz(set.s,m=2,c=cut);
a=ceiling(sqrt(cut));
b=ceiling(cut/a);
pdf(file='Dynamic cluster.pdf',width=10,height=12);
mfuzz.plot2(set.s,cl=cl,mfrow=c(a,b),x11=F,time.labels=colnames(mydata));
dev.off();
warnings();
write.table(cl[3],file='Cluster.txt',sep="\t");
