#CreateFrameWork.py 建立框架
import gdal
from osgeo import gdal
from osgeo import gdal_array
from osgeo import ogr
from PIL import Image,ImageDraw
def ImageToArray(i):
    a=gdal_array.numpy.fromstring(i.tobytes(),'b')
    a.shape=i.im.size[1],i.im.size[0]
    return a
def WorldtoPixel(geoMatrix,x,y):
    #使用gdal的geoMatrix方法，计算地理坐标对应的像素坐标
    ulx=geoMatrix[0]
    uly=geoMatrix[3]
    xDist=geoMatrix[1]
    yDist=geoMatrix[5]
    pixel=int((x-ulx)/xDist)
    line=int((uly-y)/abs(yDist))
    return (pixel,line)
def Copy_Geo(array,prototype=None,xoffset=0,yoffset=0):
    #从原数据集拷贝数组
    ds=gdal.Open(gdal_array.GetArrayFilename(array))
    prototype=gdal.Open(prototype)
    gdal_array.CopyDatasetInfo(prototype, ds, xoff=xoffset, yoff=yoffset)
    return ds
source=r"D:\Landset\landset.tif"
target=r"D:\Landset\NDVI.tif"
srcArray=gdal_array.LoadFile(source)
#打开源数据获取地理参考
srcImage=gdal.Open(source)
geoTrans=srcImage.GetGeoTransform()
#红外和近红外波段
red=srcArray[2]
nearred=srcArray[3]
#使用农田边界shapefile文件裁剪边框之外的区域
#根据区域边界Shapefile文件创建OGR图层
shp=r"D:\Landset\Clip.shp"
field=ogr.Open(shp)
lyr=field.GetLayer("Clip")
poly=lyr.GetNextFeature()
#图层坐标转化为图片像素坐标
minX,maxX,minY,maxY=lyr.GetExtent()
ulX,ulY=WorldtoPixel(geoTrans,minX,maxY)
lrX,lrY=WorldtoPixel(geoTrans,maxX,minY)
#计算新图像的像素尺寸
pxWidth=int(lrX-ulX)
pxHeight=int(lrY-ulY)
#为裁剪层创建一张合适空白图片
clipped=gdal_array.numpy.zeros((3,pxHeight,pxWidth),gdal_array.numpy.uint8)
#裁剪红光和近红外波段到新的数据
redClip=red[ulY:lrY,ulX:lrX]
nearredClip=nearred[ulY:lrY,ulX:lrX]
#为图片创建一个新的geomatrix对象
geoTrans=list(geoTrans)
geoTrans[0]=minX
geoTrans[3]=maxY
#在新建图片上把点映射为像素用于绘制区域边界
points=list()
pixels=list()
#获取多边形几何图形
geom=poly.GetGeometryRef()
pts=geom.GetGeometryRef(0)
for p in range(pts.GetPointCount()):
    points.append((pts.GetX(p),pts.GetY(p)))
for p in points:
    pixels.append(WorldtoPixel(geoTrans,p[0],p[1]))
#用‘L’模式创建一个栅格多边形图片
rasterPoly=Image.new("L",(pxWidth,pxHeight),1)#1 white
rasterize=ImageDraw.Draw(rasterPoly)
#将像素点转化为多边形 
rasterize.polygon(pixels,0)#0 black
mask=ImageToArray(rasterPoly)
redClip=gdal_array.numpy.choose(mask,(redClip,0)).astype(gdal_array.numpy.uint8)
nearredClip=gdal_array.numpy.choose(mask,(nearredClip,0)).astype(gdal_array.numpy.uint8)
#忽略裁剪过程中遇到的NaN值
gdal_array.numpy.seterr(all="ignore")
ndvi=1.0*((nearredClip-redClip)/(nearredClip+redClip+1.0))
ndvi=gdal_array.numpy.nan_to_num(ndvi)
#saveas
gdal_array.SaveArray(ndvi,target, format="GTiff", prototype=srcImage)
update = gdal.Open(target, 1)
update.SetGeoTransform(list(geoTrans))
update.GetRasterBand(1).SetNoDataValue(0.0)
update = None
print("NDVI数据创建成功！")