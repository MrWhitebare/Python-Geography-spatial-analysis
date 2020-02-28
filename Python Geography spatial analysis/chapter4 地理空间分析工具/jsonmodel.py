# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 14:17:42 2020

@author: 立文
"""

import json
jsdata="""{"type":"Feature","id":"OpenLayers.Feature.Vector_314","properties":{},
"geometry":{"type":"Point","coordinates":[97.03125,39.7265625]},"crs":{"type":"name","properties":{
"name":"urn.ogr.def.crs.OGR.1.2.CRS84"}}}
"""
point=eval(jsdata)
pydata=json.loads(jsdata)
json.dumps(pydata)
