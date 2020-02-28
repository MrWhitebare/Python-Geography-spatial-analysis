#OpenStreetMap.py Netbus地址映射
import urllib.request
import urllib.parse
import urllib.error
from xml.dom import minidom
import time
def nextbus(a,r,c="vehicleLocations",e=0):
    #使用NextBus API(NextBus API，nbapi)
    #返回选定公交线路的经纬度坐标。
    #参数：a=代理, r=线路, c=命令, e=时间，开始记录时间的起始值,
    #0 = 返回最近15分钟之内的记录信息
    nbapi = "http://webservices.nextbus.com"
    nbapi += "/service/publicXMLFeed?"
    nbapi += "command={}&a={}&r={}&t={}".format(c, a, r, e)
    xml = minidom.parse(urllib.request.urlopen(nbapi))
    #如果有多个车辆只返回第一条记录
    bus=xml.getElementsByTagName("vehicle")[0]
    if bus:
        at=bus.attributes
        return (at["lat"].value,at["lon"].value)
    else:
        return (False,False)
def nextmap(a,r,mapimg):
    #使用OpenstreetMap静态地图API 在地图上绘制nextbus的位置信息并将其保存
    #获取最近公共汽车经纬度坐标
    lat,lon=nextbus(a,r)
    if not lat:
        return False
    #基础URL地址+服务路径
    osmapi="http://staticmap.openstreetmap.de/staticmap.php?"
    #地图中心点位置与公交车所在位置保持一致
    osmapi+="center={},{}&".format(lat, lon)
    #设置缩放级别【1-18级之间】
    osmapi+="zoom=14&"
    #设置地图图片尺寸
    osmapi+="&size=1500x1000&"
    #渲染图片样式为mapnik
    osmapi+="maptype=mapnik&"
    #使用红色图标记录表示公交车
    osmapi+="markers={},{},red-pushpin".format(lat, lon)
    img=urllib.request.urlopen(osmapi)
    #保存地图快照
    with open("{}.png".format(mapimg),"wb") as f:
        f.write(img.read())
    return True
#Nextbus API代理和公交线路变量
agency="lametro"
route="2"
#为地图指定名称，设置保存格式
nextimg=r"D:\Program Files\Python学习文档\samples\nextmap"
#执行次数
requests=3
#执行请求频率second
freq=5
for i in range(requests):
    success=nextmap(agency,route,nextimg)
    if not success:
        print("No data avilable")
        continue
    print("Saved map{} at {}".format(i,time.asctime()))
    time.sleep(freq)

