"""
Output a normalized vegetative index
"""
import gdal, gdalnumeric, ogr
from PIL import Image, ImageDraw

def imageToArray(i):
  """
  Converts a Python Imaging Library 
  array to a gdalnumeric image.
  """
  a=gdalnumeric.numpy.fromstring(i.tostring(),'b')
  a.shape=i.im.size[1], i.im.size[0]
  return a
   
def world2Pixel(geoMatrix, x, y):
  """
  Uses a gdal geomatrix (gdal.GetGeoTransform()) 
  to calculate the pixel location of a 
  geospatial coordinate 
  """
  ulX = geoMatrix[0]
  ulY = geoMatrix[3]
  xDist = geoMatrix[1]
  yDist = geoMatrix[5]
  pixel = int((x - ulX) /xDist)
  line = int((ulY - y) / yDist)
  return (pixel, line)    

# Multispectral image used 
# to create the NDVI. Must
# have red and infrared
# bands
source = r"D:\Program Files\Python学习文档\samples\NDVI\farm.tif"

# Output geotiff file name
target =r"D:\Program Files\Python学习文档\samples\NDVI\farm_ndvi2.tif"

# Load the source data as a gdalnumeric array
srcArray = gdalnumeric.LoadFile(source)

# Also load as a gdal image to 
# get geotransform (world file) info
srcImage = gdal.Open(source)
geoTrans = srcImage.GetGeoTransform()

# Red and infrared (or near infrared) bands
r = srcArray[1]
ir = srcArray[2]

## Clip a field out of the bands using a
## field boundary shapefile

# Create an OGR layer from a Field boundary shapefile
shp=r"D:\Program Files\Python学习文档\samples\NDVI\field.shp"
field = ogr.Open(shp)
# Must define a "layer" to keep OGR happy
lyr = field.GetLayer("field")
# Only one polygon in this shapefile
poly = lyr.GetNextFeature()

# Convert the layer extent to image pixel coordinates
minX, maxX, minY, maxY = lyr.GetExtent()
ulX, ulY = world2Pixel(geoTrans, minX, maxY)
lrX, lrY = world2Pixel(geoTrans, maxX, minY)

# Calculate the pixel size of the new image
pxWidth = int(lrX - ulX)
pxHeight = int(lrY - ulY)

# Clip each band to the extent of the shapefile
rClip = r[ulY:lrY, ulX:lrX]
irClip = ir[ulY:lrY, ulX:lrX]

# Create a new geomatrix for the target image
geoTrans = list(geoTrans)
geoTrans[0] = minX
geoTrans[3] = maxY

# Map points to pixels for drawing 
# the field boundary on a blank
# 8-bit, black and white, mask image.
points = []
pixels = []

# Grab the polygon geometry
geom = poly.GetGeometryRef()
pts = geom.GetGeometryRef(0)

# Loop through geometry and turn
# the points into an easy-to-manage 
# Python list 
for p in range(pts.GetPointCount()):
  points.append((pts.GetX(p), pts.GetY(p)))
  
# Loop through the points and map to pixels.
# Append the pixels to a pixel list
for p in points:
  pixels.append(world2Pixel(geoTrans, p[0], p[1]))
# Create the raster polygon image
rasterPoly = Image.new("L", (pxWidth, pxHeight), 1)
# Create a PIL drawing object
rasterize = ImageDraw.Draw(rasterPoly)
# Dump the pixels to the image
rasterize.polygon(pixels, 0)
# Hand the image back to gdal/gdalnumeric
# so we can use it as an array mask
mask = imageToArray(rasterPoly)    
# Clip the red band using the mask   
rClip = gdalnumeric.numpy.choose(mask, \
  (rClip, 0)).astype(gdalnumeric.numpy.uint8)
# Clip the infrared band using the mask
irClip = gdalnumeric.numpy.choose(mask, \
  (irClip, 0)).astype(gdalnumeric.numpy.uint8)

# We don't care about numpy warnings
# due to NaN values from clipping
gdalnumeric.numpy.seterr(all="ignore")

# NDVI equation: (infrared - red) / (infrared + red)
# *1.0 converts values to floats, 
# +1.0 prevents ZeroDivisionErrors 
ndvi = 1.0 * (irClip - rClip) / irClip + rClip + 1.0

# Remove any NaN values from the final product
ndvi = gdalnumeric.numpy.nan_to_num(ndvi)

# Save ndvi as tiff
gdalnumeric.SaveArray(ndvi, target, \
  format="GTiff", prototype=srcImage)

# Update georeferencing and NoData value
update = gdal.Open(target, 1)
update.SetGeoTransform(list(geoTrans))
update.GetRasterBand(1).SetNoDataValue(0.0)
update = None
