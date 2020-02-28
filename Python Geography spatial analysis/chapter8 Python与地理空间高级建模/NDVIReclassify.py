# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 11:10:46 2020

@author: 立文
"""
#NDVIReclassify.py NDVI分类
from osgeo import gdal_array
import operator
from functools import reduce
import time
def Histogram(a,bins=list(range(256))):
    #多维数组直方图函数 a[数组] bins[区间分配数值]
    fa=a.flat
    #把直方图相关的数据均衡化，排序和分隔
    n=gdal_array.numpy.searchsorted(gdal_array.numpy.sort(fa),bins)
    n=gdal_array.numpy.concatenate([n,[len(fa)]])
    hist=n[1:]-n[:-1]
    return hist
def stretch(a):
	#在gdal_array数据图像中执行直方图 平均化操作
	hist=Histogram(a)
	lut=[]
	for b in range(0,len(hist),256):
		#步长值：创建相等的间隔区间
		step=reduce(operator.add,hist[b:b+256])/256
		#创建均衡化查找表
		n=0
		for i in range(256):
			lut.append(n/step)
			n=n+hist[i+b]
	gdal_array.numpy.take(lut,a,out=a)
	return a
#载入NDVI
start=time.perf_counter()
source=r"D:\Program Files\Python学习文档\samples\NDVI\ndvi.tif"
target=r"D:\Program Files\Python学习文档\samples\NDVI\ndvi_color.tif"
ndvi=gdal_array.LoadFile(source).astype(gdal_array.numpy.uint8)
#预解析NDVI
ndvi=stretch(ndvi)
rgb=gdal_array.numpy.zeros((3,len(ndvi),len(ndvi[0])),gdal_array.numpy.uint8)#创建3波段图片
#创建类
classes=[58,73,110,147,184,220,255]#设置NDVI区间上限值
lut=[[120, 69, 25], [255, 178, 74], [255, 237, 166], [173, 232, 94],
       [135, 181, 64], [3, 156, 0], [1, 100, 0]]
start=1
for i in range(len(classes)):
	mask=gdal_array.numpy.logical_and(start<=ndvi,ndvi<=classes[i])
	for j in range(len(lut[i])):
		rgb[j]=gdal_array.numpy.choose(mask,(rgb[j],lut[i][j]))
	start=classes[i]+1
output=gdal_array.SaveArray(rgb,target,format="GTIFF",prototype=source)
output=None
end=time.perf_counter()-start
print("程序运行时间{0}".format(end))




    
