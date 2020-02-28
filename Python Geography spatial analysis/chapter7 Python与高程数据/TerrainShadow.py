#TerrainShadow.py 创建地形阴影
import numpy
from linecache import getline
#数字高程
source=r"D:\Program Files\Python学习文档\samples\dem\dem.asc"
#坡度网格
slopegrid=r"D:\Program Files\Python学习文档\samples\dem\slope.asc"
#坡向网格
aspectgrid=r"D:\Program Files\Python学习文档\samples\dem\aspect.asc"
#输出晕渲地图文件
shadowdegrid=r"D:\Program Files\Python学习文档\samples\dem\relief.asc"

#高程阴影参数
#日光方位角
azimuth=315.0
#日光角度
altitude=45.0
#高程放大比例
z=1.0
#分辨率
scale=1.0
#设定NODATA值
NODATA=-9999

#转化必要参数
deg2rad=3.141592653589793/180.0#degree radian
rad2deg=180.0/3.141592653589793

#使用内置的模块循环解析头部信息
hdr=[getline(source,i) for i in range(1,7)]
values=[float(h.split(" ")[-1].strip()) for h in hdr]#去掉空格
cols,rows,lx,ly,cell,nd=values
xres=cell
yres=cell*-1

#加载dem数据
array=numpy.loadtxt(source,skiprows=6)
#排除围绕边框之外2像素NODATA数据
#同时设立3*3的窗口进行坡度计算
window=list()
for row in range(3):
    for column in range(3):
        window.append(array[row:(row+array.shape[0]-2),column:(column+array.shape[1]-2)])
#处理水平和竖直方向上3*3模块
x=((z*window[0]+z*window[3]+z*window[3]+z*window[6])-(z*window[2]+z*window[5]+z*window[5]+z*window[8]))/(8.0*xres*scale)
y=((z*window[6]+z*window[7]+z*window[7]+z*window[8])-(z*window[0]+z*window[1]+z*window[1]+z*window[2]))/(8.0*yres*scale)
#计算坡度
slope=90.0-numpy.arctan(numpy.sqrt(x*x+y*y))*rad2deg
#计算坡向
aspect=numpy.arctan2(x,y)
#计算晕渲阴影
shaded=numpy.sin(altitude*deg2rad)*numpy.sin(slope*deg2rad)+numpy.cos(altitude*deg2rad)*numpy.cos(slope*deg2rad)*numpy.cos((azimuth-90.0)* \
deg2rad-aspect)
#阴影放大比例,可选值区间为：0-1 or 0-255
shaded=shaded*255
#生成头部信息
header="ncols {}\n".format(shaded.shape[1])
header+="nrows {}\n".format(shaded.shape[0])
header+="xllcorner {}\n".format(lx+(cell*(cols-shaded.shape[1])))
header+="yllcorner {}\n".format(ly+(cell*(rows-shaded.shape[0])))
header+="cellsize {}\n".format(cell)
header+="NODATA_value {}\n".format(NODATA)
#为窗体设定NODATA值
for pane in window:
    slope[pane==nd]=NODATA
    aspect[pane==nd]=NODATA
    shaded[pane==nd]=NODATA
#输出文件
with open(slopegrid,"wb") as f:
    f.write(bytes(header,"UTF-8"))
    numpy.savetxt(f,slope,fmt="%4i")
with open(aspectgrid,"wb") as f:
    f.write(bytes(header,"UTF-8"))
    numpy.savetxt(f,aspect,fmt="%4i")
with open(shadowdegrid,"wb") as f:
    f.write(bytes(header,"UTF-8"))
    numpy.savetxt(f,shaded,fmt="%4i")
print("完成地形图的制作！")