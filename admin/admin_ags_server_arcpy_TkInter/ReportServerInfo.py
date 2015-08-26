# -*-coding:utf-8 -*-

import Tkinter

from admin_ags_server_arcpy_TkInter import mapHelper


class reportServerInfo:

    def __init__(self,root):

        self.initialize(root)

    def initialize(self,root):
        w=root.winfo_screenwidth()/4
        h=root.winfo_screenheight()/4
        self.frm=Tkinter.Toplevel()
        self.frm.title("Report Server Info")
        self.frm.geometry('600x300+%d+%d'%(w,h))
        self.frm.grab_set()
        self.frm.transient(root)
        Tkinter.Grid.rowconfigure(self.frm,0,weight=1)
        Tkinter.Grid.columnconfigure(self.frm,0,weight=1)

        self.group = Tkinter.LabelFrame(self.frm, text="输入相关的参数")
        self.group.grid(row=0,column=0,sticky="NESW")

        self.Create_widget(self.group)


        self.group2 =Tkinter.LabelFrame(self.frm, text="工具使用说明")
        self.group2.grid(row=0,column=1,sticky="NSEW")

        Tkinter.Grid.rowconfigure(self.group2,0,weight=1)
        Tkinter.Grid.columnconfigure(self.group2,0,weight=1)

        w3=Tkinter.Label(self.group2,text="该工具用来获取和监控服务器的状态信息,包括：\n\n集群状态，集群中计算机状况，\n\n日志设置情况，许可情况等").grid(row=0,column=0,rowspan=3,sticky="NW")
        self.btn_excute=Tkinter.Button(self.frm,text="Excute",command=lambda:self.Excute())
        self.btn_excute.grid(row=1,column=0,sticky="NE")

        btn_cance=Tkinter.Button(self.frm,text="cancel")
        btn_cance.grid(row=1,column=1,sticky="wn")

    def Create_widget(self,group):

        Tkinter.Grid.rowconfigure(group,0,weight=1)
        Tkinter.Grid.columnconfigure(group,0,weight=1)



        self.text=Tkinter.Text(group)
        self.text.grid(row=0,column=0,rowspan=5,sticky="NSWE")


    def Excute(self):

       report= mapHelper.getServerInfo("localhost","6080","arcgis","Super123")

       newtxt=''



       self.text.insert("end",report.get("clusters"))
       self.text.insert("end",report.get("machineNames"))
       self.text.insert("end",report.get("Version"))
       self.text.insert("end",report.get("Log level"))
       self.text.insert("end",report.get("License"))
       self.text.insert("end",report.get("License expiration"))
       self.text.insert("end",report.get("extension"))


if __name__ == "__main__":

    def show(root):
        app=reportServerInfo(root)


    root=Tkinter.Tk()
    Tkinter.Button(root,text="clickme",command=lambda:show(root)).grid(row=0,column=0)
    root.mainloop()


