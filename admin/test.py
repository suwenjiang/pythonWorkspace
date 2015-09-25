__author__ = 'jiangmb'
from Get_site_information_helper import *
import json
import threading
import thread
def calc(jobID,cls):
    timeBegin=time.time()
    print "start check jobid"+jobID
    # cls=ADMINself("arcgis", "Super123", "192.168.220.167", "6080")   #check the jobid

    url3="http://192.168.220.167:6080/arcgis/rest/services/CopyFeatureMB2/GPServer/CopyFeatureMB2/jobs/%s?f=pjson"%jobID
    urlTest="http://localhost:6080/arcgis/rest/services/Model3/GPServer/Model/jobs/%s?f=pjson"%jobID

    # for i in range(1000):
    #     check_status=cls.sendAGSReq(urlTest,'')
    #     jobstatus=check_status['jobStatus']
    #     if(jobstatus)=='esriJobSucceeded':
    #         timeEnd=time.time()
    #         print threading.currentThread().name
    #         print str(threading.activeCount())
    #         print jobID+":total time====>"+str(timeEnd-timeBegin)
    #         return
    #     else:
    #         time.sleep(2)
    check_status=cls.sendAGSReq(urlTest,'')
    jobstatus=check_status['jobStatus']
    if(jobstatus)=='esriJobSucceeded':
        timeEnd=time.time()
        print threading.currentThread().name
        print str(threading.activeCount())
        print jobID+":total time====>"+str(timeEnd-timeBegin)
        return
    t=threading.Timer(1,calc,(jobID,cls))
    t.start()

def send_mutilple_request():
        for i in range(8):
            url="http://192.168.220.167:6080/arcgis/rest/services/CopyFeatureMB2/GPServer/CopyFeatureMB2/submitJob?f=pjson"
            urlTest="http://localhost:6080/arcgis/rest/services/Model3/GPServer/Model/submitJob"
            cls=ADMINself("arcgis", "Super123", "192.168.220.167", "6080")
            timeBegin=time.time()
            response=cls.sendAGSReq(urlTest,{'input':"m","f":"pjson"})
            jobID=response['jobId']
            t=threading.Thread(target=calc,name=str(i),args=(jobID,cls))
            t.start()


send_mutilple_request()
