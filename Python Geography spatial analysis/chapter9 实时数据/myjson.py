# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 16:18:17 2020

@author: 立文
"""
#myjson.py 区域报告
import folium
import os

'''创建Map对象'''
m = folium.Map(location=[29.488869,106.571034],
              zoom_start=14)

'''查看m的类型'''
print(m.__class__)
