#GridLidar.py 使用LIDAR创建格网
from laspy.file import File
import numpy
#LAS源文件
source=r"D:\Program Files\Python学习文档\samples\lidar\lidar.las"
#输出ASCII DEM文件
target=r"D:\Program Files\Python学习文档\samples\lidar\lidar.asc"
#网格尺寸
cell=1
#输出DEM的NODATA值
NODATA=0
#打开lidar的LAS文件
las=File(source,mode="r")
#xyz的极值
min=las.header.min
max=las.header.max
#获取x轴的距离m
xdist=max[0]-min[0]
#获取y轴的距离m
ydist=max[1]-min[1]
#网格的列数
columns=int(xdist)//cell
#网格的行数
rows=int(ydist)//cell
columns+=1
rows+=1
#统计平均高程值
count=numpy.zeros((rows,columns)).astype(numpy.float32)
#平均高程值
zsum=numpy.zeros((rows,columns)).astype(numpy.float32)
#y分辨率是负数
ycell=-1*cell

#将x,y的值投影到网格
projx=(las.x-min[0])/cell
projy=(las.y-min[1])/ycell

#将数据转化为整数并且提取部分用作索引
ix=projx.astype(numpy.int32)
iy=projy.astype(numpy.int32)

#遍历x,y,z数据，将其添加到网格形状中并添加平均值
for x,y,z in numpy.nditer([ix,iy,las.z]):
    count[y,x]+=1
    zsum[y,x]+=z
#修改0值为1避免numpy报错以及数组出现NaN值
nonzero=numpy.where(count>0,count,1)
#平均化z值
zavg=zsum/nonzero

#将0值插入数组中避免网格出缺陷
mean=numpy.ones((rows,columns))*numpy.mean(zavg)
left=numpy.roll(zavg,-1,1)
lavg=numpy.where(left>0,left,mean)
right=numpy.roll(zavg,1,1)
ravg=numpy.where(right>0,right,mean)
interpolate=(lavg+ravg)/2
fill=numpy.where(zavg>0,zavg,interpolate)

#创建ASCII　ＤＥＭ的头部信息
header = "ncols        {}\n".format(fill.shape[1])
header += "nrows        {}\n".format(fill.shape[0])
header += "xllcorner    {}\n".format(min[0])
header += "yllcorner    {}\n".format(min[1])
header += "cellsize     {}\n".format(cell)
header += "NODATA_value      {}\n".format(NODATA)

with open(target,"wb") as f:
    f.write(bytes(header,'UTF-8'))
    numpy.savetxt(f,fill,fmt="%1.2f")
print("输出DEM")

