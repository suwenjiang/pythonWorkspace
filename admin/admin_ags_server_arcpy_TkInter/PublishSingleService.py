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

class Publish_Single_Service:

    def __init__(self,root):
       self.vConfile=StringVar()
       self.ServiceName=StringVar()
       self.mxdPath=StringVar()
       self.Publish_Single_Mxd_UI(root)

    def Publish_Single_Mxd_UI(self,root):
        ''''发布单独的mxd文件 '''
        w=root.winfo_screenwidth()/4
        h=root.winfo_screenheight()/4
        frm=Toplevel()
        frm.title('Single Sevices Publish')
        frm.geometry('600x300+%d+%d'%(w,h))
        frm.grab_set()
        frm.transient(root)

        Grid.rowconfigure(frm,0,weight=1)
        Grid.columnconfigure(frm,0,weight=1)


        labelFrame=LabelFrame(frm,text="Publish Service")
        labelFrame.grid(row=0,column=0,sticky="NESW")


        for x in range(0,10):
            Grid.rowconfigure(labelFrame,x,weight=1)
        Grid.columnconfigure(labelFrame,0,weight=1)
        Grid.columnconfigure(labelFrame,1,weight=1)

        label_agsFile=Label(labelFrame,text="arcgis server connection file")
        label_agsFile.grid(row=0,column=0,sticky="W")
        txt_ags=Entry(labelFrame,textvariable=self.vConfile)
        txt_ags.grid(row=1,column=0,columnspan=2,sticky="WNE")

        btnBroswer1=Button(labelFrame,text="Broswer",command=self.selct_conn_file)
        btnBroswer1.grid(row=1,column=1,sticky="EN")

        labelurl= Label(labelFrame,text='Service Name:')
        labelurl.grid(row=2,column=0,sticky="WN")
        txturl=Entry(labelFrame,textvariable= self.ServiceName)
        txturl.grid(row=3,column=0,columnspan=2,sticky="WNE")


        labelurl= Label(labelFrame,text='Service type:')
        labelurl.grid(row=4,column=0,sticky="WN")
        cb=Combobox(labelFrame)
        cb["value"]=["MapServer"]
        cb.set("MapServer")
        cb.grid(row=5,column=0,columnspan=2,sticky="WEN")

        labelname=Label(labelFrame,text='Data Source Path:')
        labelname.grid(row=6,column=0,sticky="WN")
        txtname=Entry(labelFrame,textvariable = self.mxdPath)
        txtname.grid(row=7,column=0,columnspan=2,sticky="WNE")
        btnBroswer=Button(labelFrame,text="Broswer", command=self.Browsfile)
        btnBroswer.grid(row=7,column=1,sticky="NE")

        group2 = LabelFrame(frm, text="工具使用说明",width=200)
        group2.grid(row=0,column=1,sticky="NSEW")

        Grid.rowconfigure(group2,0,weight=1)
        Grid.columnconfigure(group2,0,weight=1)
        textdd="该工具用来发布单个服务\n\n且默认采用数据库链接\n\n1.arcgis server connection file 为连接server文件\n\n如test.ags\n2.Service Name，服务名\n\n3.service tpye 为发布服务类型\n\n4.Data Source Path待发布数据"
        w3=Label(group2,text=textdd).grid(row=0,column=0,sticky="NW")

        btnOk=Button(frm,text='Publish', command=self.DoPublish).grid(row=1,column=0)
        btnCancle=Button(frm,text='Cancle',command=lambda: self.doCance(frm)).grid(row=1,column=1)
        tk.CallWrapper=Catcher

    def DoPublish(self):
         mapDocPath=self.mxdPath.get()
         serviceName=self.ServiceName.get()
         #get ags file in current dir
         ags_conn_file=self.vConfile.get()
         if(checkMxdValidation(mapDocPath)):
            PublishService(mapDocPath,serviceName,ags_conn_file)
            showinfo("success","发布成功！")
         else:
             showerror("error","data source is broken\nplease repair the data source")


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

if __name__ == "__main__":

    def show(root):
        app=Publish_Single_Service(root)


    root=Tk()
    Button(root,text="clickme",command=lambda:show(root)).grid(row=0,column=0)
    root.mainloop()
