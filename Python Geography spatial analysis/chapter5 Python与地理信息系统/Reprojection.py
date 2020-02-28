# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 18:54:22 2020

@author: 立文
"""
from osgeo import ogr
from osgeo import osr
import os
import shutil
srcName=r"D:\Program Files\Python学习文档\samples\NYC_MUSEUMS_LAMBERT\NYC_MUSEUMS_LAMBERT.shp"
tgtName=r"D:\Program Files\Python学习文档\samples\NYC_MUSEUMS_LAMBERT\NYC_MUSEUMS_GEO.shp"
tgt_spatRef=osr.SpatialReference()
tgt_spatRef.ImportFromEPSG(4326)#WGS84
driver=ogr.GetDriverByName("ESRI Shapefile")
src=driver.Open(srcName,0)#打开资源
srcLyr=src.GetLayer()
src_spatRef=srcLyr.GetSpatialRef()
if os.path.exists(tgtName):
    driver.DeleteDataSource(tgtName)
tgt=driver.CreateDataSource(tgtName)
lyrName=os.path.splitext(tgtName)[0]
#os.path.splitext()将文件名和扩展名分开[返回以元组形式分开，选用第一项]
#('D:\\Program Files\\Python学习文档\\samples\\NYC_MUSEUMS_LAMBERT\\NYC_MUSEUMS_GEO', '.shp')
#使用WKB格式声明几何图形
tgtLyr=tgt.CreateLayer(lyrName,geom_type=ogr.wkbPoint)
featDef=srcLyr.GetLayerDefn()
trans=osr.CoordinateTransformation(src_spatRef,tgt_spatRef)
srcFeat=srcLyr.GetNextFeature()
while srcFeat:
    geom=srcFeat.GetGeometryRef()#投影
    geom.Transform(trans)
    feature=ogr.Feature(featDef)
    feature.SetGeometry(geom)
    tgtLyr.CreateFeature(feature)
    feature.Destroy()
    srcFeat.Destroy()
    srcFeat=srcLyr.GetNextFeature()
src.Destroy()
tgt.Destroy()
#为导出的投影文件将几何图形转化为Esri的WKT格式
tgt_spatRef.MorphToESRI()
prj=open(lyrName+".prj","w")
prj.write(tgt_spatRef.ExportToWkt())
prj.close()
srcDbf=os.path.splitext(srcName)[0]+".dbf"
tgtDbf=lyrName+".dbf"
shutil.copyfile(srcDbf,tgtDbf)















