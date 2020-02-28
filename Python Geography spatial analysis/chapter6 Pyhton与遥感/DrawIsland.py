# -*- coding: utf-8 -*-
#DrawIsland.py 绘制岛屿
import shapefile
import pngcanvas
reader=shapefile.Reader(r"D:\Program Files\Python学习文档\samples\islands\extract.shp")
xdist=reader.bbox[2]-reader.bbox[0]#maxx-minx
ydist=reader.bbox[3]-reader.bbox[1]#maxy-miny
iwidth=800
iheight=600
xratio=iwidth/xdist
yratio=iheight/ydist
polygons=[]
for shape in reader.iterShapes():
    pixels=list()
    pt=None
    for i in range(len(shape.parts)):
        if i<len(shape.parts)-1:
            pt=shape.points[shape.parts[i]:shape.parts[i+1]]
        else:
            pt=shape.points[shape.parts[i]:]
        for x,y in pt:
            px=int(iwidth-(reader.bbox[2]-x)*xratio)
            py=int((reader.bbox[3]-y)*yratio)
            pixels.append([px,py])
    polygons.append(pixels)
    canvas=pngcanvas.PNGCanvas(iwidth,iheight)
    for p in polygons:
        canvas.polyline(p)
file=open(r"D:\Program Files\Python学习文档\samples\islands\extract.png","wb")
file.write(canvas.dump())
file.close()
print("图形绘制完成！")
