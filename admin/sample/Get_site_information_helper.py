#coding:cp936
__author__ = 'Administrator'

# Required imports
import urllib
import urllib2
import json
import sys
import time


class ADMINself(object):

    def __init__(self, username, password, server, port):
        self.username = username
        self.password = password
        self.server = server
        self.port= port
        self.token, self.expires, self.URL = self.getToken(username, password, server, port)
        self.basicQ = "?f=pjson&token={}".format(self.token)

    def getToken(self, username, password, server, port, exp=60):

        query_dict = {'username':   username,
                      'password':   password,
                      'expiration': str(exp),
                      'client':     'requestip',
                      'f': 'json'}

        tokenURL = "http://{}:{}/arcgis/admin/generateToken".format(server, port)
        token = self.sendAGSReq(tokenURL, query_dict)

        if "token" not in token:
            print token['messages']
            exit()
        else:
            # Return the token, expiry and URL
            return token['token'], token['expires'], "http://{}:{}/arcgis/admin".format(server, port)

    def checkExpiredToken(self):
        # call to check if token time limit has elapsed, if so, request a new one
        # server time in epoch values
        if (self.expires) < int(time.time() * 1000):
            self.token, self.expires, self.URL = self.getToken(self.username, self.password, self.server, self.port)
            print "Obtained new token"
        else:
            print "Token is still valid"



    def sendAGSReq(self,URL, query_dict):
    #
    # Takes a URL and a dictionary and sends the request, returns the JSON

        query_string = urllib.urlencode(query_dict)

        jsonResponse = urllib.urlopen(URL, urllib.urlencode(query_dict))
        jsonOuput = json.loads(jsonResponse.read())

        return jsonOuput
    
    def checkMSG(self,jsonMSG):
        #
        # Takes JSON and checks if a success message was found
    
        try:
            if jsonMSG['status'] == "success":
                return True
            else:
                return False
        except:
            return False



    def modifyLogs(self,clearLogs, logLevel):
        ''' Function to clear logs and modify log settings.
        clearLogs = True|False
        logLevel = SEVERE|WARNING|FINE|VERBOSE|DEBUG
        '''

        # Clear existing logs
        if clearLogs:
            clearStatus =self.sendAGSReq(self.URL + "/logs/clean" + self.basicQ, '')
            if self.checkMSG(clearStatus['status']):
                print "Cleared log files"
           
        # Get the current logDir, maxErrorReportsCount and maxLogFileAge as we dont want to modify those
        logSettings = self.sendAGSReq(self.URL + "/logs/settings" + self.basicQ, '')
        logSettingProps = logSettings['settings']

        # Place the current settings, along with new log setting back into the payload
        logLevel_dict = {"logDir": logSettingProps['logDir'],
                         "logLevel": logLevel,
                         "maxErrorReportsCount": logSettingProps['maxErrorReportsCount'],
                         "maxLogFileAge": logSettingProps['maxLogFileAge']
                        }

        # Modify the logLevel
        logStatus = self.sendAGSReq(self.URL + "/logs/settings/edit" + self.basicQ, logLevel_dict)

        if self.checkMSG(logStatus):
            print "Successfully changed log level to {}".format(logLevel)
        else:
            print "Log level not changed:\n" + logStatus

        return


    def createFolder(self,folderName, folderDescription):
        ''' Function to create a folder
        folderName = String with a folder name
        folderDescription = String with a description for the folder
        '''

        # Dictionary of properties to create a folder
        folderProp_dict = { "folderName": folderName,
                            "description": folderDescription
                          }

        folder_encode = urllib.urlencode(folderProp_dict)
        folderStatus = self.sendAGSReq(self.URL + "/services/createFolder" + self.basicQ, folderProp_dict)

        if self.checkMSG(folderStatus):
            print "Created folder: {}".format(folderName)
        else:
            print "Could not create folder:\n" + str(folderStatus)

        return


    def getFolders(self):
        ''' Function to get all folders on a server
        '''

        foldersList = self.sendAGSReq(self.URL + "/services" + self.basicQ, '')
        folders = foldersList["folders"]

        # Return a list of folders to the function which called for them
        return folders


    def renameService(self,service, newName):
        ''' Function to rename a service
        service = String of existing service with type separated by a period <serviceName>.<serviceType>
        newName = String of new service name
        '''

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

        renameStatus = self.sendAGSReq(self.URL + "/services/renameService" + self.basicQ, renameService_dict)

        if self.checkMSG(renameStatus):
            print "Successfully renamed service to : {}".format(newName)
        else:
            print "Could not rename service:\n" + renameStatus

        return


    def stopStartServices(self,stopStart, serviceList):
        ''' Function to stop, start or delete a service.
        stopStart = Stop|Start|Delete
        serviceList = List of services. A service must be in the <name>.<type> notation        '''

        # modify the services(s)
        for service in serviceList:
            status = self.sendAGSReq(self.URL + "/services/{}/{}".format(service, stopStart) + self.basicQ, '')

            if self.checkMSG(status):
                print (str(service) + " === " + str(stopStart))
            else:
                print status

        return



    def getServiceList(self):
        ''' Function to get all services
        Note: Will not return any services in the Utilities or System folder
        '''

        services = []
        folder = ''
        serviceList = self.sendAGSReq(self.URL + "/services" + self.basicQ, '')

        # Build up list of services at the root level
        for single in serviceList["services"]:
            services.append(single['serviceName'] + '.' + single['type'])

        # Build up list of folders and remove the System and Utilities folder (we dont want anyone playing with them)
        folderList = serviceList["folders"]
        folderList.remove("Utilities")
        folderList.remove("System")

        for folder in folderList:
            fList = self.sendAGSReq(self.URL + "/services/{}".format(folder) + self.basicQ, '')
            for single in fList["services"]:
                services.append(folder + "/" + single['serviceName'] + '.' + single['type'])

        #print services
        return services

    def getStartedOrStopedServiceList(self,startstop="started"):
        """get the started or
        stopped services list
        """
        #get all the user services in site
        URL="http://{}:{}/arcgis/rest/services".format(self.server,self.port)
        allServices=self.getServiceList()

        services=[]
        # get the started services in site
        serviceList=self.sendAGSReq(URL+self.basicQ,'')
        for single in serviceList["services"]:

            services.append(single['name'] + '.' + single['type'])

        # Build up list of folders and remove the System and Utilities folder (we dont want anyone playing with them)
        folderList = serviceList["folders"]
        folderList.remove("Utilities")
        folderList.remove("System")
        for folder in folderList:
            fList = self.sendAGSReq(URL + "/"+(folder) + self.basicQ, '')
            for single in fList["services"]:
                services.append(single['name']+ '.' + single['type'])

        if(str.lower(startstop)=='started'):


            return services
        else:
            stoppedservice=[i for i in allServices if i not in services]

            return stoppedservice

    def getServiceListInCluster(self,clusterName):

        '''
        :param clusterName:
        :return:
        '''

        service=[]
        result=self.sendAGSReq(self.URL+"/clusters/{}/services".format(clusterName)+self.basicQ,'')
        for single in result['services']:
            if single['folderName']=="/":

                service.append(single['serviceName'] + '.' + single['type'])
            else:
                service.append(single['folderName']+"//"+single['serviceName'] + '.' + single['type'])

        return service

    def getServerInfo(self):
        ''' Function to get and display a detailed report about a server
        '''

        report = ''
        report += "*-----------------------------------------------*\n\n"

        # Get Cluster and Machine info
        jCluster = self.sendAGSReq(self.URL + "/clusters" + self.basicQ, '')
        if len(jCluster["clusters"]) == 0:
            report += "No clusters found\n\n"
        else:
            for cluster in jCluster["clusters"]:
                report += "Cluster: {} is {}\n".format(cluster["clusterName"], cluster["configuredState"])
                if len(cluster["machineNames"])== 0:
                    report += "No machines associated with cluster\n"
                else:
                    # Get individual Machine info
                    for machine in cluster["machineNames"]:
                        jMachine = self.sendAGSReq(self.URL + "/machines/{}".format(machine) + self.basicQ, '')
                        report += "    Machine: {} is {}. (Platform: {})\n".format(machine, jMachine["configuredState"],jMachine["platform"])


        # Get Version and Build
        jInfo = self.sendAGSReq(self.URL + "/info" + self.basicQ, '')
        report += "\nVersion: {}\nBuild:   {}\n\n".format(jInfo ["currentversion"], jInfo ["currentbuild"])


        # Get Log level
        jLog = self.sendAGSReq(self.URL + "/logs/settings" + self.basicQ, '')
        report += "Log level: {}\n\n".format(jLog["settings"]["logLevel"])


        #Get License information
        jLicense = self.sendAGSReq(self.URL + "/system/licenses" + self.basicQ, '')
        report += "License is: {} / {}\n".format(jLicense["edition"]["name"], jLicense["level"]["name"])
        if jLicense["edition"]["canExpire"] == True:
            import datetime
            d = datetime.date.fromtimestamp(jLicense["edition"]["expiration"] // 1000) #time in milliseselfds since epoch
            report += "License set to expire: {}\n".format(datetime.datetime.strftime(d, '%Y-%m-%d'))
        else:
            report += "License does not expire\n"


        if len(jLicense["extensions"]) == 0:
            report += "No available extensions\n"
        else:
            report += "Available Extensions........\n"
            for name in jLicense["extensions"]:
                report += "extension:  {}\n".format(name["name"])

        report += "\n*-----------------------------------------------*\n"

        print report


    def securityReport(self):
        ''' Get the security settings on the Server
        '''

        securityReport = self.sendAGSReq(self.URL + "/security/selffig" + self.basicQ, '')

        print "\n  ==Security settings==\n"
        for k, v in securityReport.iteritems():
            if type(v) == dict:
                print "{0}...".format(k)
                for sK, sV in v.iteritems():
                    print "{0:14}{1:13} : {2}".format(" ", sK, sV)
            else:
                print "{0:27} : {1}".format(k, v)

        return


    def listRoles(self):
        ''' List all the current roles on the Server
        '''

        roleList = self.sendAGSReq(self.URL + "/security/roles/getRoles" + self.basicQ, '')

        if len(roleList['roles']) == 0:
            print "\nNo Roles found. Is security enabled?"
        else:
            print "\n___Roles___"
            for role in roleList['roles']:
                for k, v in role.iteritems():
                    if k == 'rolename':
                        print v
                    if k == 'description':
                        print " ... {0}".format(v)

        return


    def listUsers(self):
        ''' List all the users in the server security store
        '''

        userList =self.sendAGSReq(self.URL + "/security/users/getUsers" + self.basicQ, '')

        if len(userList['users']) == 0:
            print "No Users found. Is security enabled?"
        else:
            print "\n___Users___"
            for user in userList['users']:
                for k, v in user.iteritems():
                    print "{0:11} : {1}".format(k, v)

        return


    def listUsersInRole(self,role):
        ''' List all users that belong to a given role
        '''

        userList =self.sendAGSReq(self.URL + "/security/roles/getUsersWithinRole" + self.basicQ, {"rolename": role})
        if len(userList['users']) >0:
            print "Found these users in '{0}' role...".format(role)
            for user in userList['users']:
                print user
        else:
            print "No users found in '{0}' role".format(role)


    def listRolesByUser(self,user):
        ''' List all roles that a given user belongs to
        '''

        roleList =self.sendAGSReq(self.URL + "/security/roles/getRolesForUser" + self.basicQ, {"username": user})
        if len(roleList['roles']) >0:
            print "Found these roles for '{0}'...".format(user)
            for role in roleList['roles']:
                print role
        else:
            print "No roles found for '{0}'".format(user)


    def exportSite(self,pathToExport):
        ''' Export (make a backup) of the AGS Site.
        A directory is given, the file will be created with the date and suffix of .agssite
        '''

        exportJSON =self.sendAGSReq(self.URL + "/exportSite" + self.basicQ, {"location": pathToExport})
        if self.checkMSG(exportJSON):
            print "Exported site to {0}".format(exportJSON['location'])
        else:
            print exportJSON

    def getServiceConfig(self,serviceName):
        result=self.sendAGSReq(self.URL+"/services/{}".format(serviceName)+self.basicQ,'')
        return result
    def updateServiceConfig(self,serviceName,config):

        url=self.URL+"/services/{}/edit".format(serviceName)+self.basicQ
        result =self.sendAGSReq(url,config)
        return result

if __name__=="__main__":
    con=ADMINself("arcgis","Super123","localhost","6080")
