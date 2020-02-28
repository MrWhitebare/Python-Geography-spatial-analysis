#PhotoGPS.py 照片地理定位
import glob
from PIL import Image
from PIL.ExifTags import TAGS
import shapefile
import os
def exif(img):#提取exif数据
    exif_data={}
    try:
        i = Image.open(img)
        tags = i._getexif()
        for tag, value in tags.items():
            decoded = TAGS.get(tag, tag)
            exif_data[decoded] = value
    except:
        pass
    return exif_data
def dmstodd(d,m,s,i):#转化度、分、秒为十进制degree minute second
    sec=float((m*60)+s)
    dec=float(sec/3600)
    deg=float(d+dec)
    if i.upper()=='W':
        deg=deg*-1
    elif i.upper()=='S':
        deg=dec*-1
    return float(deg)
def gps(exif):#从exif中获取GPS数据
    lat=None
    lon=None
    if exif['GPSInfo']:
        #纬度latitude
        coords=exif['GPSInfo']
        i=coords[1]
        d=coords[2][0][0]
        m=coords[2][1][0]
        s=coords[2][2][0]
        lat=dmstodd(d,m,s,i)
        #longtitude
        i=coords[3]
        d=coords[4][0][0]
        m=coords[4][1][0]
        s=coords[4][2][0]
        lon=dmstodd(d,m,s,i)
    return lat,lon
photos={}#dict 字典类型
photo_dir=r"D:\Program Files\Python学习文档\samples\photos\*"
files=glob.glob(photo_dir)
for f in files:
    e=exif(f)
    print(e)
    lat,lon=gps(e)
    photos[f]=[lon,lat]
print(photos)
target=r"D:\Program Files\Python学习文档\samples\photos\gps.shp"
w=shapefile.Writer(target,shapefile.POINT)
w.field("NAME","C",80)
for f,coords in photos.items():
    w.point(*coords)
    w.record("photos")
w.close()


