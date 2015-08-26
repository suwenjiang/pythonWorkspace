__author__ = 'suwen'
import ArcPy_Project
import os
from ArcPy_Project import env

def CreateContectionFile(wrkspc,userName,password):
      # con = 'http://localhost:6080/arcgis/admin'
    con="http://"+str(serverName)+":6080/arcgis/admin"
    connection_file_path=str(wrkspc)+"/tmp.ags"
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



#get the servername
serverName=ArcPy_Project.GetParameterAsText(0)

#get the username and the password to connect the server
userName=ArcPy_Project.GetParameterAsText(1)
password=ArcPy_Project.GetParameterAsText(2)
#Get the mxd files directory
mxdfolder=ArcPy_Project.GetParameterAsText(3)
#set the workspace
env.workspace=ArcPy_Project.GetParameterAsText(4)
wrkspc =env.workspace

# Create the connection file
connection_file_path=CreateContectionFile(wrkspc,userName,password)
# the mxd file list of the mxdPath
if os.path.isdir(mxdfolder)==False:
    print "this path is not a dir"
else:
    mxds=os.listdir(mxdfolder)
    for file in mxds:
        if file.endswith(".mxd"):
            mxdpath=os.path.join(mxdfolder,file)
            PublishService(connection_file_path,wrkspc,mxdpath)





