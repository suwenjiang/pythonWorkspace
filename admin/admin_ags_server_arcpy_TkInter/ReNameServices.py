# -*-coding:utf-8 -*-
__author__ = 'jmb'

from Tkinter import *
from  ttk import *
from tkFileDialog import *
import sys

from admin_ags_server_arcpy_TkInter.mapHelper import *
from ExceptionCatcher import *

reload(sys)
sys.setdefaultencoding('utf8')

class Rename_Service:

    def __init__(self,root):
       self.url=StringVar()
       self.adminName=StringVar()
       self.password=StringVar()
       self.old_name=StringVar()
       self.new_name=StringVar()
       self.port=StringVar()

       self.Rename_Service_UI(root)
    def Rename_Service_UI(self,root):
        ''''发布单独的mxd文件 '''
        w=root.winfo_screenwidth()/4
        h=root.winfo_screenheight()/4
        frm=Toplevel()
        frm.title('ReName Services')
        frm.geometry('600x300+%d+%d'%(w,h))
        frm.grab_set()
        frm.transient(root)

        Grid.rowconfigure(frm,0,weight=1)
        Grid.columnconfigure(frm,0,weight=1)


        labelFrame=LabelFrame(frm,text="Parameters")
        labelFrame.grid(row=0,column=0,sticky="NESW")

        for x in range(0,10):
            Grid.rowconfigure(labelFrame,x,weight=1)
        Grid.columnconfigure(labelFrame,0,weight=1)
        Grid.columnconfigure(labelFrame,1,weight=1)

        labelurl=Label(labelFrame,text="Server")
        labelurl.grid(row=0,column=0,columnspan=2,sticky='W')

        labelurl2=Label(labelFrame,text="Port")
        labelurl2.grid(row=0,column=1,sticky='N')


        txt_url=Entry(labelFrame,textvariable=self.url)

        txt_url.grid(row=1,column=0,columnspan=2,sticky="WN")

        self.port.set("6080")
        txt_port=Entry(labelFrame,textvariable=self.port)
        txt_port.grid(row=1,column=1,columnspan=2,sticky='EN')

        label_userName=Label(labelFrame,text="ags server admin username")
        label_userName.grid(row=2,column=0,sticky="W")
        txt_userName=Entry(labelFrame,textvariable=self.adminName)
        txt_userName.grid(row=3,column=0,columnspan=2,sticky="WNE")



        label_password= Label(labelFrame,text='ags server admin password')
        label_password.grid(row=4,column=0,sticky="WN")
        txt_password=Entry(labelFrame, show="*",textvariable= self.password)
        txt_password.grid(row=5,column=0,columnspan=2,sticky="WNE")


        label_oldName= Label(labelFrame,text='choose a service need to be renamed:')
        label_oldName.grid(row=6,column=0,sticky="WN")


        button_getOldService=Button(labelFrame,text="GetServiceName",command=lambda:self.getServiceName(cb))
        button_getOldService.grid(row=7,column=0,sticky="w")

        cb=Combobox(labelFrame)
        cb.grid(row=7,column=1,sticky="NE")

        label_newName=Label(labelFrame,text='new service name:')
        label_newName.grid(row=8,column=0,sticky="WN")
        txtname=Entry(labelFrame,textvariable = self.new_name)
        txtname.grid(row=9,column=0,columnspan=2,sticky="WNE")


        group2 = LabelFrame(frm, text="工具使用说明",width=200)
        group2.grid(row=0,column=1,sticky="NSEW")

        Grid.rowconfigure(group2,0,weight=1)
        Grid.columnconfigure(group2,0,weight=1)
        textdd="该工具用来重命名服务名\n1.参数1为site的管理员用户名\n2.参数2为site管理员密码\n3.参数3为旧服务名\n4.新的服务名"
        w3=Label(group2,text=textdd).grid(row=0,column=0,sticky="NW")

        btnOk=Button(frm,text='ExcuteReName', command=lambda:self.Excute(cb)).grid(row=1,column=0)
        btnCancle=Button(frm,text='Cancle',command=lambda: self.doCance(frm)).grid(row=1,column=1)

        tk.CallWrapper=Catcher

    def Excute(self,cb):

        renameService(self.url.get(),self.port.get(),self.adminName.get(),self.password.get(),cb.get(),self.new_name.get())

        showinfo("success","服务名更改成功！*——*")

    def doCance(self,frm):
        frm.destroy()

    def selct_conn_file(self):

        file=askopenfilename(defaultextension=".ags")
        if file:
            self.vConfile.set(file)

    def Browsfile(self):
         file=askopenfilename(defaultextension=".mxd")
         if file:
             self.mxdPath.set(file)

    def getServiceName(self,cb):
        rootservices=getServiceList(self.url.get(),self.port.get(),self.adminName.get(),self.password.get())

        cb["value"]=[]
        cb.set("")
        cb["value"]=rootservices

        # result_folder=getfolder(self.url.get(),self.adminName.get(),self.password.get())
        # #
        # for folderName in result_folder:
        #     if(folderName!="Utilities" or folderName!="System"):
        #          rootservices+=getServiceInfolder(self.url.get(),self.adminName.get(),self.password.get(),folderName)

if __name__ == "__main__":

    def show(root):
        app=Rename_Service(root)


    root=Tk()
    Button(root,text="clickme",command=lambda:show(root)).grid(row=0,column=0)
    root.mainloop()
