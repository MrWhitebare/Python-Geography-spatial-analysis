#GPX-Reporter.py 综合应用
from xml.dom import minidom
import json
import urllib.request
import urllib.parse
import urllib.error
import math
import time
import logging
import numpy
import srtm
import sys
from pygooglechart import SimpleLineChart
from pygooglechart import Axis
from PIL import ImageDraw,Image,ImageFilter,ImageEnhance
import fpdf
#Python日志模块
#提供了一种更高级的方式跟踪和记录程序运行状态
#日志级别，任何处于或者低于该级别的信息都会输出
level=logging.DEBUG
#日志信息格式化工具，本实例需要处理的日志信息是本地时间、日志时间和信息
formatter=logging.Formatter("%(asctime)s-%(name)s-%(message)s")
#创建一个日志对象
log=logging.getLogger("GPX-Reporter")
#配置日志级别
log.setLevel(level)
#在命令行中输出日志信息
console=logging.StreamHandler()
console.setLevel(level)
console.setFormatter(formatter)
log.addHandler(console)
def lonlattometer(lat,lon):#经纬度转化为m
    x=lon*20037508.34/180.0
    y=math.log(math.tan((90.0+lat)*math.pi/360.0))/(math.pi/180.0)
    y=y*20037508.34/180.0
    return (x,y)
def worldtopixel(x,y,width,height,bbox):
    #世界坐标转化为屏幕坐标
    minx,miny,maxx,maxy=bbox
    xdist=maxx-minx
    ydist=maxy-miny
    #x和y的缩放比例
    xratio=width/xdist
    yratio=height/ydist
    #计算x,y屏幕坐标
    px=width-((maxx-x)*xratio)
    py=(maxy-y)*yratio
    return int(px),int(py)
def get_utc_epoch(timestr):
    #将GPX文件中的时间格式转化为UTM格式
    #获取标准格式字符串
    utctime=time.strptime(timestr,'%Y-%m-%dT%H:%M:%S.%fZ')
    secs=int(time.mktime(utctime))
    return secs
def get_local_time(timestr,utcoffset=None):
    #将GPX文件中的时区转化为本地格式
    secs=get_utc_epoch(timestr)
    if not utcoffset:
        if time.localtime(secs).tm_isdst:
        #获取本时区偏差
            utcoffset=time.altzone
            pass
        else:
            utcoffset=time.timezone
            pass
        pass
    return time.localtime(secs-utcoffset)
def haversine(x1,y1,x2,y2):
    #计算距离的半矢正公式
    x_dist=math.radians(x1-x2)
    y_dist=math.radians(y1-y2)
    y1_rad=math.radians(y1)
    y2_rad=math.radians(y2)
    a=math.sin(y_dist/2)**2+math.sin(x_dist/2)**2*math.cos(y1_rad)*math.cos(y2_rad)
    c=2*math.asin(math.sqrt(a))
    #距离是以英里为单位，c*6371转化为km
    distance=c*(6371/1.609344) #Miles
    return distance
def wms(minx,miny,maxx,maxy,service,lyr,epsg,style,img,width,height):
    #从指定的数据源中获取WMS地图数据，然后另存为JPGE
    wms = service
    wms += "?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&"
    wms += "LAYERS={}".format(lyr)
    wms += "&STYLES={}&".format(style)
    wms += "SRS=EPSG:{}&".format(epsg)
    wms += "BBOX={}, {}, {}, {}&".format(minx, miny, maxx, maxy)
    wms += "WIDTH={}&".format(width)
    wms += "HEIGHT={}&".format(height)
    wms += "FORMAT=image/jpeg"
    wmsmap = urllib.request.urlopen(wms)
    with open(img + ".jpg", "wb") as f:
        f.write(wmsmap.read())
