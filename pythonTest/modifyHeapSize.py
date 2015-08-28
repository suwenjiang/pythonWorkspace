__author__ = 'jiangmb'
# -*- coding:UTF-8 -*-
import httplib, urllib, urllib2, json, sys, mimetypes

def getMachineName(arcServerIp, arcServerPort, token):
    url = "http://{}:{}/arcgis/admin/machines?token={}&f=json".format(arcServerIp, arcServerPort, token)
    status = urllib2.urlopen(url).read()
    jsonResult = json.loads(status)
    machineName = jsonResult.get("machines")[0].get("machineName")
    print(machineName)
    return machineName

def edit(arcServerIp, arcServerPort, machineName, token):
    info1={
        "appServerMaxHeapSize": 1024,
        "webServerSSLEnabled": False,
        "webServerMaxHeapSize": -1,
        "webServerCertificateAlias": "SelfSignedCertificate",
           "machineName": machineName,
            "socMaxHeapSize": 256,
        "synchronize": False,
        "JMXPort": 4001,
        "NamingPort": 4003,
        "DerbyPort": 4004,
        "OpenEJBPort": 4002,
        "tcpClusterPort": 4005
        }
    # result=getTheMachineInof()
    #
    # result['appServerMaxHeapSize']=256
    # result['JMXPort']=4000
    # result['OpenEJBPort']=4001
    # result['NamingPort']=4002
    # result['DerbyPort']=4003
    # result['tcpClusterPort']=4004
    # print result
    # info1=str(json.dumps(result))
    #
    # print info1

    params = urllib.urlencode(info1)

    print params

    url = "http://{}:{}/arcgis/admin/machines/{}/edit?token={}&f=json".format(arcServerIp, arcServerPort, machineName, token)
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

    httpConn = httplib.HTTPConnection(arcServerIp, arcServerPort)
    httpConn.request("POST", url, params, headers)

    # Read response
    response = httpConn.getresponse()
    if (response.status != 200):
        httpConn.close()
        print('Error while creating the site.')
        return 255
    else:
        data = response.read()
        print("edit server recycleStartTime:"+url+",succeed")
        try:
            httpConn.close()
        except:
            print('httpConn.close catch Exception.')

        # Check that data returned is not an error object
        if not assertJsonSuccess(data):
            print('Error returned by operation. ' + str(data))
            return 255
        else:
            print('server recycleStartTime edit successfully')
        return 0

def getToken(arcServerUser, arcServerKey, arcServerIp, arcServerPort):
    tokenURL = "/arcgis/admin/generateToken"
    params = urllib.urlencode({'username': arcServerUser, 'password': arcServerKey, 'client': 'requestip', 'f': 'json'})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    print('start getToken')
    # Connect to URL and post parameters
    httpConn = httplib.HTTPConnection(arcServerIp, arcServerPort)
    httpConn.request("POST", tokenURL, params, headers)
    # Read response
    response = httpConn.getresponse()
    if (response.status != 200) :
        httpConn.close()
        print('Error while fetching tokens from admin URL. Please check the URL and try again.')
        return
    else:
        data = response.read()
        httpConn.close()
        # Check that data returned is not an error object
        if not assertJsonSuccess(data) :
            return
        # Extract the token from it
        token = json.loads(data)
        return token['token']
def sendAGSReq(URL, query_dict):
        #
        # Takes a URL and a dictionary and sends the request, returns the JSON

        query_string = urllib.urlencode(query_dict)

        jsonResponse = urllib.urlopen(URL, urllib.urlencode(query_dict))
        jsonOuput = json.loads(jsonResponse.read())

        return jsonOuput

def assertJsonSuccess(data):
    obj = json.loads(data)
    if 'status' in obj and obj['status'] == "error":
        print('Error: JSON object returns an error.' + str(obj))
        sys.exit(False)
    else:
        return True
def getTheMachineInof():

    url="http://192.168.100.251:6080/arcgis/admin/machines/SUSEGIS/?token={}&f=pjson".format(token)
    #url="http://localhost:6080/arcgis/admin/machines/JIANGMB.ESRICHINA.COM/?token={}&f=pjson".format(token)
    result=sendAGSReq(url,'')
    return result

if __name__ == '__main__':
    arcServerIp = "192.168.100.251"
    arcServerPort = "6080"
    arcServerUser = "arcgis"
    arcServerKey = "Super123"
    #get token
    token = getToken(arcServerUser, arcServerKey, arcServerIp, arcServerPort)
    if token in ("", None) :
        print('Could not generate a token with the username and password provided.')
        sys.exit(False)
    #get machine name
    machineName = getMachineName(arcServerIp, arcServerPort, token)
    print "gis"
    edit(arcServerIp, arcServerPort, machineName, token)
