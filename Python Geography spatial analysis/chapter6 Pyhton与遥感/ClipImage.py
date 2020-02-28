# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 12:41:16 2020

@author: 立文
"""
#ClipImage.py 图像裁切
import shapefile
from osgeo import gdal,gdal_array
from PIL import Image,ImageDraw
def ImageToArray(i):
    #把一个Python影像库的数组转化为一个Gdal_array图片
    a=gdal_array.numpy.fromstring(i.tobytes(),'b')
    a.shape=i.im.size[1], i.im.size[0]
    return a
def World2Pixel(geoMatrix,x,y):
    #使用gdal库的geomatrix对象【gdal.GetGeoTransform()】计算地理坐标的像素位置
    ulX=geoMatrix[0]
    ulY=geoMatrix[3]
    xDist=geoMatrix[1]
    yDist=geoMatrix[5]
    pixel=int((x-ulX)/xDist)
    line=int((ulY-y)/abs(yDist))
    return (pixel,line)
raster=r"D:\Program Files\Python学习文档\samples\FalseColor\stretched.tif"
shp=r"D:\Program Files\Python学习文档\samples\hancock\hancock.shp"
output=r"D:\Program Files\Python学习文档\samples\FalseColor\clip3.tif"
srcArray=gdal_array.LoadFile(raster)
#同时载入gdal库的图片从而获取geotransform（世界文件）
srcImage=gdal.Open(raster)
geoTrans=srcImage.GetGeoTransform()
reader=shapefile.Reader(shp)
#将图层扩张转化为图片像素坐标
minX,minY,maxX,maxY=reader.bbox
ulX,ulY=World2Pixel(geoTrans,minX,maxY)
lrX,lrY=World2Pixel(geoTrans,maxX,minY)
#计算新图片的像素尺寸
pxWidth=int(lrX-ulX)
pxHeight=int(lrY-ulY)
clip=srcArray[:,ulY:lrY,ulX:lrX]
#为图片创建一个新的geomatrix对象以便附加地理参考数据
geoTrans=list(geoTrans)
geoTrans[0]=minX
geoTrans[3]=maxY
#在一个空白的8字节黑白遮罩图片上把点映射为像素绘制县市
#边界线
pixels=[]
for p in reader.shape(0).points:
    pixels.append(World2Pixel(geoTrans,p[0],p[1]))
rasterPoly=Image.new("L",(pxWidth,pxHeight),1)
#使用PIL创建一个空白图片用于绘制多边形
rasterize=ImageDraw.Draw(rasterPoly)
rasterize.polygon(pixels,0)
#将PIL图片转化为Numpy数组
mask=ImageToArray(rasterPoly)
#根据创建图片对图片裁剪
clip=gdal_array.numpy.choose(mask,(clip,0)).astype(gdal_array.numpy.uint8)#无符号的八位
#保存图片
output =gdal_array.SaveArray(clip,output,format="GTiff",prototype=raster)
output=None

    



