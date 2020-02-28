#DotDensityMap.py 点密度人口地图
import shapefile
import random
import pngcanvas
'''
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
canvas=pngcanvas.PNGCanvas(iwidth,iheight)
#绘制红色点
canvas.color(255,0,0,0xff)
for d in dots:
    #将使用*d标记扩展(x,y)元组
    x,y=world2screen(inShp.bbox,iwidth,iheight,*d)
    canvas.filled_rectangle(x-1,y-1,x+1,y+1)
#绘制人口普查区域
canvas.color=(255,0,0,0xff)
for shape in inShp.iterShapes():
    pixels=list()
    for point in shape.points:
        pixel=world2screen(inShp.bbox,iwidth,iheight,*point)
        pixels.append(pixels)
    canvas.polyline(pixels)
#保存图片
img=open("D:\Program Files\Python学习文档\samples\GIS_CensusTract\DotDensity.png",'wb')
img.write(canvas.dump())
img.close()
print("点密度地图制作完成！")
'''
"""Create a dot-density thematic map"""
def point_in_poly(x, y, poly):
    """Boolean: is a point inside a polygon?"""
    # check if point is a vertex
    if (x, y) in poly:
        return True
    # check if point is on a boundary
    for i in range(len(poly)):
        p1 = None
        p2 = None
        if i == 0:
            p1 = poly[0]
            p2 = poly[1]
        else:
            p1 = poly[i-1]
            p2 = poly[i]
        if p1[1] == p2[1] and p1[1] == y and \
           x > min(p1[0], p2[0]) and x < max(p1[0], p2[0]):
            return True
    n = len(poly)
    inside = False

    p1x, p1y = poly[0]
    for i in range(n+1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x, p1y = p2x, p2y

    if inside:
        return True
    else:
        return False


def world2screen(bbox, w, h, x, y):
    """convert geospatial coordinates to pixels"""
    minx, miny, maxx, maxy = bbox
    xdist = maxx - minx
    ydist = maxy - miny
    xratio = w/xdist
    yratio = h/ydist
    px = int(w - ((maxx - x) * xratio))
    py = int((maxy - y) * yratio)
    return (px, py)

# Open the census shapefile
#inShp = shapefile.Reader("GIS_CensusTract_poly")
inShp=shapefile.Reader(r"D:\Program Files\Python学习文档\samples\GIS_CensusTract\GIS_CensusTract_poly.shp")
# Set the output image size
iwidth = 600
iheight = 400

# Get the index of the population field
pop_index = None
dots = []

for i, f in enumerate(inShp.fields):
    if f[0] == "POPULAT11":
        # Account for deletion flag
        pop_index = i-1

# Calculate the density and plot points
for sr in inShp.shapeRecords():
    population = sr.record[pop_index]
    # Density ratio - 1 dot per 100 people
    density = population / 100
    found = 0
    # Randomly distribute points until we
    # have the correct density
    while found < density:
        minx, miny, maxx, maxy = sr.shape.bbox
        x = random.uniform(minx, maxx)
        y = random.uniform(miny, maxy)
    if point_in_poly(x, y, sr.shape.points):
        dots.append((x, y))
        found += 1

# Set up the PNG output image
c = pngcanvas.PNGCanvas(iwidth, iheight)

# Draw the red dots
c.color = (255, 0, 0, 0xff)
for d in dots:
    x, y = world2screen(inShp.bbox, iwidth, iheight, *d)
    c.filled_rectangle(x-1, y-1, x+1, y+1)

# Draw the census tracts
c.color = (0, 0, 0, 0xff)
for s in inShp.iterShapes():
    pixels = []
    for p in s.points:
        pixel = world2screen(inShp.bbox, iwidth, iheight, *p)
        pixels.append(pixel)
    c.polyline(pixels)

# Save the image
img=open("D:\Program Files\Python学习文档\samples\GIS_CensusTract\DotDensity.png",'wb')
#img = open("DotDensity.png", "wb")
img.write(c.dump())
img.close()
print("点密度地图制作完成！")
