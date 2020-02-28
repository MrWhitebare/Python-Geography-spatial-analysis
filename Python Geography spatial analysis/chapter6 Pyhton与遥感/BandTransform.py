#BandTransform.py 图像波段变换
from osgeo import gdal_array
srcImg=r"D:\Program Files\Python学习文档\samples\FalseColor\FalseColor.tif"
array=gdal_array.LoadFile(srcImg)
#为了获得真彩色图片交换band1和band2
#使用numpy库的高级分片功能对波段进行重新排列
out=r"D:\Program Files\Python学习文档\samples\FalseColor\Swap.tif"
output=gdal_array.SaveArray(array[[1,0,2],:],out,format="GTiff",prototype=srcImg)
#取消输出避免损坏文件
output=None