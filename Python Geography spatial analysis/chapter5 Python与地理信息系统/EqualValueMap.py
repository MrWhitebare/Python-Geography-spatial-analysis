#EqualValueMap.py 等值区域图
import shapefile
from PIL import Image,ImageDraw
import math
def world2screen(bbox,width,heigth,x,y):
    minx,miny,maxx,maxy=bbox
    xdist=maxx-minx
    ydist=maxy-miny
    xratio=width/xdist
    yratio=heigth/ydist
    px=int(width-((maxx-x)*xratio))
    py=int((maxy-y)*yratio)
    return (px,py)
inShp=shapefile.Reader(r"D:\Program Files\Python学习文档\samples\GIS_CensusTract\GIS_CensusTract_poly.shp")
iwidth=600
iheight=400
#初始化PIL的Image对象
img=Image.new("RGB",(iwidth,iheight),(255,255,255))
#初始化PIL的Draw模块用于填充多边形
draw=ImageDraw.Draw(img)
#获取人口和区域索引
pop_index=None
area_index=None
#绘制人口普查区域阴影
for i,f in enumerate(inShp.fields):
    if f[0]=="POPULAT11":
        #声明删除标记
        pop_index=i-1#20
    elif f[0]=="AREASQKM":
        area_index=i-1#18
#绘制多边形
for sr in inShp.iterShapeRecords():
    density=sr.record[pop_index]/sr.record[area_index]
    #Weigth 用来配置人口相关的颜色深度
    weight=min(math.sqrt(density/80),1)*50
    R=int(205-weight)
    G=int(215-weight)
    B=int(245-weight)
    pixels=list()
    for x,y in sr.shape.points:
        (px,py)=world2screen(inShp.bbox,iwidth,iheight,x,y)
        pixels.append((px,py))
    draw.polygon(pixels,outline=(255,255,255),fill=(R,G,B))
img.save(r"D:\Program Files\Python学习文档\samples\GIS_CensusTract\EqualValueMap.png")