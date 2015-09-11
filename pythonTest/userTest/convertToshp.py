# -*- coding: gbk -*-
import arcpy
import json
import uuid
from arcpy import env
import datetime
import time
import os
import string
from shutil import copy
def commit():
    starttime = datetime.datetime.now()
    spatialReference={'wkt':'PROJCS["SH",GEOGCS["GCS_Beijing_1954",DATUM["D_Beijing_1954",SPHEROID["Krasovsky_1940",6378245.0,298.3]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Gauss_Kruger"],PARAMETER["False_Easting",8.0],PARAMETER["False_Northing",-3457143.04],PARAMETER["Central_Meridian",121.4671519444444],PARAMETER["Scale_Factor",1.0],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]'}
    cutpolygon={"rings": [[[-21182.21789336484, 3622.4762820750475], [-19846.069387733936, 3344.6632264479995], [-18602.525233979337, 2603.828411443159], [-15573.040008341894, 1519.0345751922578], [-14699.913262089714, 341.63638705946505], [-15242.310180216096, -1232.637594819069], [-17332.522693973966, -650.5530973169953], [-18060.128315851092, 606.2202495634556], [-19660.860683985054, 1479.3469958156347], [-21248.363858991303, 2352.473742067814], [-21182.21789336484, 3622.4762820750475]]], "spatialReference": {"wkt": "PROJCS[\"ShangHaiCity\",GEOGCS[\"GCS_Beijing_1954\",DATUM[\"D_Beijing_1954\",SPHEROID[\"Krasovsky_1940\",6378245.0,298.3]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Gauss_Kruger\"],PARAMETER[\"False_Easting\",8.0],PARAMETER[\"False_Northing\",-3457143.04],PARAMETER[\"Central_Meridian\",121.4671519444444],PARAMETER[\"Scale_Factor\",1.0],PARAMETER[\"Latitude_Of_Origin\",0.0],UNIT[\"Meter\",1.0]]"}}
    result=cutpolygon_t = arcpy.AsShape(cutpolygon,True)
    arcpy.SetParameterAsText(2, cutpolygon_t.JSON)

    print result
    print cutpolygon_t.JSON
    print u"执行时间共 "+str((datetime.datetime.now()-starttime).seconds)+u"秒"
if __name__ == "__main__":
    print(u"开始计算...")
    commit()