from osgeo import gdal,gdal_array,gdalnumeric,ogr
from PIL import Image, ImageDraw
import os
import time
import operator
from functools import reduce
#脚本采用先计算NDVI值，再裁切的方式
def get_ndvi(filename,red,infrared):  # 计算某一影像的ndvi值，返回二维数组
    dataset = gdal.Open(filename)
    cols = dataset.RasterXSize  # 列数
    rows = dataset.RasterYSize  # 行数
    band3 = dataset.GetRasterBand(red).ReadAsArray(0, 0, cols, rows)
    band4 = dataset.GetRasterBand(infrared).ReadAsArray(0, 0, cols, rows)
    molecule = band4 - band3
    denominator = band4 + band3
    del dataset
    band = molecule / denominator
    band[band > 1] = 9999  # 过滤异常值
    return band
def compute_band(file,target):
    dataset = gdal.Open(file)
    cols = dataset.RasterXSize  # 列数
    rows = dataset.RasterYSize  # 行数
    # 生成影像
    target_ds = gdal.GetDriverByName('GTiff').Create(target, xsize=cols, ysize=rows, bands=1,eType=gdal.GDT_Float32)
    target_ds.SetGeoTransform(dataset.GetGeoTransform())
    target_ds.SetProjection(dataset.GetProjection())
    del dataset
    band = get_ndvi(file,1,2)
    target_ds.GetRasterBand(1).SetNoDataValue(9999)
    target_ds.GetRasterBand(1).WriteArray(band)
    target_ds.FlushCache()
def ImageToArray(i):
    #把一个Python影像库的数组转化为一个Gdal_array图片
    a=gdal_array.numpy.fromstring(i.tobytes(),'b')
    a.shape=i.im.size[1], i.im.size[0]
    return a
def World2Pixel(geoMatrix,x,y):
    #使用gdal库的geomatrix对象【gdal.GetGeoTransform()】计算地理坐标的像素位置
    ulX=geoMatrix[0]
    ulY=geoMatrix[3]
    xDist=geoMatrix[1]
    yDist=geoMatrix[5]
    pixel=int((x-ulX)/xDist)
    line=int((ulY-y)/abs(yDist))
    return (pixel,line)
def arrayToImage(a):
    """
    Converts a gdalnumeric array to a
    Python Imaging Library Image.
    """
    i=Image.frombytes('L',(a.shape[1],a.shape[0]),
            (a.astype('b')).tobytes())
    return i
def OpenArray( array, prototype_ds = None, xoff=0, yoff=0 ):
    ds =gdal_array.OpenArray(array)
    if ds is not None and prototype_ds is not None:
        if type(prototype_ds).__name__ == 'str':
            prototype_ds = gdal.Open(prototype_ds)
        if prototype_ds is not None:
            gdal_array.CopyDatasetInfo( prototype_ds, ds, xoff=xoff, yoff=yoff )
    return ds
def histogram(a, bins=range(0,256)):
    """
    Histogram function for multi-dimensional array.
    a = array
    bins = range of numbers to match
    """
    fa = a.flat
    n = gdalnumeric.searchsorted(gdalnumeric.sort(fa), bins)
    n = gdalnumeric.concatenate([n, [len(fa)]])
    hist = n[1:]-n[:-1]
    return hist

def stretch(a):
    """
    Performs a histogram stretch on a gdalnumeric array image.
    """
    hist = histogram(a)
    im = arrayToImage(a)
    lut = []
    for b in range(0, len(hist), 256):
        # step size
        step = reduce(operator.add, hist[b:b+256]) / 255
        # create equalization lookup table
        n = 0
        for i in range(256):
            lut.append(n / step)
            n = n + hist[i+b]
        im = im.point(lut)
    return ImageToArray(im)
def main(delete):
    source=r"D:\Program Files\Python学习文档\samples\NDVI\farm.tif"
    target=r"D:\Program Files\Python学习文档\samples\NDVI\Clip_farm.tif"
    shp=r"D:\Program Files\Python学习文档\samples\NDVI\field.shp"
    output=r"D:\Program Files\Python学习文档\samples\NDVI\clip_ndvi.tif"
    compute_band(source,target)
    srcArray = gdalnumeric.LoadFile(target)
    srcImage = gdal.Open(target)
    geoTrans = srcImage.GetGeoTransform()
    shapef = ogr.Open(shp)
    lyr = shapef.GetLayer(os.path.split(os.path.splitext(shp)[0] )[1] )
    poly = lyr.GetNextFeature()
    minX, maxX, minY, maxY = lyr.GetExtent()
    ulX, ulY = World2Pixel(geoTrans, minX, maxY)
    lrX, lrY = World2Pixel(geoTrans, maxX, minY)
    pxWidth = int(lrX - ulX)
    pxHeight = int(lrY - ulY)
    clip = srcArray[ulY:lrY, ulX:lrX]
    xoffset =  ulX
    yoffset =  ulY
    print("Xoffset, Yoffset = ( %f, %f )" % ( xoffset, yoffset ))
    geoTrans = list(geoTrans)
    geoTrans[0] = minX
    geoTrans[3] = maxY
    points = []
    pixels = []
    geom = poly.GetGeometryRef()
    pts = geom.GetGeometryRef(0)
    for p in range(pts.GetPointCount()):
      points.append((pts.GetX(p), pts.GetY(p)))
    for p in points:
      pixels.append(World2Pixel(geoTrans, p[0], p[1]))
    rasterPoly = Image.new("L", (pxWidth, pxHeight), 1)
    rasterize = ImageDraw.Draw(rasterPoly)
    rasterize.polygon(pixels, 0)
    mask = ImageToArray(rasterPoly)
    clip = gdalnumeric.choose(mask,(clip, 0)).astype(gdalnumeric.uint8)
    gtiffDriver = gdal.GetDriverByName( 'GTiff' )
    if gtiffDriver is None:
        raise ValueError("Can't find GeoTiff Driver")
    gtiffDriver.CreateCopy(output,OpenArray( clip, prototype_ds=target, xoff=xoffset, yoff=yoffset ))
    if delete and os.path.exists(target):
        os.remove(target)
if __name__ == '__main__':
    start=time.perf_counter()
    main(False)
    end=time.perf_counter()-start
    print("NDVI计算耗时",end)
