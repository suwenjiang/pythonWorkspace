#-*-encoding:utf-8 -*-
__author__ = 'jmb'
import ArcPy_Project
from ArcPy_Project import env

env.workspace="E:\\data"
fc="Join_Output.shp"
 #新建一个txt，将该文件输出到txt中
file=open("d:\json.txt",'w')

#通过令牌的形式将shape字段转换成json
for row in ArcPy_Project.da.SearchCursor(fc,["SHAPE@JSON"]):
    file.write(str(row))
file.close()