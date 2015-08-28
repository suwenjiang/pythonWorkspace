#coding:cp936
__author__ = 'jiangmb'

from Get_site_information_helper import *

# server="localhost"
# port='6080'
# username='arcgis'
# password='Super123'
#
# operation='started'
# count=4


server=raw_input("请输入GIS服务器的IP地址:")
port=raw_input("请输入GIS连接的端口号，默认为6080。采用默认值请直接回车。")
if port=='':
    port='6080'
username=raw_input("请输入站点管理员用户名:")
password=raw_input("请输入管理员密码:")

operation=raw_input("请输入操作名(stopped/started)：")
if not str.upper(operation) in ('STARTED,STOPPED'):
    print "++++ERROR:请输入正确的操作!!!++++"
    sys.exit(1)
count=raw_input("请输入操作的服务数:")
adminself=ADMINself(username,password,server,port)

if str.upper(operation)=='STOPPED':

    serviceList=adminself.getStartedOrStopedServiceList('STARTED')
    if len(serviceList)<count:
        count=len(serviceList)
    adminself.stopStartServices('stop',adminself.getServiceList()[0:count])
else:
    serviceList=adminself.getStartedOrStopedServiceList('STOPPED')
    if len(serviceList)<count:
        count=len(serviceList)
    adminself.stopStartServices('start',adminself.getServiceList()[0:count])







