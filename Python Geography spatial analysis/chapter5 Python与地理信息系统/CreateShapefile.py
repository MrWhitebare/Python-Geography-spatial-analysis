#CreateShapefile.py#创建shapefile文件
import shapefile
import utm
file_path = r"D:\Program Files\Python学习文档\samples\NYC_MUSEUMS_GEO\NYC_MUSEUMS_GEO.shp"
r = shapefile.Reader(file_path)
print(list(r.fields))
print(r.shapeTypeName)
# 版本修改，路径和类型都要在writer里面定义
w = shapefile.Writer(r"D:\Program Files\Python学习文档\samples\NYC_MUSEUMS_GEO\NYC_MUSEUMS_UTM.shp",shapeType=r.shapeType)
w.fields = list(r.fields[1:])
for rec in r.iterShapeRecords():  # 新版本已经删除了w.records
    print(*rec.record)
    w.record(*rec.record)
for sha in r.iterShapes():
    print(sha.points[0])
    # poitns返回shapefile文件坐标值
    lon, lat = sha.points[0]
    y, x, zone, band = utm.from_latlon(lat, lon)
    w.point(x, y)
w.close()