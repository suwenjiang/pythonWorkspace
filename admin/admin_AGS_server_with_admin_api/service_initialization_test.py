#coding:cp936
__author__ = 'jiangmb'
from Get_site_information_helper import *
import datetime


# server=raw_input("请输入GIS服务器的Ip:")
# port=raw_input("请输入GIS连接的端口号，默认为6080。采用默认值请直接回车。")
# if port=='':
#     port='6080'
# username=raw_input("请输入站点管理员用户名:")
# password=raw_input("请输入管理员密码:")
# path=raw_input("请输入结果文件保存地址:")


server="localhost"
port='6080'
username='arcgis'
password='Super123'
path='d:\\'


def writeOutPut(path,contents):
    file=open(path,'w')
    file.write("服务名,初始化时间(ms)\n")
    for content in contents:
      line=content[0].encode('utf-8')+","+str(content[1]).encode('utf-8')+"\n"
      file.write(line)

    file.close()

adminself=ADMINself(username,password,server,port)
serviceList=adminself.getStartedOrStopedServiceList()
if (len(serviceList)==0):
    print "++++++++当前服务器没有服务可以初始化:+++++++"
    sys.exit(1)
Dict_service={}
for singleService in serviceList:
    newname=singleService.replace('.','/')
    if "//" in newname:
       newname=newname.replace('//','/')
    url="http://{}:{}/arcgis/rest/services/{}".format(server,port,newname)

    timeStart=datetime.datetime.now()
    results= adminself.sendAGSReq(url+adminself.basicQ,"")
    if results is None:
        print "++++++++"+singleService+" has an error in initialization+++++++"
    else:
        timeEnd=datetime.datetime.now()
        timeElapse=(timeEnd-timeStart).microseconds/1000
        print "++++++++"+singleService+" spent:"+str(timeElapse)+" ms in initialization++++++++"
        Dict_service[singleService]=timeElapse

#对字典进排序
results=sorted(Dict_service.items(), key=lambda Dict_service:Dict_service[1])
writeOutPut(path+"\\result.txt",results)
