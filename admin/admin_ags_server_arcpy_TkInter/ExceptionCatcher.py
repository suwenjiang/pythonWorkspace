__author__ = 'suwen'
import Tkinter as tk
import traceback
from tkMessageBox import *
class Catcher:
    def __init__(self, func, subst, widget):
        self.func = func
        self.subst = subst
        self.widget = widget

    def __call__(self, *args):
        try:
            if self.subst:
                args = apply(self.subst, args)
            return apply(self.func, args)
        except SystemExit, msg:
            print msg
            raise SystemExit,msg
        except Exception,msg:
            print msg
            showerror('error',msg)
            #traceback.print_exc(file=open(r'c:\test.log', 'a'))



