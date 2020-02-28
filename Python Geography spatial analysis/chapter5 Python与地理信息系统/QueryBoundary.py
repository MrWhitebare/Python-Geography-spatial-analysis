#QueryBoudary.py 查询边框
import shapefile
reader=shapefile.Reader(r"D:\Program Files\Python学习文档\samples\roads\roadtrl020.shp")
writer=shapefile.Writer(r"D:\Program Files\Python学习文档\samples\roads\selection.shp",reader.shapeType)
writer.fields=list(reader.fields[1:])
xmin=-67.5
xmax=-65.0
ymin=17.8
ymax=18.6
for road in reader.iterShapeRecords():
	geom=road.shape#geometry
	rec=road.record
	sxmin,symin,sxmax,symax=geom.bbox#boundary
	if sxmin < xmin:
		continue
	elif sxmax > xmax:
		continue
	elif symin < ymin:
		continue
	elif symax > ymax:
		continue
	writer.shape(geom)
	writer.record(*rec)
reader.close()
writer.close()
print("查询边界成功！")