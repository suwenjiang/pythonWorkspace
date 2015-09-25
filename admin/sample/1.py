__author__ = 'jiangmb'
from Get_site_information_helper import *
import json
import threading
import thread
def calc():
    url="http://192.168.100.202:6080/arcgis/rest/services/Buffer2/GPServer/Buffer/submitJob?buffer_distance_or_field=%7B%0D%0A+%22distance%22%3A+10000%2C%0D%0A+%22units%22%3A+%22esriMeters%22%0D%0A%7D&line_side=FULL&line_end_type=ROUND&dissolve_option=NONE&dissolve_field=%5B%5D&env%3AoutSR=&env%3AprocessSR=&returnZ=false&returnM=false&f=pjson"
    cls=ADMINself("arcgis", "Super123", "192.168.100.202", "6080")
    timeBegin=time.time()
    #get the gometries:

    response=cls.sendAGSReq(url,'')
    print response

def send_mutilple_request():
        for i in range(1):
            t=threading.Thread(target=calc,name=str(i))
            t.start()

send_mutilple_request()
