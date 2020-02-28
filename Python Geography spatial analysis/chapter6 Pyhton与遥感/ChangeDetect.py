# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 13:22:29 2020

@author: 立文
"""
#ChangeDetect.py 变化检测
from osgeo import gdal,gdal_array
import numpy as np
img1=r"D:\Program Files\Python学习文档\samples\detect\before.tif"
img2=r"D:\Program Files\Python学习文档\samples\detect\after.tif"
array1=gdal_array.LoadFile(img1).astype(np.int8)
array2=gdal_array.LoadFile(img2)[1].astype(np.int8)
diff=array2-array1
#建立类别并输出变化特征
classes=np.histogram(diff,bins=5)[1]
#用黑色掩模裁切不是特别明显的变化特征
lut=[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,255,0],[255,0,0]]
#开始分类
start=1
rgb=np.zeros((3,diff.shape[0],diff.shape[1],),np.int8)
#处理所有类别并且分配颜色
for i in range(len(classes)):
    mask=np.logical_and(start<=diff,diff<=classes[i])
    for j in range(len(lut[i])):
        rgb[j]=np.choose(mask,(rgb[j],lut[i][j]))
    start=classes[i]+1
#save
out=r"D:\Program Files\Python学习文档\samples\detect\different.tif"
output=gdal_array.SaveArray(rgb,out,format="GTIFF",prototype=img2)
output=None
print("变化检测完成！")