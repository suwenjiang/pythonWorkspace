__author__ = 'jiangmb'
# -*- coding:UTF-8 -*-
import httplib, urllib, urllib2, json, sys,os, mimetypes
# import Machineosutils

def getMachineName(arcServerIp, arcServerPort, token):
    url = "http://"+arcServerIp+":"+arcServerPort+"/arcgis/admin/machines?token="+token+"&f=json"
    status = urllib2.urlopen(url).read()
    jsonResult = json.loads(status)
    machineName = jsonResult.get("machines")[0].get("machineName")
    print(machineName)
    return machineName

def edit(arcServerIp, arcServerPort, machineName, token):
    info1={
        "appServerMaxHeapSize": 1024,
        "machineName": machineName,
        "socMaxHeapSize": 256,
        "JMXPort": 4001,
        "HTTP": 6080,
        "NamingPort": 4003,
        "DerbyPort": 4004,
        "OpenEJBPort": 4002,
        "tcpClusterPort": 4005
        }
    params = urllib.urlencode(info1)
    url = "http://"+arcServerIp+":"+arcServerPort+"/arcgis/admin/machines/"+machineName+"/edit?token="+token+"&f=json"
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
        print("edit server appServerMaxHeapSize:"+url+",succeed")
        try:
            httpConn.close()
        except:
            print('httpConn.close catch Exception.')

        # Check that data returned is not an error object
        if not assertJsonSuccess(data):
            print('Error returned by operation. ' + str(data))
            return 255
        else:
            print('server appServerMaxHeapSize edit successfully')
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

def assertJsonSuccess(data):
    obj = json.loads(data)
    if 'status' in obj and obj['status'] == "error":
        print('Error: JSON object returns an error.' + str(obj))
        sys.exit(False)
    else:
        return True

if __name__ == '__main__':
    arcServerIp = Machineosutils.NastarServerPrivateIP
    arcServerPort = Machineosutils.ArcServerPort
    arcServerUser = Machineosutils.ArcServerUser
    Pkey = os.environ["ARCGISKEY"]
    arcServerKey = Pkey
    #get token
    token = getToken(arcServerUser, arcServerKey, arcServerIp, arcServerPort)
    if token in ("", None) :
        print('Could not generate a token with the username and password provided.')
        sys.exit(False)
    #get machine name
    machineName = getMachineName(arcServerIp, arcServerPort, token)
    print "begin."
    edit(arcServerIp, arcServerPort, machineName, token)

