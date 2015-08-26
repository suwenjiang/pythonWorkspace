__author__ = 'jmb'
from Tkinter import *

from admin_ags_server_arcpy_TkInter.ExceptionCatcher import *


class CommonUI:

    def __init__(self):
        pass

    def CreateUITemplate(self):
        w=self.root.winfo_screenwidth()/4
        h=self.root.winfo_screenheight()/4
        frm=Toplevel()
        frm.title('Replace sde connection file')
        frm.geometry('600x300+%d+%d'%(w,h))
        frm.grab_set()
        frm.transient(self.root)
        Grid.rowconfigure(frm,0,weight=1)
        Grid.columnconfigure(frm,0,weight=1)


        group = LabelFrame(frm, text="输入相关的参数")
        group.grid(row=0,column=0,sticky="NESW")

        for x in range(10):
            Grid.rowconfigure(group,x,weight=1)

        Grid.columnconfigure(group,0,weight=1)
        Grid.columnconfigure(group,1,weight=1)

        label1=Label(group,text="directories Path")
        label1.grid(row=0,column=0,sticky="W")
        en1=Entry(group,textvariable=self.diretories_path)
        en1.grid(row=1,column=0,columnspan=2,sticky="WEN")
        btn1=Button(group,text="browser",command=lambda:self.Select_dirctior(txt))
        btn1.grid(row=1,column=1,sticky="EN")


        label2=Label(group,text="Old sde connection file")
        label2.grid(row=2,column=0,sticky="WN")
        en2=Entry(group,textvariable=self.strOldSde)
        en2.grid(row=3,column=0,columnspan=2,sticky="WEN")
        btn2=Button(group,text="browser",command=lambda:self.select_sde_file("Old"))
        btn2.grid(row=3,column=1,sticky="EN")



        label3= Label(group,text="New sde connection file")
        label3.grid(row=4,column=0,sticky="WN")
        en3= Entry(group,textvariable=self.strNewSde)
        en3.grid(row=5,column=0,columnspan=2,sticky="WEN")
        btn3=Button(group,text="browser",command=lambda:self.select_sde_file("NEW"))
        btn3.grid(row=5,column=1,sticky="EN")


        Grid.rowconfigure(group,6,weight=1)
        Grid.rowconfigure(group,0,weight=1)

        group3= LabelFrame(group,text="To be repaired map services")
        group3.grid(row=6,column=0,columnspan=2,sticky="WNE")
        Grid.rowconfigure(group3,0,weight=1)
        # Grid.columnconfigure(group3,0,weight=1)
        # Grid.columnconfigure(group3,1,weight=1)
        txt=Text(group3,height=6)
        txt.grid(row=0,column=0,columnspan=2,sticky="WES")



        Grid.columnconfigure(frm,2,weight=1)
        group2 = LabelFrame(frm, text="工具使用说明",width=200)
        group2.grid(row=0,column=1,rowspan=6,columnspan=1,sticky="NSEW")

        Grid.rowconfigure(group2,0,weight=1)
        Grid.columnconfigure(group2,0,weight=1)
        textdd="改工具用来创建sde链接文件，\n且默认采用数据库链接\n1.ArcSDE connection file name sde文件名,\nsde后缀必须包含，如test.sde\n2.Instance为数据库实例名，如ip/orcl\n3.UserName和Password为地理数据库的凭证\n4.DataBase当数据库为Sqlserver的时候需要制定"
        w3=Label(group2,text=textdd).grid(row=0,column=0,rowspan=3,sticky="NW")
        tk.CallWrapper=Catcher


        Button(frm,text="ok",command=lambda:self.doCreateFile(txt)).grid(row=1,column=0,sticky="E")
        Button(frm,text="cancle",command=lambda:self.doCance(frm)).grid(row=1,column=1,sticky="E")
