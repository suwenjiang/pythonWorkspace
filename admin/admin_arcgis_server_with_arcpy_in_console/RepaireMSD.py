__author__ = 'jiangmb'
import zipfile
from arcpy import mapping
import os
from xml.dom.minidom import parse

EXCLUDED_FILE_NAMES = ["DocumentInfo.xml", "layers/layers.xml","GISProject.xml"]
path=r"C:\arcgisserver\directories\arcgissystem\arcgisinput\test4\testCopy.MapServer\extracted\v101\testCopy.msd"

with zipfile.ZipFile(path,'r') as zzInput:
    for filename in (fileName for fileName in zzInput.namelist() if not fileName in EXCLUDED_FILE_NAMES):
        print filename
        dom=parse(zzInput.open(filename,'U'))

        pWorkspaceConnectionString=dom.getElementsByTagName('WorkspaceConnectionString')[0].childNodes[0].nodeValue
        print pWorkspaceConnectionString
        dom.getElementsByTagName('WorkspaceConnectionString')[0].childNodes[0].nodeValue='dd'
        zzInput.write(dom)



#         print dom
#     pWorkspaceConnectionString=dom.getElementsByTagName('WorkspaceConnectionString')[0].childNodes[0].nodeValue
#     # pWorkspaceFactory=dom.getElementsByTagName('WorkspaceFactory')[0].childNodes[0].nodeValue
#     # pDataset=dom.getElementsByTagName('Dataset')[0].childNodes[0].nodeValue
#     print pWorkspaceConnectionString
#
#     # modify the mxd
#     dom.getElementsByTagName('WorkspaceConnectionString')[0].childNodes[0].nodeValue=''
#
#
#
# else:


    # for fileName in (fileName for fileName in zz.namelist()):
    #     dom = parse(zz.open(fileName))




#
# def loadMsdLayerDom(dom):
#     """ Load dom created from xml file inside the msd. """
#
#     lyr =
#
#     # Layer name
#     lyr.name = dom.getElementsByTagName(self.LYR_NAME_NODE)[0].childNodes[0].nodeValue
#
#     # Symbology field name
#     symbologyElement = dom.getElementsByTagName(self.LYR_SYMBOL_NODE)[0]
#     lyr.symbologyFieldName = symbologyElement.getElementsByTagName(self.LYR_FIELD_NODE)[0].childNodes[0].nodeValue
#
#     return lyr.name, lyr

############
