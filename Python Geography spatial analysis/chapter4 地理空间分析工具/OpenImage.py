# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 19:28:54 2020

@author: 立文
"""
#OpenImage.py 使用GDAL库打开栅格数据
from osgeo import gdal
from osgeo import gdal_array
raster=gdal.Open(r"D:\Program Files\Python学习文档\samples\SatImage\SatImage.tif")
print(raster.RasterCount)
print(raster.RasterXSize)
print(raster.RasterYSize)
srcArray=gdal_array.LoadFile(r"D:\Program Files\Python学习文档\samples\SatImage\SatImage.tif")
band1=srcArray[0]
gdal_array.SaveArray(band1,r"D:\Program Files\Python学习文档\samples\band1.jpg",format="JPEG")