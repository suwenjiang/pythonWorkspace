# -*-  coding:cp936 -*-
__author__ = 'jiangmb'
from arcpy import mapping
import os
import sys
class CreateContectionFile(object):
    def __init__(self):

        self.__filePath = None
        self.__loginDict = None

    def CreateContectionFile(self):
        """
        wrkspc: store the ags file
        loginDict: dictionary stored login information

        """
        # con = 'http://localhost:6080/arcgis/admin'
        try:
            server_url = "http://{}:6080/arcgis/admin".format(self.__loginDict['server'])
            connection_file_path = str(self.__filePath)            #
            use_arcgis_desktop_staging_folder = False
            if os.path.exists(connection_file_path):
                os.remove(connection_file_path)
            out_name = os.path.basename(connection_file_path)

            path = os.path.split(self.filePath)[0]

            result = mapping.CreateGISServerConnectionFile("ADMINISTER_GIS_SERVICES",
                                                           path,
                                                           out_name,
                                                           server_url,
                                                           "ARCGIS_SERVER",

                                                           use_arcgis_desktop_staging_folder,
                                                           path,
                                                           self.__loginDict['userName'],
                                                           self.__loginDict['passWord'],
                                                           "SAVE_USERNAME"
                                                           )

            print "++++++++INFO:链接文件创建成功++++++++"


            return connection_file_path

        except Exception, msg:
            print msg

    #
    @property
    def filePath(self):

        return self.__filePath

    @filePath.setter
    def filePath(self, value):
        self.__filePath = value

    @property
    def loginInfo(self):
        return self.__loginDict

    @loginInfo.setter
    def loginInfo(self, value):

        self.__loginDict = value


if __name__ == '__main__':
    logDict = {'server': '192.168.220.64',
               'userName': "arcgis",
               'passWord': "Super123"}
    dd = CreateContectionFile()
    dd.loginInfo = logDict
    path = os.path.split(sys.argv[0])[0] + "\\" + 'tt.ags'

    print path
    dd.filePath = path
    dd.CreateContectionFile()
