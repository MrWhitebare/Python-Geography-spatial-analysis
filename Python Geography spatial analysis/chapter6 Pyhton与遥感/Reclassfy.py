# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 22:08:05 2020

@author: 立文
"""
#Reclassfy.py 图像分类
from osgeo import gdal_array
src=r"D:\Program Files\Python学习文档\samples\thermal\thermal.tif"
target=r"D:\Program Files\Python学习文档\samples\thermal\classified.jpg"
#使用gdal库加载图片
srcArray=gdal_array.LoadFile(src)
#根据类别数目将直方图分割为20个颜色区间
classes=gdal_array.numpy.histogram(srcArray,bins=20)[1]
#颜色查找表的记录数必须为len(classes)+1
#声明R，G，B元组
lut = [[255, 0, 0], [191, 48, 48], [166, 0, 0], [255, 64, 64], [255, 115, 115],
       [255, 116, 0], [191, 113, 48], [255, 178, 115], [0, 153, 153],
       [29, 115, 115], [0, 99, 99], [166, 75, 0], [0, 204, 0], [51, 204, 204],
       [255, 150, 64], [92, 204, 204], [38, 153, 38], [0, 133, 0],
       [57, 230, 57], [103, 230, 103], [184, 138, 0]]
#分类初始化
start=1
#创建一个RGB颜色的JPEG输出图片
rgb=gdal_array.numpy.zeros((3, srcArray.shape[0],srcArray.shape[1],), gdal_array.numpy.float32)
#处理所有类并声明颜色
for i in range(len(classes)):
    mask=gdal_array.numpy.logical_and(start<=srcArray,srcArray<=classes[i])
    for j in range(len(lut[i])):
        rgb[j]=gdal_array.numpy.choose(mask,(rgb[j],lut[i][j]))
    start=classes[i]+1
#save
output=gdal_array.SaveArray(rgb.astype(gdal_array.numpy.uint8),target,format="JPEG")
output=None
print("分类完成!")

