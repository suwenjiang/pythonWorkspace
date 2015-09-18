#-*-coding:cp936  -*-

__author__ = 'jiangmb'
import time


def GetMxFileList(filePath):
        #判断文件夹是否存在
    if not os.path.exists(filePath):
        print "++++++++ERROR:文件夹不存在+++++++"
        sys.exit(1)
    #获取文件夹中的所有mxd文件
    list=[]
    for root,dirname, files in os.walk(filePath):

             for file in files:

                if os.path.splitext(file)[1]=='.mxd':
                    mxdfile=os.path.join(root,file)

                    list.append(mxdfile)

    if list==[]:
      print "++++++++INFO:在当前目录下不存在有效的mxd文件++++++++"
      time.sleep(5)
      sys.exit(1)
    return list
def GetInfo():

    server = raw_input("请输入GIS Server IP:")
    userName=raw_input("请输入站点管理员用户名:")
    passWord=getpass.getpass("请输入站点管理员密码:")



    print "++++++++INFO:开始创建server的链接文件++++++++"
    """
    logDict={'server':'localhost',
        'userName':"arcgis",
             'passWord':"Super123"}
    dd=CreateContectionFile()
    dd.loginInfo=logDict
    dd.filePath="d:/dd.ags"
    dd.CreateContectionFile()
    """
    logDict={'server':server,
            'userName':userName,
                 'passWord':passWord}

    contionfile= os.path.split(sys.argv[0])[0]+'\\'+server+".ags"

    #调用创建链接文件的参数
    instace=CreateContectionFile()
    instace.filePath=contionfile
    instace.loginInfo=logDict
    instace.CreateContectionFile()

    if(os.path.isfile(contionfile)==False):
        print "++++++++ERROR:创建链接失败++++++++"
        time.sleep(5)
        sys.exit(1)

    #输入mxd文件的文件夹e
    mxdDir=raw_input('请输入mxd所在文件夹:')
    fileList=GetMxFileList(mxdDir)

    servic_dir=raw_input("请指定发布到服务器目录，默认为root。使用默认值直接回车:")
    if len(servic_dir)==0:
        servic_dir==None
    clusterName=raw_input("请指定发布到集群，默认为cluster。如没有集群环境，请直接回车:")
    if len(clusterName)==0:
        clusterName='default'
    clsPublishservice=publishServices()
    clsPublishservice.publishServices(fileList,contionfile,clusterName,copy_data_to_server=False,folder=servic_dir)
if __name__=='__main__':
    GetInfo()
    # clsPublishservice=publishServices()
    # fileList=['d:\\workspace\\testCopy.mxd', 'd:\\workspace\\test.mxd']
    # contionfile=r"d:\localhost.ags"
    # clusterName='default'
    # servic_dir='test3'