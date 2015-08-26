# -*-coding:utf-8 -*-
__author__ = 'jmb'

from admin_ags_server_arcpy_TkInter.s4_do_publish import *

reload(sys)
sys.setdefaultencoding('utf8')


class checkfilevalidation:
    def __init__(self,root,dic_mxd_files,dic_mxd_toPublish,conn):
        self.dic_mxd_toPublish={}
        self.dic_mxd_files=dic_mxd_files
        self.conn=conn
        self.check_file_validationUI(root)
    def check_file_validationUI(self,root):

        w=root.winfo_screenwidth()/4
        h=root.winfo_screenheight()/4
        frm=Toplevel()
        frm.title(' Batch Sevices Publish')
        frm.geometry('600x400+%d+%d'%(w,h))
        #frm.grab_set()
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
        #插入数据
        for file in self.dic_mxd_files:
            w.insert("end","\n"+self.dic_mxd_files[file])
        w2=Text(group3)
        w2.grid(row=2,column=0,sticky="NEW")
        group2=LabelFrame(frm,text="STEP3:检查mxd的有效性")
        group2.grid(row=0,column=1,rowspan=3,sticky="NESW")

        textdd="1.添加包含mxd文件的文件夹\n2检测mxd文档的有效性\n3. 发布成服务"
        w3=Label(group2,text=textdd).grid(row=0,column=1,sticky="NSEW")
        Button(frm,text="checkValid",command=lambda :self.checkfile(w2)).grid(row=1,column=0,sticky="NSEW")
        Button(frm,text="Next",command=lambda :self.mutiMXDPublishUI(root,frm)).grid(row=3,column=0,sticky="NE")
        Button(frm,text="Cancel",command=lambda:self.doCance(frm)).grid(row=3,column=1,sticky="NW")

    def doCance(self,frm):
        frm.destroy()

    def mutiMXDPublishUI(self,root,frm):
        publishsevice=clsDoPublish(root,self.dic_mxd_toPublish,self.conn)
        self.doCance(frm)


    def checkfile(self,text):

        # 将验证不通过的设置为红色
        text.tag_config("error",foreground="red")
        #获取当前程序路径，将检测报告放置该目录
        current_path=os.getcwd()
        check_report=os.path.join(current_path,"check.txt")

        for file in self.dic_mxd_files:
            mxd=arcpy.mapping.MapDocument(self.dic_mxd_files[file])
            brkList=arcpy.mapping.ListBrokenDataSources(mxd)
            if  brkList:
                text.insert("end","文档 %s 损坏:\n"%str(file))

                for brkItem in brkList:
                    text.insert("end","\t"+"损毁图层为有:%s\n"% str(brkItem.dataSource))
            else:
                text.insert("end","文档%s正常\n"%unicode(file))
                self.dic_mxd_toPublish[file]=self.dic_mxd_files[file]