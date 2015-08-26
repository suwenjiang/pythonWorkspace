#-*-  coding:utf-8 -*-
import ArcPy_Project
import xml.dom.minidom as DOM
import os
import sys
import codecs
import chardet

def RePairMxd(oldMxd,old_dataSource_path,new_DataSourcePath):
    print "checking the  mxd files..."
    brknlist=ArcPy_Project.mapping.ListBrokenDataSources(oldMxd) #check the datasource
    if len(brknlist)>0:
        oldMxd.findAndReplaceWorkspacePaths(old_dataSource_path,new_DataSourcePath)
        oldMxd.save()
        print "the mxd file repaird"

def GetMXDFils(mxdPath):
    try:
        mxdPath=mxdPath.decode("gbk")
        mxd_file_lists=[] #所有需要overwrite的mxd文件
        if os.path.exists(mxdPath):
            for file in os.listdir(mxdPath):
                if file.endswith(".mxd"):
                    fullpath=os.path.join(mxdPath,file)

                    mxd_file_lists.append(fullpath)
        else:
            print "mxd directory is not valid"
        return mxd_file_lists
    except Exception,e:
        print e


def PublishService(mapDoc,sddraft,service,con,sd):
    try:
        #check sddraft and sd file exist or not


       # sddraft=sddraft.decode('KOI8-R').encode('utf-8')
        #sddraft=unicode(sddraft)
        #print chardet.detect(sddraft)
        #sd=sddraft.decode('ISO-8859-2').encode('utf-8')
        #print chardet.detect(sd)

        analysis = ArcPy_Project.mapping.CreateMapSDDraft(mapDoc, sddraft, service, 'ARCGIS_SERVER',
                                                  con, True, None,None,None)
        print analysis['warnings']
        print analysis['messages']
        # set service type to esriServiceDefinitionType_Replacement
        newType = 'esriServiceDefinitionType_Replacement'
        xml = sddraft
        doc = DOM.parse(xml)
        descriptions = doc.getElementsByTagName('Type')
        for desc in descriptions:
            if desc.parentNode.tagName == 'SVCManifest':
                if desc.hasChildNodes():
                    desc.firstChild.data = newType
        outXml = xml
        #   print chardet.detect(outXml)
        f = open(outXml, 'w')
        doc.writexml( f )
        f.close()
        print sd.__class__
        print sddraft.__class__
        # stage and upload the service if the sddraft analysis did not contain errors
        if analysis['errors'] == {}:
            print "creating the sddraft file..."
            ArcPy_Project.StageService_server(sddraft, sd)
            print "uploading serviceDefinition..."
            ArcPy_Project.UploadServiceDefinition_server(sd, con)
            print service+" overwrite successfully.."
        else:
            # if the sddraft analysis contained errors, display them
            print analysis['errors']
    except Exception,e:
        print e
def CreateContectionFile(wrkspc,userName,password,serverName):
      # con = 'http://localhost:6080/arcgis/admin'
    con="http://"+str(serverName)+":6080/arcgis/admin"
    connection_file_path=str(wrkspc)+"/tmp.ags"

    if os.path.exists(connection_file_path):
        os.remove(connection_file_path)
    agsname=os.path.basename(connection_file_path)
    ArcPy_Project.mapping.CreateGISServerConnectionFile("ADMINISTER_GIS_SERVICES",
                                                    wrkspc,
                                                   agsname,
                                                    con,
                                                    "ARCGIS_SERVER",
                                                    username=userName,
                                                    password=password,
                                                    save_username_password=True)

    return connection_file_path

def OverWriteMapService(mxd_dir,old_datasource,new_datasource,con,stage_path):
    #mxd_file_lists
    #old_datasource
    #new_datasource
    print "Get the mxd files..."
    mxd_file_lists=GetMXDFils(mxd_dir)
    try:
        for file in mxd_file_lists:
            print "Checking the services.."
            mapDoc = ArcPy_Project.mapping.MapDocument(file) #读取地图文档
            fileName=os.path.split(file)[1] #获取mxd文件的名字作为服务的名字
            print "overwriting the servcie:"+fileName+"..."
            sddraftName=fileName.replace(".mxd",".sddraft") #sddraft文件名
            sdName=fileName.replace(".mxd",".sd")#sd文件的名称
            service=os.path.splitext(fileName)[0] #服务名，默认服务名与地图文档名相同
            sss="repairing the service:"+service+"..."
            RePairMxd(mapDoc,old_datasource,new_datasource) #修复地图文档，如果是sde输入的为sde链接文件
            sddraft=os.path.join(stage_path,sddraftName)
            sd=sddraft.replace(".sddraft",".sd")
            PublishService(mapDoc,sddraft,service,con,sd)

    except Exception,e:
        print e

def CheckPath(filePath):
    if ".sde" in filePath:
    #判断是否sde文件是否存在
        if os.path.isfile(filePath):
            return  True
        else:
            print "SDE file path is not valid"
            return  False
    else:
        if os.path.isdir(filePath):
            return True
        else:
            print filePath+" is not a valid path"
            return False

mxdPath=r"d:\data\china"
con="http://localhost:6080/arcgis/admin"
#get the default staging path
staging_path=os.path.expanduser("~\AppData\Local\Esri\Desktop10.2\Staging")
sde_path=os.path.expanduser("~\AppData\Roaming\ESRI\Desktop10.2\ArcCatalog")
wrkspc=staging_path
old_dataSource="d:\data\china"
new_dataSource=r"d:\data\chinaCopy"

if CheckPath(old_dataSource) and CheckPath(new_dataSource):
    Conectfile_file=CreateContectionFile(wrkspc,"arcgis","jmb","localhost")
    OverWriteMapService(mxdPath,old_dataSource,new_dataSource,Conectfile_file,staging_path)