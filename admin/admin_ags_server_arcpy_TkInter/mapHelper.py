#-*-coding:utf-8 -*-
__author__ = 'jmb'
import arcpy
import os

import json,urllib2,urllib


def CreateMSD(filePathin,filePathout):
    if os.path.exists(filePathin):
        print "Begin to create msd..."
        mxd = arcpy.mapping.MapDocument(filePathin)
        #get the filename of the mxd
        msdname=os.path.basename(filePathin).replace('mxd','msd')

        msd = filePathout+"/"+msdname
        #df = arcpy.mapping.ListDataFrames(mxd, "County Maps")[0]
        arcpy.mapping.ConvertToMSD(mxd, msd, "", "NORMAL", "NORMAL")
        print "Create Successfully.."
    else:
        print "File dosen't exist, please check your file path.."

def CreateServerConntionFile(url,uname,pwd,out_folder_path,file_name):
        ''''''
        server_url =url+'/admin'
        use_arcgis_desktop_staging_folder = False
        username = uname
        password =pwd
        arcpy.mapping.CreateGISServerConnectionFile("ADMINISTER_GIS_SERVICES",
                                            out_folder_path,
                                            file_name,
                                            server_url,
                                            "ARCGIS_SERVER",
                                            use_arcgis_desktop_staging_folder,
                                            out_folder_path,
                                            username,
                                            password,
                                            "SAVE_USERNAME")

        print "create successfully"


def PublishService(mapDocPath,serviceName,con,testWidget):

    '''' mxd文档路径，服务名称和连接字符串路径'''
    mapDoc=arcpy.mapping.MapDocument(mapDocPath)

    sd=os.path.splitext(mapDocPath)[0]+".sd"
    sddraft=os.path.splitext(mapDocPath)[0]+".sddraft"
    # check the sd file exits or not
    if os.path.exists(sd):
        os.remove(sd)
    result= arcpy.mapping.CreateMapSDDraft(mapDoc, sddraft, serviceName, 'ARCGIS_SERVER', con, True, None)

    if not result['errors']=={}:
        print result['errors']
# analyze the service definition draft
    analysis = arcpy.mapping.AnalyzeForSD(sddraft)
# stage and upload the service if the sddraft analysis did not contain errors
    if analysis['errors'] == {}:
    # Execute StageService
        arcpy.StageService_server(sddraft, sd)
        testWidget.insert("end",serviceName+"创建服务定义文件成功\n")
    # Execute UploadServiceDefinition
        arcpy.UploadServiceDefinition_server(sd, con)
        testWidget.insert("end",serviceName+"发布服务成功\n")
    else:
    # if the sddraft analysis contained errors, display them
        testWidget.insert("end",serviceName+"发布失败,失败原因为:%s\n"%analysis['errors'])

def checkMxdValid(path):

    for fileName in os.listdir(path):
        fullPath = os.path.join(path, fileName)
        if os.path.isfile(fullPath):
            basename, extension = os.path.splitext(fullPath)
            if extension == ".mxd":
                mxd = arcpy.mapping.MapDocument(fullPath)
                print "MXD: " + fileName
                brknList = arcpy.mapping.ListBrokenDataSources(mxd)
                for brknItem in brknList:
                    print "\t" + brknItem.name
                    return False
    return True

def checkMxdValidation(path):


    mxd = arcpy.mapping.MapDocument(path)
    brknList = arcpy.mapping.ListBrokenDataSources(mxd)
    if brknList:
        return False

    return True

def getArcgisServerConnection():
        confilePath=os.getcwd()
        for root,dirname, files in os.walk(confilePath):
             list=[]
             for file in files:
                if os.path.splitext(file)[1]=='.ags':
                    list.append(file)
                    break
             if len(list)==0:
                print "找不到连接文件"
             else:
                 file=os.path.join(confilePath,file)
        return file



def PublishService(mapDocPath,serviceName,con):

    '''' mxd文档路径，服务名称和连接字符串路径'''
    mapDoc=arcpy.mapping.MapDocument(mapDocPath)

    sd=os.path.splitext(mapDocPath)[0]+".sd"
    sddraft=os.path.splitext(mapDocPath)[0]+".sddraft"
    # check the sd file exits or not
    if os.path.exists(sd):
        os.remove(sd)
    result= arcpy.mapping.CreateMapSDDraft(mapDoc, sddraft, serviceName, 'ARCGIS_SERVER', con, True, None)

    if not result['errors']=={}:
        print result['errors']
