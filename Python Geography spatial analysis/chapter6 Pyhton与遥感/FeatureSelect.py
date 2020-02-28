#FeatureSelect.py 图像特征提取
from osgeo import gdal_array
src=r"D:\Program Files\Python学习文档\samples\islands\islands.tif"
target=r"D:\Program Files\Python学习文档\samples\islands\islands_classified.tiff"
srcArray=gdal_array.LoadFile(src)
#将直方图分割为2子区间以便分类
classes=gdal_array.numpy.histogram(srcArray,bins=2)[1]
lut=[[255,0,0],[0,0,0],[255,255,255]]
#开始分类
start=1
#建立输出图片
rgb=gdal_array.numpy.zeros((3,srcArray.shape[0],srcArray.shape[1]),gdal_array.numpy.float32)
#处理所有类别并分配颜色
for i in range(len(classes)):
    mask=gdal_array.numpy.logical_and(start<=srcArray,srcArray<=classes[i])
    for j in range(len(lut[i])):
        rgb[j]=gdal_array.numpy.choose(mask,(rgb[j],lut[i][j]))
    start=classes[i]+1
#save
output=gdal_array.SaveArray(rgb.astype(gdal_array.numpy.uint8),target,format="GTIFF",prototype=src)
output=None
print("分类完成！")

