__author__ = 'jiangmb'

from arcpy import mapping
import xml.dom.minidom as DOM
import os
class CreateSddraft:
    def CreateSddraft(self,mapDocPath,con,serviceName,copy_data_to_server=True,folder=None):

        """
        :param mapDocPath: mxd path
        :param con: arcgis server connection file
        :param serviceName: service name
        :param clusterName: cluster name
        :param folder: folder to contain the publishing service
        :return: the file path of the sddraft
        """

        mapDoc=mapping.MapDocument(mapDocPath)

        sddraft=mapDocPath.replace(".mxd",".sddraft")

        result= mapping.CreateMapSDDraft(mapDoc, sddraft, serviceName, 'ARCGIS_SERVER', con, copy_data_to_server, folder)


        return sddraft



    def setTheClusterName(self,xml,clusterName):# the new description

        doc = DOM.parse(xml)
        # find the Item Information Description element
        doc.getElementsByTagName('Cluster')[0].childNodes[0].nodeValue=clusterName
        # output to a new sddraft
        outXml =xml
        f = open(outXml, 'w')
        doc.writexml( f )
        f.close()
        return  outXml

if __name__=='__main__':
    print('dd')

    CreateSddraft(r"d:\workspace\test.mxd",r'C:\Users\jiangmb\AppData\Roaming\ESRI\Desktop10.3\ArcCatalog\arcgis on localhost_6080 (admin).ags','testttt','default')