# analyze the service definition draft
    analysis = arcpy.mapping.AnalyzeForSD(sddraft)
# stage and upload the service if the sddraft analysis did not contain errors
    if analysis['errors'] == {}:
    # Execute StageService
        arcpy.StageService_server(sddraft, sd)

    # Execute UploadServiceDefinition
        arcpy.UploadServiceDefinition_server(sd, con)

    else:
        print "Publish failed"

def gentoken(server, port, adminUser, adminPass, expiration=60):
    #Re-usable function to get a token required for Admin changes

    query_dict = {'username':   adminUser,
                  'password':   adminPass,
                  'expiration': str(expiration),
                  'client':     'requestip'}

    query_string = urllib.urlencode(query_dict)
    url = "http://{}:{}/arcgis/admin/generateToken".format(server, port)

    token = json.loads(urllib.urlopen(url + "?f=json", query_string).read())

    if "token" not in token:
        arcpy.AddError(token['messages'])
        quit()
    else:
        return token['token']


def renameService(server, port, adminUser, adminPass, service, newName, token=None):
    ''' Function to rename a service
    Requires Admin user/password, as well as server and port (necessary to construct token if one does not exist).
    service = String of existing service with type seperated by a period <serviceName>.<serviceType>
    newName = String of new service name
    If a token exists, you can pass one in for use.
    '''

    # Get and set the token
    if token is None:
        token = gentoken(server, port, adminUser, adminPass)

    service = urllib.quote(service.encode('utf8'))

    # Check the service name for a folder:
    if "//" in service:
        serviceName = service.split('.')[0].split("//")[1]
        folderName = service.split('.')[0].split("//")[0] + "/"
    else:
        serviceName = service.split('.')[0]
        folderName = ""

    renameService_dict = { "serviceName": serviceName,
                           "serviceType": service.split('.')[1],
                           "serviceNewName" : urllib.quote(newName.encode('utf8'))
                         }


    rename_encode = urllib.urlencode(renameService_dict)
    rename = "http://{}:{}/arcgis/admin/services/{}renameService?token={}&f=json".format(server, port, folderName, token)
    status = urllib2.urlopen(rename, rename_encode ).read()


    if 'success' in status:
        pass
    else:
        pass
        arcpy.AddError(status)




def getfolder(url_admin,adminUser,adminPass,token=None):

    if token is None:
        token=gentoken(url_admin,adminUser,adminPass)
    service_url=url_admin+"/services?token={}&f=json".format(token)

    result=json.loads(urllib2.urlopen(service_url).read())

    if result:

        listForder=result["folders"]

    return listForder


def getServiceList(server, port,adminUser, adminPass, token=None):
    ''' Function to get all services
    Requires Admin user/password, as well as server and port (necessary to construct token if one does not exist).
    If a token exists, you can pass one in for use.
    Note: Will not return any services in the Utilities or System folder
    '''


    if token is None:
        token = gentoken(server, port, adminUser, adminPass)

    services = []
    folder = ''
    URL = "http://{}:{}/arcgis/admin/services{}?f=pjson&token={}".format(server, port, folder, token)

    serviceList = json.loads(urllib2.urlopen(URL).read())

    # Build up list of services at the root level
    for single in serviceList["services"]:
        services.append(single['serviceName'] + '.' + single['type'])

    # Build up list of folders and remove the System and Utilities folder (we dont want anyone playing with them)
    folderList = serviceList["folders"]
    folderList.remove("Utilities")
    folderList.remove("System")

    if len(folderList) > 0:
        for folder in folderList:
            URL = "http://{}:{}/arcgis/admin/services/{}?f=pjson&token={}".format(server, port, folder, token)
            fList = json.loads(urllib2.urlopen(URL).read())

            for single in fList["services"]:
                services.append(folder + "//" + single['serviceName'] + '.' + single['type'])

    return services


