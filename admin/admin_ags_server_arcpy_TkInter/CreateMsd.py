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

class Create_msd_file:
    def __init__(self,root):
        self.mxdPath=StringVar()
        self.msdPath=StringVar()
        self.Create_msd_file(root)

    def openMxdFile(self):
        filePath=askopenfilename()
        if filePath:
            self.mxdPath.set(filePath)

    def SaveMsdFile(self):
        savefilePath=askdirectory()
        if savefilePath:
            self.msdPath.set(savefilePath)
    def DoCreate(self):
        mxd = arcpy.mapping.MapDocument(self.mxdPath.get())
        #get the filename of the mxd

        #df = arcpy.mapping.ListDataFrames(mxd, "County Maps")[0]
        arcpy.mapping.ConvertToMSD(mxd, self.msdPath.get(), "", "NORMAL", "NORMAL")

        showinfo("message","create successfully!")

    def Create_msd_file(self,root):
        ''''发布单独的mxd文件 '''
        w=root.winfo_screenwidth()/4
        h=root.winfo_screenheight()/4
        frm=Toplevel()
        frm.title('Create msd file')
        frm.geometry('600x300+%d+%d'%(w,h))
        frm.grab_set()
        frm.transient(root)

        Grid.rowconfigure(frm,0,weight=1)
        Grid.columnconfigure(frm,0,weight=1)


        labelFrame=LabelFrame(frm,text="输入参数")
        labelFrame.grid(row=0,column=0,sticky="NESW")


        for x in range(0,10):
            Grid.rowconfigure(labelFrame,x,weight=1)
        Grid.columnconfigure(labelFrame,0,weight=1)
        Grid.columnconfigure(labelFrame,1,weight=1)

        label_agsFile=Label(labelFrame,text="mxd Path")
        label_agsFile.grid(row=0,column=0,sticky="W")
        txt_ags=Entry(labelFrame,textvariable=self.mxdPath)
        txt_ags.grid(row=1,column=0,columnspan=2,sticky="WNE")

        btnBroswer1=Button(labelFrame,text="Broswer",command=self.openMxdFile)
        btnBroswer1.grid(row=1,column=1,sticky="EN")

        labelurl= Label(labelFrame,text='msd save Path:')
        labelurl.grid(row=2,column=0,sticky="WN")
        txturl=Entry(labelFrame,textvariable= self.msdPath)
        txturl.grid(row=3,column=0,columnspan=2,sticky="WNE")

        btnBroswer2=Button(labelFrame,text="Broswer",command=self.SaveMsdFile)
        btnBroswer2.grid(row=3,column=1,sticky="EN")



        group2 = LabelFrame(frm, text="工具使用说明",width=200)
        group2.grid(row=0,column=1,sticky="NSEW")

        Grid.rowconfigure(group2,0,weight=1)
        Grid.columnconfigure(group2,0,weight=1)
        textdd="该工具用来将mxd文档转换为msd文件\n\n1.参数1为需要转换的mxd文件，使用完整的路径\n\n2.参数2为需要保存的msd文件路径"
        w3=Label(group2,text=textdd).grid(row=0,column=0,sticky="NW")

        btnOk=Button(frm,text='Create', command=self.DoCreate).grid(row=1,column=0,sticky="NE")
        btnCancle=Button(frm,text='Cancle',command=lambda: self.doCance(frm)).grid(row=1,column=1,sticky="WN")
        tk.CallWrapper=Catcher
if __name__ == "__main__":

    def show(root):
        app=Create_msd_file(root)


    root=Tk()
    Button(root,text="clickme",command=lambda:show(root)).grid(row=0,column=0)
    root.mainloop()
