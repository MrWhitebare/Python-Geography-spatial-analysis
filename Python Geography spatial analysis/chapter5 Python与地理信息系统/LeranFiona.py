#使用fiona库 Kobe Bryant
import fiona
with fiona.open("MS_UrbanAnC10.shp") as sf:
	filtered=filter(lambda f: f['properties']['pop'] < 5000, sf)
	#shapefile文件驱动格式
	drv=sf.driver
	#参考坐标系
	crs=sf.crs
	#Dbf架构
	schm=sf.schema
	subset="MS_Urban_Subset.shp"
	with fiona.open(subset,"w",driver=drv,crs=crs,schema=schm) as w:
		for rec in filtered:
			w.writer(rec)