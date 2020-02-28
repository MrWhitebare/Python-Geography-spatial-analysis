import shapefile
#读取文件
reader=shapefile.Reader(r"D:\Program Files\Python学习文档\samples\NYC_MUSEUMS_GEO\NYC_MUSEUMS_GEO.shp")
#创建文件，添加路径也添加多边形类型
writer=shapefile.Writer(r"D:\Program Files\Python学习文档\samples\NYC_MUSEUMS_GEO\NYC_MUSEUMS_UTM.shp",reader.shapeType)
writer.fields=list(reader.fields)
#复制原图形信息
'''
for rec in reader.iterShapeRecords():
    writer.record(*rec.record)
    writer.shape(rec.shape)
'''
#新建字段
writer.field("LAT","F",8,5)
writer.field("LON","F",8,5)
#读取坐标信息
geo=shapefile.Reader(r"D:\Program Files\Python学习文档\samples\NYC_MUSEUMS_GEO\NYC_MUSEUMS_GEO.shp")
i=0
for shape in geo.iterShapeRecords():
    ls = shape.record#读取记录
    lon,lat=geo.shape(i).points[0]#读取坐标
    #print(geo.shape(i).points)
    ls.extend([lat,lon])#添加新建字段属性
    writer.record(*ls)#写入字段
    writer.shape(shape.shape)
    i+=1
    reader.close()
writer.close()
geo.close()
print("添加字段成功！")