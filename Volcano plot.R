rm(list=ls())
library(ggplot2)
setwd('C:/Users/Todzhu/Desktop/Z8030TPST_初分析结果/Volcano plot')
data = read.table('data.txt',sep = '\t',header = T)
Type = data$Type
volcano = ggplot(data,aes(x=log2(data$FC),y=-log10(data$P),colour=Type))+geom_point()+
  scale_color_manual(values=c("green","gray","red"))+
  theme_bw()+xlim(-1,1)+ylim(-0,10)+labs(x="log2 (fold change)",y="-log10 (p value)")+
  geom_hline(yintercept = -log10(0.05))+geom_vline(xintercept = c(-0.263,0.263))
  
# 保存结果
ggsave("Volcano plot.pdf",volcano,width=10,height=8)