#coding:cp936
import os

import arcpy
import time
import sys

from createsddraft import *


class publishServices:

    def checkfileValidation(self,mxdLists):
        print "____开始检查文档的有效性...."
        file_to_be_published=[]
        for file in mxdLists:
            mxd=mapping.MapDocument(file)
            brknlist=mapping.ListBrokenDataSources(mxd)
            if not len(brknlist)==0:
                print "____地图文档,"+os.path.split(file)[1]+"损坏，无法发布服务...."
            else:
                file_to_be_published.append(file)
        print "____地图文档有效性检查完毕...."
        return file_to_be_published


    def publishServices(self,mxdLists,con,clusterName='default',copy_data_to_server=True,folder=None):


        for file in self.checkfileValidation(mxdLists):

            serviceName=os.path.splitext(os.path.split(file)[1])[0]

            print "____服务:"+serviceName+"开始创建服务定义文件...."
            clsCreateSddraft=CreateSddraft()
            sddraft=clsCreateSddraft.CreateSddraft(file,con,serviceName,copy_data_to_server,folder)
            print "____开始分析服务:"+serviceName+"...."
            analysis = arcpy.mapping.AnalyzeForSD(sddraft)
            dirName=os.path.split(file)[0]
            if analysis['errors'] == {}:
               print "____不存在错误，但是有如下提示信息。这些内容可能会影响服务性能...."
               print analysis['warnings']
               if(not self.checkWarnings(analysis['warnings'])):
                   try:
                        sd=dirName+"\\"+serviceName+".sd"
                        if(os.path.exists(sd)):
                            os.remove(sd)
                        arcpy.StageService_server(sddraft, sd)
                        print "____服务:"+serviceName+"打包成功...."
                        arcpy.UploadServiceDefinition_server(sd, con,in_cluster=clusterName)
                        print "____服务:"+str(serviceName)+"发布成功...."
                        os.remove(sd)
                   except Exception,msg:
                        print msg


               else:
                   print "____强烈建议，退出当前程序，去注册数据源。如不退出，6s后发布服务继续...."
                   time.sleep(10)
                   try:
                    sd=dirName+"\\"+serviceName+".sd"
                    if(os.path.exists(sd)):
                        os.remove(sd)
                    arcpy.StageService_server(sddraft, sd)
                    print "____打包成功...."
                    arcpy.UploadServiceDefinition_server(sd, con,in_cluster=clusterName)
                    print "____"+str(file)+"发布成功...."
                    os.remove(sd)
                   except Exception,msg:
                    print msg




            else:
                print '____存在如下错误:'+analysis['errors']+'....'
                print '____请先处理上述错误....'
                #五秒后退出控制台
                time.sleep(5)
                sys.exit(1)


    def  checkWarnings(self,warnings):
        for warning in warnings:
            if warning[1]==24011:
                print "____当前数据位置没有注册，数据会拷贝到服务器上,拷贝过程会影响发布速度...."
        return True

if __name__=='__main__':
    clsPublishservice=publishServices()
    fileList=['d:\\workspace\\testCopy.mxd', 'd:\\workspace\\test.mxd']
    contionfile=r"d:\localhost.ags"
    clusterName='default'
    servic_dir='test3'

    clsPublishservice.publishServices(fileList,contionfile,clusterName,copy_data_to_server=False,folder=servic_dir)
