import shapefile
import utm
reader=shapefile.Reader(r"D:\Program Files\Python学习文档\samples\footprints\footprints_se.shp")
writer=shapefile.Writer(r"D:\Program Files\Python学习文档\samples\footprints\footprints_split.shp",reader.shapeType)
writer.fields=list(reader.fields[1:])
for shapeRecord in reader.iterShapeRecords():
    utmPoints=[]
    for point in shapeRecord.shape.points:
        x,y,band,zone=utm.from_latlon(point[1],point[0])
        #latitude 纬度 longitude 经度,网格
        utmPoints.append([x,y])
    area=abs(shapefile.signed_area(utmPoints))#abs()绝对值函数 signed_area()计算多边形面积
    if area<=100:
        writer.shape(shapeRecord.shape)
        writer.record(*shapeRecord.record)
reader.close()
writer.close()
print("Shapefile文件分隔完成！")
'''
r=shapefile.Reader(r"D:\Program Files\Python学习文档\samples\footprints\footprints_se.shp")
subset=shapefile.Reader(r"D:\Program Files\Python学习文档\samples\footprints\footprints_split.shp")
r.numRecords
26447
subset.numRecords
13331
'''