def getServerInfo(server, port, adminUser, adminPass, token=None):
    ''' Function to get and display a detailed report about a server
    Requires Admin user/password, as well as server and port (necessary to construct token if one does not exist).
    service = String of existing service with type seperated by a period <serviceName>.<serviceType>
    If a token exists, you can pass one in for use.
    '''

    # Get tand set the token
    if token is None:
        token = gentoken(server, port, adminUser, adminPass)

    # report = ''
    report={}
    URL = "http://{}:{}/arcgis/admin/".format(server, port)

    # report += "*-----------------------------------------------*\n\n"

    # Get Cluster and Machine info
    jCluster = getJson(URL, "clusters", token)

    if len(jCluster["clusters"]) == 0:
       # report += "No clusters found\n\n"
        report["clusters"]="No clusters found"
    else:
        for cluster in jCluster["clusters"]:
           # report += "Cluster: {} is {}\n".format(cluster["clusterName"], cluster["configuredState"])
            report["clusters"]="Cluster: {} is {}\n".format(cluster["clusterName"], cluster["configuredState"])
            if len(cluster["machineNames"])== 0:
                # report += "    No machines associated with cluster\n"
                report["machineNames"]=" No machines associated with cluster"
            else:
                # Get individual Machine info
                for machine in cluster["machineNames"]:
                    jMachine = getJson(URL, "machines/" + machine, token)
                    # report += "    Machine: {} is {}. (Platform: {})\n".format(machine, jMachine["configuredState"],jMachine["platform"])
                    report["machineNames"]="Machine: {} is {}. (Platform: {})\n".format(machine, jMachine["configuredState"],jMachine["platform"])


    # Get Version and Build
    jInfo = getJson(URL, "info", token)
    # report += "\nVersion: {}\nBuild:   {}\n\n".format(jInfo ["currentversion"], jInfo ["currentbuild"])
    report["Version"]="Version: {}Build:   {}\n\n".format(jInfo ["currentversion"], jInfo ["currentbuild"])

    # Get Log level
    jLog = getJson(URL, "logs/settings", token)
    # report += "Log level: {}\n\n".format(jLog["settings"]["logLevel"])
    report["Log level"]= "Log level: {}\n\n".format(jLog["settings"]["logLevel"])

    #Get License information
    jLicense = getJson(URL, "system/licenses", token)
    # report += "License is: {} / {}\n".format(jLicense["edition"]["name"], jLicense["level"]["name"])
    report["License"]="License is: {} / {}\n\n".format(jLicense["edition"]["name"], jLicense["level"]["name"])
    if jLicense["edition"]["canExpire"] == True:
        import datetime
        d = datetime.date.fromtimestamp(jLicense["edition"]["expiration"] // 1000) #time in milliseconds since epoch
        # report += "License set to expire: {}\n".format(datetime.datetime.strftime(d, '%Y-%m-%d'))
        report["License expiration"]="License set to expire: {}".format(datetime.datetime.strftime(d, '%Y-%m-%d'))
    else:
        # report += "License does not expire\n"
        report["License expiration"]="License does not expire"


    if len(jLicense["extensions"]) == 0:
        # report += "No available extensions\n"
        report["extensions"]="No available extensions"
    else:
        extension=''
        extension += "Available Extenstions........"
        for name in jLicense["extensions"]:
            extension += "extension:  {}\n\n v".format(name["name"])
        report["extension"]=extension
    return report
def getJson(URL, endURL, token):
    # Helper function to return JSON for a specific end point
    #

    openURL = URL + endURL + "?token={}&f=json".format(token)
    status = urllib2.urlopen(openURL, '').read()
    outJson = json.loads(status)

    return outJson

def stopStartServices(server, port, adminUser, adminPass, stopStart, serviceList, token=None):
    ''' Function to stop, start or delete a service.
    Requires Admin user/password, as well as server and port (necessary to construct token if one does not exist).
    stopStart = Stop|Start|Delete
    serviceList = List of services. A service must be in the <name>.<type> notation
    If a token exists, you can pass one in for use.
    '''

    # Get and set the token
    if token is None:
        token = gentoken(server, port, adminUser, adminPass)

    # Getting services from tool validation creates a semicolon delimited list that needs to be broken up
    services = serviceList.split(';')

    #modify the services(s)
    for service in services:
        service = urllib.quote(service.encode('utf8'))
        op_service_url = "http://{}:{}/arcgis/admin/services/{}/{}?token={}&f=json".format(server, port, service, stopStart, token)
        status = urllib2.urlopen(op_service_url, ' ').read()

        if 'success' in status:
            arcpy.AddMessage(str(service) + " === " + str(stopStart))
        else:
            arcpy.AddWarning(status)

    return