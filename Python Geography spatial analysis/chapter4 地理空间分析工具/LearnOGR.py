# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 15:49:30 2020

@author: 立文
"""
#LearnOGR.py
from osgeo import ogr
shape=ogr.Open("D:/Program Files/arcpy_project/Data/point/point.shp")
layer=shape.GetLayer()
for feature in layer:
    geometry=feature.GetGeometryRef()
    print(geometry.GetX(),geometry.GetY(),feature.GetField("FIRST_FLD"))


