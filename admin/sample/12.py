__author__ = 'jiangmb'
from Get_site_information_helper import *
import json
import threading
import thread
def calc(jobID,timeBegin):
    print "start check jobid"+jobID
    cls=ADMINself("arcgis", "Super123", "192.168.220.167", "6080")   #check the jobid

    url3="http://192.168.100.202:6080/arcgis/rest/services/CopyFeatureMB_2/GPServer/CopyFeatureMB_2/jobs/%s?f=pjson"%jobID

    for i in range(1000):
        check_status=cls.sendAGSReq(url3,'')
        jobstatus=check_status['jobStatus']
        if(jobstatus)=='esriJobSucceeded':
            timeEnd=time.time()
            print jobID+":total time====>"+str(timeEnd-timeBegin)
            return
        else:
            time.sleep(10)

def send_mutilple_request():

        url="http://192.168.100.202:6080/arcgis/rest/services/CopyFeatureMB_2/GPServer/CopyFeatureMB_2/submitJob?f=pjson"
        urlTest="http://localhost:6080/arcgis/rest/services/Model3/GPServer/Model/submitJob"
        cls=ADMINself("arcgis", "Super123", "192.168.100.202", "6080")
        timeBegin=time.time()
        response=cls.sendAGSReq(url,'')
        jobID=response['jobId']
        calc(jobID,timeBegin)

send_mutilple_request()