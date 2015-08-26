__author__ = 'suwen'
import ArcPy_Project
import os
from ArcPy_Project import env

def CreateContectionFile(wrkspc,userName,password,serverName):

      # con = 'http://localhost:6080/arcgis/admin'
    con="http://"+str(serverName)+":6080/arcgis/admin"
    connection_file_path=str(wrkspc)+"/tmp.ags"
    #
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
    if os.path.exists(connection_file_path):
        return connection_file_path
    return None

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


#get the connectionfile
connection_file_path=ArcPy_Project.GetParameterAsText(0)
#get the servername
serverName=ArcPy_Project.GetParameterAsText(1)
#
##get the username and the password to connect the server
userName=ArcPy_Project.GetParameterAsText(2)
password=ArcPy_Project.GetParameterAsText(3)
#Get the mxd files directory
mxdfolder=ArcPy_Project.GetParameterAsText(4)
#set the workspace
env.workspace=ArcPy_Project.GetParameterAsText(5)
wrkspc =env.workspace
# Create the connection file
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








