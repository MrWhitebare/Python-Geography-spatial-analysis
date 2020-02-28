#MergeShapefile.py 使用dbfpy合并Shapefile
import shapefile
import glob
from dbfpy3 import dbf
files=glob.glob(r"D:\Program Files\Python学习文档\samples\footprints\footprints_*shp")
writer=shapefile.Writer(r"D:\Program Files\Python学习文档\samples\footprints\Merged.shp",shapefile.POLYGON)
reader=None
for file in files:
    print(file)
    reader=shapefile.Reader(r"{0}".format(file))#读取文件
    i = 0
    if(i==0):
        writer.fields = list(reader.fields[1:])
        #跳过('DeletionFlag', 'C', 1, 0)
        print(reader.fields)
    for shape in reader.iterShapeRecords():
        writer.record(*shape.record)
        writer.shape(shape.shape)
        i+=1
reader.close()
writer.close()
print("shapefile合并完成！")
