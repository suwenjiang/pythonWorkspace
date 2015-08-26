

__author__ = 'suwen'

import ArcPy_Project
import os

def CreateMXD(mxdPath):
    mxd = ArcPy_Project.mapping.MapDocument(mxdPath)
    msd = r"\\192.168.110.129\data\test2.mxd"
    df = ArcPy_Project.mapping.ListDataFrames(mxd, "Layers")[0]
    ArcPy_Project.mapping.ConvertToMSD(mxd, msd, df, "NORMAL", "NORMAL")
    print "create successful"


oldMxd=r"\\192.168.110.129\data\test2.mxd"
#check if it broken
mxd=ArcPy_Project.mapping.MapDocument(oldMxd)
#list the brklist
brknlist=ArcPy_Project.mapping.ListBrokenDataSources(mxd)
for brknitem in brknlist:
    print "\t"+brknitem.name
mxd.findAndReplaceWorkspacePaths(r"C:\Users\suwen\AppData\Roaming\ESRI\Desktop10.2\ArcCatalog\Connection to localhost.sde",r"C:\Users\suwen\AppData\Roaming\ESRI\Desktop10.2\ArcCatalog\Connection to localhost (2).sde",True)
mxd.save()
print "finished"

CreateMXD(oldMxd)