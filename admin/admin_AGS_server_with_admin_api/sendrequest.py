__author__ = 'jiangmb'
from Get_site_information_helper import *
import json
import threading
import thread
def calc(jobID,cls,timeBegin):

    print "start check jobid"+jobID
    # cls=ADMINself("arcgis", "Super123", "192.168.220.167", "6080")   #check the jobid

    url3="http://192.168.220.167:6080/arcgis/rest/services/CopyFeatureMB2/GPServer/CopyFeatureMB2/jobs/%s?f=pjson"%jobID
    urlTest="http://192.168.100.202:6080/arcgis/rest/services/Buffer2/GPServer/Buffer/jobs/%s?f=pjson"%jobID
    count=0
    for i in range(4000):
        check_status=cls.sendAGSReq(urlTest,'')
        jobstatus=check_status['jobStatus']
        if(jobstatus)=='esriJobSucceeded':
            timeEnd=time.time()
            print threading.currentThread().name
            print str(threading.activeCount())
            print jobID+":total time====>"+str(timeEnd-timeBegin)
            return
        else:
            print jobID+str(count)
            time.sleep(10)
            count=count+1
    # check_status=cls.sendAGSReq(urlTest,'')
    # jobstatus=check_status['jobStatus']
    # if(jobstatus)=='esriJobSucceeded':
    #     timeEnd=time.time()
    #     print threading.currentThread().name
    #     print str(threading.activeCount())
    #     print jobID+":total time====>"+str(timeEnd-timeBegin)
    #     return
    # t=threading.Timer(10,calc,(jobID,cls,timeBegin))
    # t.start()

def send_mutilple_request():
        for i in range(21):
            url="http://192.168.100.202:6080/arcgis/rest/services/Buffer2/GPServer/Buffer/submitJob?buffer_distance_or_field=%7B%0D%0A+%22distance%22%3A+10000%2C%0D%0A+%22units%22%3A+%22esriMeters%22%0D%0A%7D&line_side=FULL&line_end_type=ROUND&dissolve_option=NONE&dissolve_field=%5B%5D&env%3AoutSR=&env%3AprocessSR=&returnZ=false&returnM=false&f=pjson"
            cls=ADMINself("arcgis", "Super123", "192.168.100.202", "6080")
            timeBegin=time.time()
            response=cls.sendAGSReq(url,'')
            jobID=response['jobId']
            t=threading.Thread(target=calc,name=str(i),args=(jobID,cls,timeBegin))
            t.start()


send_mutilple_request()
