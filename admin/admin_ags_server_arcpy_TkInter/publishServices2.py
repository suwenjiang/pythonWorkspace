# -*-coding:utf-8 -*-
__author__ = 'jiangmb'
import arcpy
import os
import shutil

import xml.dom.minidom as DOM

def PublishService(mapDocPath,con):

    '''' mxd文档路径，服务名称和连接字符串路径'''
    mapDoc=arcpy.mapping.MapDocument(mapDocPath)
    # check the sd file exits or not

    for i in range(502,551):

        serviceName='myMapServer'+str(i)
        sddraft=r"d:\workspace\test.sddraft"

        result= arcpy.mapping.CreateMapSDDraft(mapDoc, sddraft, serviceName, 'ARCGIS_SERVER', con, True, None)
        newSddaft= setTheClusterName(sddraft,'ClusterC',serviceName)

        print newSddaft
    # analyze the service definition draft
        analysis = arcpy.mapping.AnalyzeForSD(newSddaft)


        if analysis['errors'] == {}:
        # Execute StageService
            sd="d:\\workspace\\"+serviceName+".sd"
            if(os.path.exists(sd)):
                os.remove(sd)
            arcpy.StageService_server(sddraft, sd)

        # Execute UploadServiceDefinition
            arcpy.UploadServiceDefinition_server(sd, con)
            print "publish successufully"+str(i)
           # createCache(con+"\\"+serviceName,i)

        else:
            print "Publish failed"



def setTheClusterName(xml,clusterName,serviceName):# the new description

    doc = DOM.parse(xml)
    # find the Item Information Description element
    doc.getElementsByTagName('Cluster')[0].childNodes[0].nodeValue=clusterName
    # for i in range(doc.getElementsByTagName('Name').length):
    #     doc.getElementsByTagName('Name')[i].childNodes[0].nodeValue=serviceName


    # output to a new sddraft
    outXml =xml
    f = open(outXml, 'w')
    doc.writexml( f )
    f.close()
    return  outXml




# Import system modules


# Set environment settings
def createCache(inputService,i):

# List of input variables for map service properties
#     connectionFile = r"C:\Users\<username>\AppData\Roaming\ESRI\Desktop10.1\ArcCatalog"
#     server = "arcgis on MyServer_6080 (publisher)"
#     serviceName = "Rainfall.MapServer"

    serviceCacheDirectory = "C:\\arcgisserver\\directories\\arcgiscache"

    scalesType = ""
    tileOrigin = ""


    numOfScales = "5"
    scales = "64000000,32000000,16000000,8000000,4000000"
    dotsPerInch = "96"
    tileSize = "256 x 256"
    cacheTileFormat = "JPEG"
    tileCompressionQuality = "75"
    storageFormat = "COMPACT"


    tilingSchemeType = "NEW"
    scalesType = "CUSTOM"


    predefinedTilingScheme = ""




    inputService=inputService+".MapServer"
    print inputService


    print "begin cache"+str(i)
    result = arcpy.CreateMapServerCache_server (inputService,
                                                    serviceCacheDirectory,
                                                    tilingSchemeType, scalesType,
                                                    numOfScales, dotsPerInch,
                                                    tileSize, predefinedTilingScheme,
                                                    tileOrigin, scales,
                                                    cacheTileFormat,
                                                    tileCompressionQuality,
                                                    storageFormat)
    print "cachesuccessfullly"+str(i)





con=r"C:\Users\jiangmb\AppData\Roaming\ESRI\Desktop10.3\ArcCatalog\arcgis on 192.168.221.102_6080 (admin).ags"

PublishService('d:\\workspace\\test.mxd',con)