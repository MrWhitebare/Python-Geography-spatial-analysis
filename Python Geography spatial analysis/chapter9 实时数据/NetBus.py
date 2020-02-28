#NetBus.py
import urllib.request
import urllib.parse
import urllib.error
from xml.dom import minidom
#Nextbus API 命令模式
command="vehicleLocations"
#Nextbus代理查询
agency="lametro"
#公交线路查询
route="2"
#毫秒为单位以1970年为起点的世界标准时间，0代表最近15分钟
epoch="0"
#构造查询url
url = "http://webservices.nextbus.com"
#Web服务路径
url += "/service/publicXMLFeed?"
# 服务模式
url += "command=" + command
#代理
url += "&a=" + agency
url += "&r=" + route
url += "&t=" + epoch
#访问
feed = urllib.request.urlopen(url)
if feed:
    xml=minidom.parse(feed)
    #获取设备标签
    vehicles=xml.getElementsByTagName("vehicle")
    if vehicles:
        bus=vehicles.pop()
        att=bus.attributes
        print(att["lon"].value, ",", att["lat"].value)
    else:
        print("No vehicles found.")