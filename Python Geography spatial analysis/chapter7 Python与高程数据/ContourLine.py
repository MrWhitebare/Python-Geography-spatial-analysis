# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 13:19:26 2020

@author: 立文
"""
#ContourLine.py 等高线
import gdal
import ogr
#高程DEM
source=r"D:\Program Files\Python学习文档\samples\dem\dem.asc"
#输出shapefile文件
target=r"D:\Program Files\Python学习文档\samples\dem\contour.shp"

ogr_driver=ogr.GetDriverByName("ESRI Shapefile")
ogr_ds=ogr_driver.CreateDataSource(target)
ogr_lyr=ogr_ds.CreateLayer(target,geom_type=ogr.wkbLineString25D)
#ogr.wkbLineString25D是包含几何高程值z的类型代码
field_defn=ogr.FieldDefn("ELEV",ogr.OFTReal)
ogr_lyr.CreateField(field_defn)
# gdal.ContourGenerate() arguments
# Band srcBand,
# double contourInterval,
# double contourBase,
# double[] fixedLevelCount,
# int useNoData,
# double noDataValue,
# Layer dstLayer,
# int idField,
# int elevField
ds=gdal.Open(source)
gdal.ContourGenerate(ds.GetRasterBand(1),400,10,[],0,0,ogr_lyr,0,1)
ogr_ds=None
print("输出等高线！")