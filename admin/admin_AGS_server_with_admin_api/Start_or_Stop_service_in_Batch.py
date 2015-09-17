#coding:cp936
__author__ = 'jiangmb'

from Get_site_information_helper import *

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


if __name__=="__main__":

    server="192.168.220.64"
    port='6080'
    username='arcgis'
    password='Super123'

    operation='stopped'
    count=400

    adminself=ADMINself(username,password,server,port)

    if str.upper(operation)=='STOPPED':

        serviceList=adminself.getStartedOrStopedServiceList('STARTED')
        print serviceList
        if len(serviceList)<count:
            count=len(serviceList)
        adminself.stopStartServices('stop',serviceList[0:count])
    else:
        serviceList=adminself.getStartedOrStopedServiceList('STOPPED')
        if len(serviceList)<count:
            count=len(serviceList)
        adminself.stopStartServices('start',serviceList[0:count])