'''
解析GPX
'''
#在生成晕渲地形时需要使用numpy
deg2rad=3.141592653589793 / 180.0
rad2deg = 180.0 / 3.141592653589793
#程序变量
gpx=r"D:\Program Files\Python学习文档\samples\GPX\route.gpx"
#NOAA OSM WMS 服务
osm_WMS = "http://osm.woc.noaa.gov/mapcache"
#街道图层名称
osm_lyr="osm"
#底图图片另存
osm_img=r"D:\Program Files\Python学习文档\samples\GPX\basemap"
#EPSG代码【空间索引】
osm_epsg=3857
#可选的WMS参数
osm_style=""
#高程阴影参数
#日光方向
azimuth=315.0
#日光的方向
altitude=45.0
#高程缩放比例
z=5.0
#分辨率
scale=1.0
#无数据情况下输入值
no_data=0
#输出的高程影像图片
elv_img=r"D:\Program Files\Python学习文档\samples\GPX\elevation"
#SRTM最小高程值的RGB颜色值
min_clr=(255,255,255,0)
#最大高程值的RGB颜色值
max_clr=(0,0,0,0)
#无数据的颜色信息
zero_clr=(255,255,255,255)
#输出图片的像素高度和宽度
width=800
height=800
#解析GPX文件，并提取坐标信息
log.info("Parsing GPX file:{}".format(gpx))
xml=minidom.parse(gpx)
#获取所有"trkpt"元素
trkpts=xml.getElementsByTagName("trkpt")
#纬度列表
lats=list()
#经度列表
lons=list()
#高程列表
elvs=list()
#时间戳列表
times=list()
#解析出纬度、高程和时间信息
for trkpt in trkpts:
    #latitude
    lat=float(trkpt.attributes["lat"].value)
    #longtitude
    lon=float(trkpt.attributes["lon"].value)
    lats.append(lat)
    lons.append(lon)
    #elevation
    elv=trkpt.getElementsByTagName("ele")
    elv=elv[0].firstChild.data
    elv=float(elv)
    elvs.append(elv)
    #时间
    t=trkpt.getElementsByTagName("time")
    t=t[0].firstChild.data
    #转化本地时间 second
    t=get_local_time(t)
    times.append(t)
print(lats,lons,elvs,times)
'''
获取边框
'''
#查找路径的经纬度边界
minx=min(lons)
miny=min(lats)
maxx=max(lons)
maxy=max(lats)
#在GPX边框外部形成20%的缓冲区，使得地图图片裁切平滑
xdist=maxx-minx
ydist=maxy-miny
x20=xdist*0.2
y20=ydist*0.2
#每一侧扩展20%
minx-=x20
miny-=y20
maxx+=x20
maxy+=y20
#存储边界信息在一个边框中
bbox=[minx,miny,maxx,maxy]
#调用OSM WMS服务需要把边框信息的计量单位转化为m
#只需要下载以度为单位的SRTM文件、WMS规范中指出
mminx,mminy=lonlattometer(miny,minx)
mmaxx,mmaxy=lonlattometer(maxy,maxx)
'''
下载地图和高程影像
'''
#下载osm底图数据
log.info("Downloading basemap")
wms(mminx,mminy,mmaxx,mmaxy,osm_WMS,osm_lyr,osm_epsg,osm_style,osm_img,width,height)
#srtm.py下载器
log.info("Retrieving SRTM elevation data")
#SRTM模块会先访问缓存，然后按需下载
srt=srtm.get_data()
#获取图片并返回一个PIL图像对象
image=srt.get_image((width,height),(miny,maxy),(minx,maxx),300,zero_color=zero_clr,min_color=min_clr,max_color=max_clr)
#保存图片
image.save(elv_img+".jpg")
'''
创建地形
'''
#根据高程影像生成晕渲地形
log.info("Hillshading elevation data")
im=Image.open(elv_img+".jpg").convert("L")
dem=numpy.asarray(im)
#定义一个3*3的窗口遍历整个网格
window=list()
#x,y的分辨率
xres=(maxx-minx)/width
yres=(maxy-miny)/height
#创建窗体
for row in range(3):
    for column in range(3):
        window.append(dem[row:(row+dem.shape[0]-2),column:(column+dem.shape[1]-2)])
#处理每个单元格
x = ((z * window[0] + z * window[3] + z * window[3] + z * window[6]) -
     (z * window[2] + z * window[5] + z * window[5] + z * window[8])) \
     / (8.0 * xres * scale)

y = ((z * window[6] + z * window[7] + z * window[7] + z * window[8]) -
     (z * window[0] + z * window[1] + z * window[1] + z * window[2])) \
     / (8.0 * yres * scale)
#计算坡度
slope=90.0-numpy.arctan(numpy.sqrt(x*x+y*y))*rad2deg
#计算坡向
aspect=numpy.arctan2(x,y)
#计算地形阴影
shaded=numpy.sin(altitude*deg2rad)*numpy.sin(slope*deg2rad)+numpy.cos(altitude*deg2rad)*numpy.cos(slope*deg2rad)*numpy.cos((azimuth-90) \
       *deg2rad-aspect)
