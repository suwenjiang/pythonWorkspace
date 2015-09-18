# -*-coding:utf-8 -*-
__author__ = 'jmb'

from Tkinter import *
from tkMessageBox import *

# reload(sys)
# sys.setdefaultencoding('utf8')
class clsDoPublish:
    def __init__(self,root,dic_mxd_toPublish,conn):

        self.dic_mxd_toPublish=dic_mxd_toPublish
        self.conn=conn
        self.mutiMXDPublishUI(root)

    def mutiMXDPublishUI(self,root):
        w=root.winfo_screenwidth()/4
        h=root.winfo_screenheight()/4
        frm=Toplevel()
        frm.title('Batch Sevices Publish')
        frm.geometry('600x400+%d+%d'%(w,h))
        frm.grab_set()
        frm.transient(root)
        for x in (0,2):
            Grid.rowconfigure(frm,x,weight=1)
            Grid.columnconfigure(frm,x,weight=1)
        group = LabelFrame(frm, text="添加mxd文件夹")
        group.grid(row=0,column=0,sticky="NEW")
        group3=LabelFrame(frm,text="mxd need to be published")
        group3.grid(row=2,column=0,sticky="NEW")

        #grid 随着放大而放大
        Grid.rowconfigure(group,0,weight=1)
        Grid.columnconfigure(group,0,weight=1)
        Grid.rowconfigure(group3,0,weight=1)
        Grid.columnconfigure(group3,0,weight=1)

        w = Text(group)
        w.grid(row=0,column=0,sticky="NESW")
        #插入有效发布的数据
        for file in self.dic_mxd_toPublish:
            w.insert("end","\n"+self.dic_mxd_toPublish[file])
        w2=Text(group3)
        w2.grid(row=0,column=0,sticky="NEW")
        group2=LabelFrame(frm,text="STEP4:发布所有文档")
        group2.grid(row=0,column=1,rowspan=3,sticky="NESW")

        textdd="1.添加包含mxd文件的文件夹\n2检测mxd文档的有效性\n3. 发布成服务"
        w3=Label(group2,text=textdd).grid(row=0,column=0)
        Button(frm,text="PublishAll",command=lambda :self.publishAll(w2)).grid(row=1,column=0,sticky="NWE")
        Button(frm,text="closed",command=lambda:self.doCance(frm)).grid(row=3,column=1,sticky="NW")

    def doCance(self,frm):
        frm.destroy()

    def publishAll(self,testWidget):

        if self.dic_mxd_toPublish=={}:
            print "选择的文件夹中没有可以用发布服务的mxd文件"
        else:
            publishServices(self.dic_mxd_toPublish,self.conn)
            showinfo("success","所有服务发布成功！")


if __name__=='__main__':
    root=Tk("批量发布地图服务")
    dd= clsDoPublish(root,{})
    root.mainloop()













