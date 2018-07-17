rm(list=ls())
setwd('E:/R_work_place/WGCNA_Test')
library(WGCNA)
options(stringsAsFactors = FALSE) 
#Step1: 读取蛋白表达序列矩阵然后进行中心化变换
data = read.table('data.txt',sep = '\t',header = T,row.names = 1)
data = scale(t(log2(data)),center = T,scale = T)  #按行进行中心化变换（即数据转置）
#Step2: 检查是否有离群样品(可省略)
sampleTree = hclust(dist(data),method = "average")
pdf(file = "sampleClustering.pdf", width = 12, height = 9)
plot(sampleTree, main = "Sample clustering to detect outliers", sub="", xlab="", cex.lab = 1.5,
     cex.axis = 1.5, cex.main = 2)
dev.off()
#Step3: SoftThreshold(软阈值的筛选原则是使构建的网络更符合无标度网络特征)
#横轴是Soft threshold (power)，纵轴是无标度网络的评估参数，数值越高，网络越符合无标度特征 (non-scale)
powers = c(c(1:10), seq(from = 12, to=30, by=2))
sft = pickSoftThreshold(data, powerVector=powers, verbose=5)
pdf('Softhreshold.pdf')
par(mfrow = c(1,2))
cex1 = 0.9
plot(sft$fitIndices[,1], -sign(sft$fitIndices[,3])*sft$fitIndices[,2],
     xlab="Soft Threshold (power)",
     ylab="Scale Free Topology Model Fit,signed R^2",type='n',
     main = paste("Scale independence"))
text(sft$fitIndices[,1], -sign(sft$fitIndices[,3])*sft$fitIndices[,2],labels=powers,cex=cex1,col="red")
# 筛选标准 R-square=0.9
abline(h=0.9,col="red")
# Soft threshold与平均连通性
plot(sft$fitIndices[,1], sft$fitIndices[,5],
     xlab="Soft Threshold (power)",ylab="Mean Connectivity", type="n",
     main = paste("Mean connectivity"))
text(sft$fitIndices[,1], sft$fitIndices[,5], labels=powers, 
     cex=cex1, col="red")
dev.off()
#网络构建
power = sft$powerEstimate
net = blockwiseModules(data, power = power,
                       TOMType = "unsigned", minModuleSize = 30,
                       reassignThreshold = 0, mergeCutHeight = 0.25,
                       numericLabels = TRUE, pamRespectsDendro = FALSE,
                       saveTOMs=TRUE, 
                       saveTOMFileBase = "TOM",
                       verbose = 3)
table(net$colors)
write.table(net$colors,file = 'wgcna.xls',sep = '\t')

#层级聚类树展示module
moduleLabels = net$colors
moduleColors = labels2colors(moduleLabels)
plotDendroAndColors(net$dendrograms[[1]], moduleColors[net$blockGenes[[1]]],
                    "Module colors",
                    dendroLabels = FALSE, hang = 0.03,
                    addGuide = TRUE, guideHang = 0.05)
moduleLabels = net$colors
moduleColors = labels2colors(net$colors)
MEs = net$MEs;
geneTree = net$dendrograms[[1]];
save(MEs, moduleLabels, moduleColors, geneTree,
     file = "FemaleLiver-02-networkConstruction-auto.txt")






#
MEs = net$MEs
MEs_col = MEs
par(cex = 0.8);
#par(mar = c(0,4,2,0))
colnames(MEs_col) = paste0("ME", labels2colors(
  as.numeric(str_replace_all(colnames(MEs),"ME",""))))
MEs_col = orderMEs(MEs_col)
plotEigengeneNetworks(MEs_col, "Eigengene adjacency heatmap", 
                      marDendro = c(3,3,2,4),
                      marHeatmap = c(3,4,2,2), plotDendrograms = T, 
                      xLabelsAngle = 45)







