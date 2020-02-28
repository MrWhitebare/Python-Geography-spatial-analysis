# -*- coding: utf-8 -*-
#ContourMap.py 等高线地图
import shapefile
import pngcanvas
reader=shapefile.Reader(r"D:\Program Files\Python学习文档\samples\dem\contour.shp")
#世界坐标转化屏幕坐标
xdist=reader.bbox[2]-reader.bbox[0]
ydist=reader.bbox[3]-reader.bbox[1]
iwidth=800
iheight=600
xratio=iwidth/xdist
yratio=iheight/ydist
contours=list()
for shape in reader.iterShapes():
    for i in range(len(shape.parts)):
        pixels=[]
        pt=None
        if i<len(shape.parts)-1:
            pt=shape.points[shape.parts[i]:shape.parts[i+1]]
        else:
            pt=shape.points[shape.parts[i]:]
        for x,y in pt:
            px=int(iwidth-((reader.bbox[2]-x)*xratio))
            py=int((reader.bbox[3]-y)*yratio)
            pixels.append([px,py])
        contours.append(pixels)
canvas=pngcanvas.PNGCanvas(iwidth,iheight)
red=[0xff,0,0,0xff]
canvas.color=red
for c in contours:
    canvas.polyline(c)
output=r"D:\Program Files\Python学习文档\samples\dem\ContourMap.png"
with open(output,"wb") as f:
    f.write(canvas.dump())
print("绘制等高线地图！")



