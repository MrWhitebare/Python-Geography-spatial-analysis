#DotDensityMap.py 点密度人口地图
import shapefile
import random
import pngcanvas
from PIL import Image,ImageDraw
def point_in_poly(x,y,poly):
    #判断点是否是顶点
    if (x,y) in poly:
        return True
    #判断点是否在边框上
    for i in range(len(poly)):
        p1=None
        p2=None
        if i==0:
            p1=poly[0]
            p2=poly[1]
        else:
            p1=poly[i-1]
            p2=poly[i]
        if p1[1]==p2[1] and p1[1] ==y and x > min(p1[0],p2[0]) and x < max(p1[0],p2[0]):
            return True
    n=len(poly)
    inside=False
    p1x,p1y=poly[0]
    for i in range(n+1):
        p2x,p2y=poly[i%n]
        if y>min(p1y,p2y):
            if y<=max(p1x,p2x):
                if x<=max(p1x,p2x):
                    if p1y !=p2y:
                        xints=(y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x ==p2x or x<=xints:
                        inside=not inside
        p1x,p1y=p2x,p2y
    if inside:
        return True
    else:
        return False
def world2screen(bbox,width,height,x,y):
    #地理坐标转化屏幕坐标
    minx,miny,maxx,maxy=bbox
    xdist=maxx-minx
    ydist=maxy-miny
    xratio=width/xdist
    yratio=height/ydist
    px=int(width-((maxx-x)*xratio))
    py=int((maxy-y)*yratio)
    return (px,py)
#打开人口普查数据
inShp=shapefile.Reader(r"D:\Program Files\Python学习文档\samples\GIS_CensusTract\GIS_CensusTract_poly.shp")
#设置输出地图尺寸
iwidth=600
iheight=400
#获取人口记录索引
pop_index=None
dots=[]
for i,f in enumerate(inShp.fields):
    #i 序号 f 字段
    if f[0] =="POPULAT11":
        #声明删除标记
        pop_index=i-1
#计算点密度并绘制相关点
for shape in inShp.iterShapeRecords():
    population=shape.record[pop_index]#获取人口数值
    #密度比率density rate 一个点代表100人
    density=population/100
    found=0
    #随机绘制点，直到密度达到指定比率
    while found < density:
        minx,miny,maxx,maxy=shape.shape.bbox
        x=random.uniform(minx,maxx)
        y=random.uniform(miny,maxy)
        if point_in_poly(x,y,shape.shape.points):
            dots.append((x,y))#点的坐标
            found+=1
#为输出PNG图片准备
#canvas=pngcanvas.PNGCanvas(iwidth,iheight)
#绘制红色点
#canvas.color(255,0,0,0xff)
#初始化PIL的Image对象
img=Image.new("RGB",(iwidth,iheight),(255,0,0))
#初始化PIL的Draw模块用于填充多边形
draw=ImageDraw.Draw(img)
for d in dots:
    #将使用*d标记扩展(x,y)元组
    point=list()
    x,y=world2screen(inShp.bbox,iwidth,iheight,*d)
    point.append((x,y))
    #canvas.filled_rectangle(x-1,y-1,x+1,y+1)
    draw.point(point)
#绘制人口普查区域
#canvas.color=(255,0,0,0xff)
for shape in inShp.iterShapes():
    pixels=list()
    for point in shape.points:
        pixel=world2screen(inShp.bbox,iwidth,iheight,*point)
        pixels.append(pixels)
    #canvas.polyline(pixels)
    draw.polygon(pixels,outline="rgb(203,196,190)",fill="rgb(198,204,189)")
#保存图片
img.save(r"D:\Program Files\Python学习文档\samples\GIS_CensusTract\DotDensity.png")
#img=open("D:\Program Files\Python学习文档\samples\GIS_CensusTract\DotDensity.png",'wb')
#img.write(canvas.dump())
#img.close()
print("点密度地图制作完成！")