'''
创建地图
'''
#将 numpy数组转化为图片
relief=Image.fromarray(shaded).convert("L")
#转化图片使其平滑
for i in range(10):
    relief=relief.filter(ImageFilter.SMOOTH_MORE)
log.info("Creating map image")
#增加晕渲对比度
e=ImageEnhance.Contrast(relief)
relief=e.enhance(2)
#裁剪图片使其于SRTM图片匹配
base=Image.open(osm_img+".jpg").crop((0,0,width-2,height-2))
#在叠加图片前，增强对比度
e=ImageEnhance.Contrast(base)
base=e.enhance(1)
#将图片叠加在底图上,设置透明度为90%
topo=Image.blend(relief.convert("RGB"),base,0.9)
#绘制GPX跟踪轨迹，将坐标转化为屏幕坐标
points=[]
for x,y in zip(lons,lats):
    px,py=worldtopixel(x,y,width,height,bbox)
    points.append((px,py))
#裁剪图片大小和地图匹配
width-=2
height-=2
#生成一个透明图片绘制路径
track=Image.new('RGBA',(width,height))
track_draw=ImageDraw.Draw(track)
#路径线路红色，设置透明度50%
track_draw.line(points,fill=(255,0,0,127),width=4)
#将该图层作为一个mask叠加至底图
topo.paste(track,mask=track)
#在地图顶部绘制起始点位置朝向
topo_draw=ImageDraw.Draw(topo)
#起点
start_lon,start_lat=(lons[0],lats[0])
start_x,start_y=worldtopixel(start_lon,start_lat,width,height,bbox)
start_point=[start_x-10,start_y-10,start_x+10,start_y+10]
topo_draw.ellipse(start_point,fill="black",outline="white")
start_marker=[start_x-4,start_y-4,start_x+4,start_y+4]
topo_draw.ellipse(start_marker,fill="black",outline="white")
end_lon,end_lat=(lons[-1],lats[-1])
end_x,end_y=worldtopixel(end_lon,end_lat,width,height,bbox)
end_point=[end_x-10,end_y-10,end_x+10,end_y+10]
topo_draw.ellipse(end_point,fill="red",outline="black")
end_marker=[end_x-4,end_y-4,end_x+4,end_y+4]
topo_draw.ellipse(end_marker,fill="black",outline="white")
#保存topo地图
topo.save("{}_topo.jpg".format(osm_img))
'''
高程测量
'''
#使用谷歌的图表API构建高程剖面分析图表
log.info("Creating elevation profile chart")
chart=SimpleLineChart(600,300,y_range=[min(elvs),max(elvs)])
#根据API可知，用户需要3条不同颜色的数据线绘制图像
chart.add_data([min(elvs)]*2)
chart.add_data(elvs)
chart.add_data([min(elvs)]*2)
#黑色的线
chart.set_colours(['000000'])
#使用hex颜色值填充高程区域
chart.add_fill_range('80C65A',1,2)
#为高程值的最大值，中间值，最大值添加标签
elv_lables=int(round(min(elvs))),int(min(elvs)+((max(elvs)-min(elvs))/2)),int(round(max(elvs)))
#在坐标轴上声明标签
elv_lable=chart.set_axis_labels(Axis.LEFT,elv_lables)
#标记坐标轴
elv_text=chart.set_axis_labels(Axis.LEFT,["FEET"])
#设定标记和线的距离为30%
chart.set_axis_positions(elv_text,[30])
#计算路径点之间的距离
distances=[]
measurements=[]
coords=list(zip(lons,lats))#zip()函数 将对象中对应的元素打包成一个个元组
for i in range(len(coords)-1):#n-1使得序号不超过列表元素
    x1,y1=coords[i]
    x2,y2=coords[i+1]
    d=haversine(x1,y1,x2,y2)
    distances.append(d)
total=sum(distances)
distances.append(0)
j=-1
'''
距离测量
'''
#定位标记
for i in range(1,int(round(total))):
    mile=0
    while mile<i:
        j+=1
        mile+=distances[j]
    measurements.append((int(mile),j))
#为每个路径创建标签
positions=[]
miles=[]
for m,i in measurements:
    pos=((i*1.0)/len(elvs))*100
    positions.append(pos)
    miles.append(m)
