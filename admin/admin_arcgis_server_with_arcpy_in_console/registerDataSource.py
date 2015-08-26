__author__ = 'jiangmb'

from arcpy import ListDataStoreItems,ValidateDataStoreItem,AddDataStoreItem
def RegisterDataStoreItem(conn,server_path,client_path,storetype="FOLDER",name="My local data folder"):
   try:
        result= AddDataStoreItem(conn,storetype,name,server_path,client_path,)
        if result=="Success":
            print "register successfully"
        else:
            print result
   except Exception,msg:
       print msg

if __name__=='__main__':
    RegisterDataStoreItem\
        (r'C:\Users\jiangmb\AppData\Roaming\ESRI\Desktop10.3\ArcCatalog\arcgis on localhost_6080 (admin).ags','d:/Auser','d:/Auser')