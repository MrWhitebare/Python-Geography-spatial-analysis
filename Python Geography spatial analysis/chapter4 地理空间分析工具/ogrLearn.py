# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from osgeo import ogr
#注意文件路径，使用反斜杠或者加“r”
shape=ogr.Open("D:/Program Files/arcpy_project/Data/polygon/polygon.shp")
layer=shape.GetLayer()
feature=layer.GetNextFeature()
geom=feature.GetGeometryRef()
wkt=geom.ExportToWkt()
poly=ogr.CreateGeometryFromWkt(wkt)
poly.GetEnvelope()
