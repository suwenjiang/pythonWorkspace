__author__ = 'jiangmb'
import zipfile
from arcpy import mapping
import os
from xml.dom.minidom import parse

EXCLUDED_FILE_NAMES = ["DocumentInfo.xml", "layers/layers.xml","GISProject.xml"]

if(zipfile.is_zipfile(r"d:\msdDataSource.msd")):

    zz = zipfile.ZipFile(r"d:\msdDataSource.msd")
    for fileName in (fileName for fileName in zz.namelist() if not fileName in EXCLUDED_FILE_NAMES):
        print fileName

    if os.path.splitext(fileName)[1]==".xml":
        dom=parse(zz.open(fileName))
        print dom
    pWorkspaceConnectionString=dom.getElementsByTagName('WorkspaceConnectionString')[0].childNodes[0].nodeValue
    pWorkspaceFactory=dom.getElementsByTagName('WorkspaceFactory')[0].childNodes[0].nodeValue
    pDataset=dom.getElementsByTagName('Dataset')[0].childNodes[0].nodeValue
    print pWorkspaceConnectionString,pWorkspaceFactory,pDataset


else:


    # for fileName in (fileName for fileName in zz.namelist()):
    #     dom = parse(zz.open(fileName))
       print "dom"



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
