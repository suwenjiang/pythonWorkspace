
# -*-coding:utf-8 -*-
__author__ = 'jmb'

from Tkinter import  *
import tkMessageBox
from  ttk import *
from tkFileDialog import *
import os

import arcpy

from admin_ags_server_arcpy_TkInter.ExceptionCatcher import *

reload(sys)
sys.setdefaultencoding('utf8')
class cls_create_sde_file:



    def __init__(self,root):
        self.root=root

        self.strfileName=StringVar()
        self.strInstance=StringVar()
        self.strUserName=StringVar()
        self.strPassword=StringVar()
        self.save_path=StringVar()
        self.strDataBase=StringVar()
        self.create_sde_file()

    def selectValueChang(self,pCombox,pEntryDB):
        database=pCombox.get()
        if(database=="SqlServer"):
            pEntryDB.config(state="Normal")
        else:
            pEntryDB.config(state="disable")
    def selectPath(self):

        file=asksaveasfilename(defaultextension=".sde")
        if file:
            self.save_path.set(file)

    def doCreateFile(self,pCombox):

        out_name=self.strfileName.get() #sde文件的名称
        if(out_name is None):
            tkMessageBox.showinfo("error","请输入sde文件名")
            return

        instance=self.strInstance.get()
        if(instance is None):
            tkMessageBox.showinfo("error","请输入sde文件名")
            return
        username=self.strUserName.get()
        password=self.strPassword.get()
        #
        database=pCombox.get()
        file_output_folder=os.path.split(self.save_path.get())[0]
        out_name=os.path.split(self.save_path.get())[1]
        if(database=="SqlServer"):
            db=self.strDataBase.get()
            result=arcpy.CreateDatabaseConnection_management(file_output_folder,out_name,"SQL_SERVER",instance,"DATABASE_AUTH",username, password, "SAVE_USERNAME",db)
        else:
            result=arcpy.CreateDatabaseConnection_management(file_output_folder,out_name,"ORACLE",instance,"DATABASE_AUTH",username, password, "SAVE_USERNAME")

        tkMessageBox.showinfo("info","创建成功")



    def doCance(self,frm):
        frm.destroy()
    def create_sde_file(self):

        w=self.root.winfo_screenwidth()/4
        h=self.root.winfo_screenheight()/4
        frm=Toplevel()
        frm.title(' Batch Sevices Publish')
        frm.geometry('600x300+%d+%d'%(w,h))
        frm.grab_set()
        frm.transient(self.root)
        Grid.rowconfigure(frm,0,weight=1)
        Grid.columnconfigure(frm,0,weight=1)
        Grid.columnconfigure(frm,1,weight=1)

        group = LabelFrame(frm, text="输入相关的参数")
        group.grid(row=0,column=0,sticky="NESW")

        for x in range(10):
            Grid.rowconfigure(group,x,weight=1)

            Grid.columnconfigure(group,0,weight=1)

        label1=Label(group,text="ArcSDE connection fullPath")
        label1.grid(row=0,column=0,sticky="W")





        en1=Entry(group,textvariable=self.save_path)
        en1.grid(row=1,column=0,sticky="WEN")
        btn=Button(group,text="Broswer",command=self.selectPath)
        btn.grid(row=1,column=1,sticky="WE")

        label2=Label(group,text="Database Platform")
        label2.grid(row=2,column=0,sticky="WN")


        cb=Combobox(group)
        cb["value"]=["Oracl","SqlServer"]
        cb.set("Oralce")

        cb.grid(row=3,column=0,columnspan=2,sticky="WEN")



        label3= Label(group,text="Instance")
        label3.grid(row=4,column=0,sticky="WN")
        en3= Entry(group,textvariable=self.strInstance)
        en3.grid(row=5,column=0,columnspan=2,sticky="WEN")

        label4= Label(group,text="UserName")
        label4.grid(row=6,column=0,sticky="WN")
        en4= Entry(group,textvariable=self.strUserName)
        en4.grid(row=7,column=0,columnspan=2,sticky="WEN")

        label5= Label(group,text="PassWord")
        label5.grid(row=8,column=0,sticky="WN")
        en5= Entry(group,show="*",textvariable=self.strPassword)
        en5.grid(row=9,column=0,columnspan=2,sticky="WEN")

        label6= Label(group,text="DataBase")
        label6.grid(row=10,column=0,sticky="W")
        en6= Entry(group,textvariable=self.strDataBase)
        en6.grid(row=11,column=0,columnspan=2,sticky="WE")

        en6.config(state="disable")

        group2 = LabelFrame(frm, text="工具使用说明",width=200)
        group2.grid(row=0,column=1,sticky="NSEW")

        Grid.rowconfigure(group2,0,weight=1)
        Grid.columnconfigure(group2,0,weight=1)
        textdd="改工具用来创建sde链接文件，\n且默认采用数据库链接\n1.ArcSDE connection file name sde文件名,\nsde后缀必须包含，如test.sde\n2.Instance为数据库实例名，如ip/orcl\n3.UserName和Password为地理数据库的凭证\n4.DataBase当数据库为Sqlserver的时候需要指定"
        w3=Label(group2,text=textdd).grid(row=0,column=0,rowspan=3,sticky="NW")
        tk.CallWrapper=Catcher

        try:
            Button(frm,text="ok",command=lambda:self.doCreateFile(cb)).grid(row=1,column=0,sticky="E")
            Button(frm,text="cancle",command=lambda:self.doCance(frm)).grid(row=1,column=1,sticky="W")
            cb.bind("<<ComboboxSelected>>",lambda x:self.selectValueChang(cb,en6))
        except ValueError,arg:
            print arg


if __name__ == "__main__":

    def show(root):
        app=cls_create_sde_file(root)


    root=Tk()
    Button(root,text="clickme",command=lambda:show(root)).grid(row=0,column=0)
    root.mainloop()



