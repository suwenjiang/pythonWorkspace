__author__ = 'suwen'
import os
import arcpy

def CreateContectionFile(wrkspc,userName,password,serverName):

      # con = 'http://localhost:6080/arcgis/admin'
    con="http://"+str(serverName)+":6080/arcgis/admin"
    print con
    connection_file_path=str(wrkspc)+"/tmp.ags"
    #
    if os.path.exists(connection_file_path):
        os.remove(connection_file_path)
    agsname=os.path.basename(connection_file_path)
    arcpy.mapping.CreateGISServerConnectionFile("ADMINISTER_GIS_SERVICES",
                                                    wrkspc,
                                                   agsname,
                                                    con,
                                                    "ARCGIS_SERVER",
                                                    username=userName,
                                                    password=password,
                                                    save_username_password=True)

    return connection_file_path


def PublishService(connection_file_path,wrkspc,mapDoc):
    #get the serviceName
    serviceName =os.path.basename(mapDoc).replace(".mxd","")

   #create the .sddraft path
    sddraftname=os.path.basename(mapDoc).replace(".mxd",".sddraft")
    sddraft =str(wrkspc)+"/"+str(sddraftname)
    #create the .sd file path
    sdname=os.path.basename(mapDoc).replace(".mxd",".sd")
    sd=str(wrkspc)+"/"+str(sdname)
   #check the file exists or not
    if(os.path.exists(sd)):
        os.remove(sd)

    analysis =arcpy.mapping.CreateMapSDDraft(mapDoc, sddraft, serviceName, 'ARCGIS_SERVER',
                                              connection_file_path, True, None,None,None)

    arcpy.StageService_server(sddraft, sd)
    arcpy.UploadServiceDefinition_server(sd, connection_file_path)

connection_file_path="d:\\"
mxdfolder=r"D:\workspace\New folder"
userName="arcgis"
password="Super123"
serverName="192.168.220.64"
wrkspc=r"D:\workspace\New folder"
if len(connection_file_path)==0:
    #check the parameters
    if len(wrkspc)==0 or len(userName)==0 or len(password)==0 or len(serverName)==0:
        print "some parameter is invalid"
    else:
        connection_file_path=CreateContectionFile(wrkspc,userName,password,serverName)
# the mxd file list of the mxdPath
if os.path.isdir(mxdfolder)==False:
    print "this path is not a dir"
else:
    mxds=os.listdir(mxdfolder)
    mxd_files=[]
    for file in mxds:
        if file.endswith(".mxd"):
            mxdpath=os.path.join(mxdfolder,file)
            mxd_files.append(mxdpath)

for mxd in mxd_files:
    PublishService(connection_file_path,wrkspc,mxd)
