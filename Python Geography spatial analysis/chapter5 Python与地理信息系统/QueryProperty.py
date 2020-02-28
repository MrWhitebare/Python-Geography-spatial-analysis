#QueryProperty.py 属性查询
import shapefile
reader=shapefile.Reader(r"D:\Program Files\Python学习文档\samples\MS_UrbanAnC10\MS_UrbanAnC10.shp")
writer=shapefile.Writer(r"D:\Program Files\Python学习文档\samples\MS_UrbanAnC10\MS_Urban_Subset.shp",reader.shapeType)
writer.fields=list(reader.fields[1:])
#获取几何图形和所有特征图层对应的人口数
selection=list()
for record in reader.iterShapeRecords():
    geom=record.shape
    if record.record[14]<5000:
        #取出人口字段的值进行比较
        selection.append([record.record,geom])
for record,geom in selection:
    #print(record,geom)
    writer.shape(geom)  # geometry
    writer.record(*record)  #保存字段，而不是保存对象
reader.close()
writer.close()
print("属性查询完成！")

