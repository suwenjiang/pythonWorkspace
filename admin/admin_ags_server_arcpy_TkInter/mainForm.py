# -*-coding:utf-8 -*-
__author__ = 'jmb'

from s1_create_conn_file import *
from Publishfiles import *
from admin_ags_server_arcpy_TkInter.createSDEFileUI import *
from admin_ags_server_arcpy_TkInter.replaceSDEConnection import *
from admin_ags_server_arcpy_TkInter.PublishSingleService import *
from admin_ags_server_arcpy_TkInter.CreateMsd import *
from admin_ags_server_arcpy_TkInter.ReNameServices import *
from DoMutiplePublish import *
from admin_ags_server_arcpy_TkInter.ReportServerInfo import *
root=Tk()
root.title('ArcGIS for Server Administrate mini tools')
def callback():

    app=clCreateServerConntionFile(root)
def create_msd_file():
    app=Create_msd_file(root)
def callbackBatchPublish():
    app=MutipleServicePublish(root)
def check_Server_Connection_file():
        confilePath=os.getcwd()
        for root,dirname, files in os.walk(confilePath):
             list=[]
             for file in files:
                if os.path.splitext(file)[1]=='.ags':
                    list.append(file)
                return os.path.join(root,file)
             if len(list)==0:
                  showerror("error","在当前目录下不到Server连接文件，请先创建连接文件")
             return None
def create_sde_file():
     app=cls_create_sde_file(root)
def replace_sde_file():
    app=cls_replace_sde_file(root)
def Publish_sigle_life():
    app=Publish_Single_Service(root)
def ReName_Service():

   app=Rename_Service(root)
def Report_server_info():
    app=reportServerInfo(root)

Button(root,text='Creat ags file',command=callback).grid(row=0,column=0,sticky="WE")
Button(root,text="Create sde file",command=create_sde_file).grid(row=1,column=0,sticky="WE")
Button(root,text='Create msd file',command=create_msd_file).grid(row=2,column=0,sticky="WE")
Button(root,text='BatchPublish',command=callbackBatchPublish).grid(row=3,column=0,sticky="WE")
Button(root,text="Replace Sde Source",command=replace_sde_file).grid(row=4,column=0,sticky="WE")
Button(root,text='Publish Single file',command=Publish_sigle_life).grid(row=5,column=0,sticky="WE")
Button(root,text='ReName Services',command=ReName_Service).grid(row=6,column=0,sticky="WE")
Button(root,text='Report Server Info',command=Report_server_info).grid(row=7,column=0,sticky="WE")
lbframe=LabelFrame(root,text="关于本工具箱")
lbframe.grid(row=0,column=1,rowspan=8,sticky="NSWE")
textstring="Server管理工具箱\n\n简介：该工具箱有python开发，可以用来批量的发布服务，修复服务等\n\n作者：江民彬\n\n 联系:jiangmb@esrichina.com.cn"
label=Label(lbframe,text=textstring).grid(row=0,column=1,sticky="NSWE")

root.mainloop()


