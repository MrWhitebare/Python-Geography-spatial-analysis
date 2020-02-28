#CreateTriangulated.py 创建不规则三角网
import pickle
import os
import time
import math
import numpy
import shapefile
import voronoi
from laspy.file import File
source=r"D:\Program Files\Python学习文档\samples\clippedLAS\clippedLAS.las"
target=r"D:\Program Files\Python学习文档\samples\clippedLAS\triangles.shp"
#三角形数据
archive=r"D:\Program Files\Python学习文档\samples\clippedLAS\triangles.p"
#Pyshp文件
pyshp=r"D:\Program Files\Python学习文档\samples\clippedLAS\\triangles.p"
class Point:
    def __init__(self,x,y):
        self.px=x
        self.py=y
    def x(self):
        return self.px
    def y(self):
        return self.py
#三角形数组保存的三点索引元组用于点集查询
#voronoi模块载入归档文件创建三角面
triangles=None
if os.path.exists(archive):
    print("Loading triangle archive ...")
    file=open(archive,"rb")
    triangles=pickle.load(file)
    file.close()
    las=File(source,mode="r")
else:
    #打开LIDAR的LAS文件
    las=File(source,mode="r")
    points=[]
    print("Assembling points...")
    #读取点集
    for x,y in numpy.nditer((las.x,las.y)):
        points.append(Point(x,y))
    print("Composing triangles...")
    #Delaunay三角剖分
    triangles=voronoi.computeDelaunayTriangulation(points)
    file=open(archive,"wb")
    pickle.dump(triangles,file,protocol=2)
    file.close()
print("Creating shapefile...")
writer=None
if os.path.exists(pyshp):
    file=open(pyshp,"rb")
    writer=pickle.load(file)
    file.close()
else:
    # PolygonZ shapefile (x, y, z, m)
    writer = shapefile.Writer(target,shapefile.POLYGONZ)
    writer.field("X1", "C", "40")
    writer.field("X2", "C", "40")
    writer.field("X3", "C", "40")
    writer.field("Y1", "C", "40")
    writer.field("Y2", "C", "40")
    writer.field("Y3", "C", "40")
    writer.field("Z1", "C", "40")
    writer.field("Z2", "C", "40")
    writer.field("Z3", "C", "40")
    tris = len(triangles)
    # Loop through shapes and
    # track progress every 10 percent
    last_percent = 0
    for i in range(tris):
        t=triangles[i]
        percent=int((i/(tris*1.0))*100.0)
        if percent % 10.0 ==0 and percent >last_percent:
            last_percent=percent
            print("{0} % done - Shape {1}/{2} at {3}".format(percent, i, tris,
                                                         time.asctime()))
            part = []
            x1 = las.x[t[0]]
            y1 = las.y[t[0]]
            z1 = las.z[t[0]]
            x2 = las.x[t[1]]
            y2 = las.y[t[1]]
            z2 = las.z[t[1]]
            x3 = las.x[t[2]]
            y3 = las.y[t[2]]
            z3 = las.z[t[2]]
            # Check segments for large triangles
            # along the convex hull which is an common
            # artificat in Delaunay triangulation
            max = 3
            if math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) > max:
                continue
            if math.sqrt((x3 - x2) ** 2 + (y3 - y2) ** 2) > max:
                continue
            if math.sqrt((x3 - x1) ** 2 + (y3 - y1) ** 2) > max:
                continue
            part.append([x1, y1, z1, 0])
            part.append([x2, y2, z2, 0])
            part.append([x3, y3, z3, 0])
            writer.poly(parts=[part])
            writer.record(x1, x2, x3, y1, y2, y3, z1, z2, z3)
print("Saving shapefile")
file=open(pyshp,"wb")
pickle.dump(writer,file,protocol=2)
file.close()
print("Done...")