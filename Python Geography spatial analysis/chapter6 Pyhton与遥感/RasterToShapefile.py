# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 12:05:36 2020

@author: 立文
"""
#RasterToShapefile.py 栅格矢量化
from osgeo import gdal,ogr,osr
import os
def polygonize(rasterTemp,outShp):
    sourceRaster = gdal.Open(rasterTemp)#打开遥感图像
    band = sourceRaster.GetRasterBand(2)#选择波段2
    driver = ogr.GetDriverByName("ESRI Shapefile")
    # If shapefile already exist, delete it
    if os.path.exists(outShp):
        driver.DeleteDataSource(outShp)

    outDatasource = driver.CreateDataSource(outShp)            
    # get proj from raster            
    srs = osr.SpatialReference()
    srs.ImportFromWkt( sourceRaster.GetProjectionRef() )
    # create layer with proj
    outLayer = outDatasource.CreateLayer(outShp,srs)
    # Add class column (1,2...) to shapefile

    newField = ogr.FieldDefn('Class', ogr.OFTInteger)
    outLayer.CreateField(newField)

    gdal.Polygonize(band, None,outLayer, 0,[],callback=None)  

    outDatasource.Destroy()
    sourceRaster=None
    band=None


    ioShpFile = ogr.Open(outShp, update = 1)
    lyr = ioShpFile.GetLayerByIndex(0)
    lyr.ResetReading()    
    for i in lyr:
        lyr.SetFeature(i)
        # if area is less than inMinSize or if it isn't forest, remove polygon 
        if i.GetField('Class')!=1:
            lyr.DeleteFeature(i.GetFID())        
    ioShpFile.Destroy()
    return outShp
raster=r"D:\Program Files\Python学习文档\samples\islands\islands_classified.tiff"
outShp=r"D:\Program Files\Python学习文档\samples\islands\band3.shp"
polygon=polygonize(raster,outShp)
if polygon!=None:    
    print("栅格矢量化成功！")
            