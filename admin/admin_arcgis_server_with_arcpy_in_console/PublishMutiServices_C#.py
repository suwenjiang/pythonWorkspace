__author__ = 'suwen'
import ArcPy_Project
import os
import sys
from ArcPy_Project import env

def CreateContectionFile(wrkspc,userName,password,serverName):


    con="http://"+str(serverName)+":6080/arcgis/admin"
    connection_file_path=str(wrkspc)+"/tmp.ags"
    #
    if os.path.exists(connection_file_path):
        os.remove(connection_file_path)
    ArcPy_Project.mapping.CreateGISServerConnectionFile("ADMINISTER_GIS_SERVICES",
                                                    wrkspc,
                                                    "tmp.ags",
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

    analysis = ArcPy_Project.mapping.CreateMapSDDraft(mapDoc, sddraft, serviceName, 'ARCGIS_SERVER',
                                              connection_file_path, True, None,None,None)

    ArcPy_Project.StageService_server(sddraft, sd)
    ArcPy_Project.UploadServiceDefinition_server(sd, connection_file_path)



str_sys=sys.argv[1] #the first argv,and check if it contains the flag ",",
if "," in str_sys:
    print "this is flag one"
    sys_list=str_sys.split(',')
    serverName=sys_list[0]
    #get the username and the password to connect the server
    userName=sys_list[1]
    password=sys_list[2]
    #Get the mxd files directory
    mxdfolder=sys_list[3]
    #set the workspace
    env.workspace=sys_list[4]
    wrkspc =env.workspace
    connection_file_path=CreateContectionFile(wrkspc,userName,password,serverName)


if os.path.isdir(mxdfolder)==False:
    print "/this path is not a dir"
else:
    mxds=os.listdir(mxdfolder)
    mxd_files=[]

    for file in mxds:
        if file.endswith(".mxd"):
            mxdpath=os.path.join(mxdfolder,file)
            mxd_files.append(mxdpath)
    print mxd_files
for mxd in mxd_files:
    PublishService(connection_file_path,wrkspc,mxd)
print "pulish service successfully"