#在x轴上为每个路径点设定相应的位置
miles_label=chart.set_axis_labels(Axis.BOTTOM,miles)
chart.set_axis_positions(miles_label,positions)
#标记x轴记录单位为英里
miles_text=chart.set_axis_labels(Axis.BOTTOM,["英里",])
chart.set_axis_positions(miles_text,[50,])
#保存图表
chart.download('{}_profile.png'.format(elv_img))
'''
获取气象数据
'''
log.info("Creating weather summary")
#获取气象数据的范围中心点
centx=minx+((maxx-minx)/2)
centy=miny+((maxy-miny)/2)
#API密钥
api_key="abd90bf31e334273990bf31e33d273b3"
#使用边框获取路劲的ID
#质心和地理查找api
geolookup_req = "http://api.wunderground.com/api/{}".format(api_key)
geolookup_req += "/geolookup/q/{},{}.json".format(centy, centx)
request = urllib.request.urlopen(geolookup_req)
geolookup_data = request.read().decode("utf-8")
json_geolook=r"D:\Program Files\Python学习文档\samples\GPX\geolookup.json"
#缓存查询结果备用
with open(json_geolook,"w") as f:
    f.write(geolookup_data)
js=json.loads(open(json_geolook).read())
loc=js["location"]
route_url=loc["requesturl"]
#获取最近的路径的时间戳，以便于查询历史天气
t=times[-1]
history_req = "http://api.wunderground.com/api/{}".format(api_key)
name_info = [t.tm_year, t.tm_mon, t.tm_mday, route_url.split(".")[0]]
history_req += "/history_{0}{1:02d}{2:02d}/q/{3}.json" .format(*name_info)
request = urllib.request.urlopen(history_req)
weather_data = request.read()
json_weather=r"D:\Program Files\Python学习文档\samples\GPX\weather.json"
#缓冲气象数据方便测试
with open(json_weather,"w") as f:
    f.write(weather_data.decode("utf-8"))
#获取气象数据
js=json.loads(open(json_weather).read())
history=js["history"]
#获取气象数据摘要，读取列表第一个元素
daily=history["dailysummary"][0]
#英制单位最高温度【℉】
#摄氏度公制："maxtempm"
maxtemp = daily["maxtempi"]
#最低温度 temperature
mintemp = daily["mintempi"]
#最大湿度 Maximum humidity
maxhum = daily["maxhumidity"]
#最小湿度
minhum = daily["minhumidity"]
#每英寸降水量(cm=precipm)
precip = daily["precipi"]
'''
生成pdf文件，肖像模式，计量单位英寸
字体大小（8.5*11）
'''
pdf=fpdf.FPDF("P","in ","Letter")
#添加一页报表
pdf.add_page()
#添加标题
pdf.set_font('Arial','B',20)
#水平方向上包含文本和空格元素
pdf.cell(6.25,1,'GPX 记录报告',border=0,align="C")
#竖直方向上空格元素
pdf.ln(h=1)
pdf.cell(1.75)
#创建一条水平线
pdf.cell(4,border="T")
pdf.ln(h=0)
pdf.set_font('Arial',style='B',size=14)
#创建路径地图
pdf.cell(w=1.2,h=1,txt="路线地图——Route Map",border=0,align="C")
pdf.image("{}_topo.jpg".format(osm_img),1,2,4,4)
pdf.ln(h=4.35)
#添加高程图表
pdf.set_font('Arial',style='B',size=14)
pdf.cell(w=1.2,h=1,txt='高程图表——Elevation Profile',border=0,align="C")
pdf.image("{}_profie.png".format(elv_img),1,6.5,4,2)
pdf.ln(h=2.4)
#添加天气摘要abstract
pdf.set_font('Arial',style='B',size=14)
pdf.cell(w=1.2,h=1,txt="Weather Summary",align="C")
pdf.ln(h=0.25)
pdf.set_font('Arial',style="",size=12)
pdf.cell(1.2, 1, "Min. Temp.: {}".format(mintemp), align="C")
pdf.cell(1.2, 1, "Max. Hum.: {}".format(maxhum), align="C")
pdf.ln(h=.25)
pdf.cell(1.2, 1, "Max. Temp.: {}".format(maxtemp), align="C")
pdf.cell(1.2, 1, "Precip.: {}".format(precip), align="C")
pdf.ln(h=.25)
pdf.cell(1.2, 1, "Min. Hum.: {}".format(minhum), align="C")
logo=r"D:\Program Files\Python学习文档\samples\GPX\logo.png"
pdf.image(logo,3.5,9,1.75,0.25)
#保存报表
log.info("Saving report pdf")
pdf_report=r"D:\Program Files\Python学习文档\samples\GPX\report.pdf"
pdf.output(pdf_report,'F')


