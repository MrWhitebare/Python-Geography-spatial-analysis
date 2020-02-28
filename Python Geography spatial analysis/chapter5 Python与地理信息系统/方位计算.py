# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 17:31:06 2020

@author: 立文
"""
from math import atan2,cos,sin,degrees
lon1=-90.21
lat1=32.31
lon2=-88.95
lat2=30.43
angle=atan2(cos(lat1)*sin(lat2)-sin(lat1)*cos(lat2)*cos(lon2-lon1),sin(lon2-lon1)*cos(lat2))
bearing=(degrees(angle)+360)%360
print(bearing)
