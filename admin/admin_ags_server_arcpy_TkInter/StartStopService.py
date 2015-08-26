# -*-coding:utf-8 -*-



import Tkinter
import baseWiget

class startStopService:

    def __init__(self,root):
        self.root=root
        self.create_wiget()

    def create_wiget(self):

        frm=baseWiget(self.root)

        group=frm.group

        btn=Tkinter.Button(group,text='click me')
        btn.grid(row=0,column=0,stikcy="W")



if "__name__"=="__main__":

    root=Tkinter.Tk()
    app=startStopService(root)

    root.mainloop()

