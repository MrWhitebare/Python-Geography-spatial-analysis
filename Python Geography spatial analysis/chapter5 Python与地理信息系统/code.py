#geocode.py 地理编码 
import geocoder
from geopy.geocoders import Nominatim
g=geocoder.google("1043 Washington Ave,New Oroleans,LA70130")
print(g.geojosn)
print(g.wkt)
geo=Nominatim()
location=geo.geocode("88360 Diamondhead Dr E, Diamondhead, MS39525")
rev=geo.reverse("{0},{1}".format(location.latitude,location.longitude))
print(rev)
print(location.raw)