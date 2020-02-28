# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 16:48:32 2020

@author: 立文
"""
#DynamicSelect.py 自动提取岛屿特征
from osgeo import gdal,ogr,osr
#阈值化之后的栅格文件
src=r"D:\Program Files\Python学习文档\samples\islands\islands_classified.tiff"
target=r"D:\Program Files\Python学习文档\samples\islands\extract2.shp"
#图层名称
tatLayer="extract"
srcDocs=gdal.Open(src)
#获取第一个波段
band=srcDocs.GetRasterBand(1)
#让gdal库使用该波段作为掩模层
mask=band
#创建Shapefile文件
driver=ogr.GetDriverByName("ESRI Shapefile")
shp=driver.CreateDataSource(target)
#拷贝空间索引
srs=osr.SpatialReference()
srs.ImportFromWkt(srcDocs.GetProjectionRef())
layer=shp.CreateLayer(tatLayer,srs=srs)
#创建dbf文件
fd=ogr.FieldDefn("DN",ogr.OFTInteger)
layer.CreateField(fd)
dst_field=0
#从图片中自动提取
extract=gdal.Polygonize(band,mask,layer,dst_field,[],None)


