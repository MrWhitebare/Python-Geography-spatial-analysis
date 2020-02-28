import shapefile
file_name=r"D:\Program Files\Python学习文档\samples\ep202009.026_5day_pgn\ep202009.026_5day_pgn.shp"
reader=shapefile.Reader(file_name)
writer=shapefile.Writer("D:\Program Files\Python学习文档\samples\ep202009.026_5day_pgn\storm.shp",shapefile.POLYGON)
writer.fields=list(reader.fields)
for rec in reader.iterShapeRecords():
    writer.record(*rec.record)
    writer.shape(rec.shape)
writer.poly([[[-104,24],[-104,25],[-103,25],[-103,24],[-104,24]]])
writer.record("STANLEY","TD","091022/1500","27","21","48","ep")
writer.close()