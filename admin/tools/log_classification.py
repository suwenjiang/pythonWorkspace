#coding:gbk
__author__ = 'jiangmb'
import os
import re
import sqlite3

import argparse
import os
import sys


#check path
def getLogfile(log_path):

    try:
        fileslList=[]
        for root,dirname,files in os.walk(log_path):
            #print root,dir,files
            for file in files:
               # print file
                if os.path.splitext(file)[1]=='.log':
                    filePath=os.path.join(root,file)
                    if os.path.getsize(filePath)!=0:
                     fileslList.append(filePath )
        return fileslList
    except IOError,msg:
        print msg

def createDB(sqllite_file):

    conn=sqlite3.connect(sqllite_file)
    conn.execute('''CREATE TABLE LOG
       (id     INT  PRIMARY KEY     NOT NULL,
       msgtime    TEXT ,
       msg           TEXT ,
       msgtype        CHAR(50),
       code         CHAR(50),
       source       TEXT,
       process      CHAR(50),
       thread     CHAR(50),
       methodname  TEXT,
       machine   CHAR(50),
       fullmsg   TEXT,
       msguser    CHAR(100))
       ;''')
    conn.close()

def readAllMsg(sqllite_file,logFileList):
    try:
        conn=sqlite3.connect(sqllite_file)
        count=0
        for single in logFileList:
            file=open(single)
            #get all lines in file
            Lines=file.readlines()
            for i in Lines:
                time=re.findall(r'"([^"]*)"',re.findall('time="[^"]*"',i)[0])[0]
                type=re.findall(r'"([^"]*)"',re.findall('type="[^"]*"',i)[0])[0]
                code=re.findall(r'"([^"]*)"',re.findall('code="[^"]*"',i)[0])[0]
                process=re.findall(r'"([^"]*)"',re.findall('process="[^"]*"',i)[0])[0]
                thread=re.findall(r'"([^"]*)"',re.findall('thread="[^"]*"',i)[0])[0]
                methodName=re.findall(r'"([^"]*)"',re.findall('methodName="[^"]*"',i)[0])[0]
                source=re.findall(r'"([^"]*)"',re.findall('source="[^"]*"',i)[0])[0]
                machine=re.findall(r'"([^"]*)"',re.findall('machine="[^"]*"',i)[0])[0]
                user=re.findall(r'"([^"]*)"',re.findall('user="[^"]*"',i)[0])[0]
                msg1=re.findall('>[^/].*<',i)
                if len(msg1)!=0:
                    msg2=re.findall(r'>([^"]*)<',msg1[0])
                if len(msg2)!=0:
                    msg=msg2[0]
                else:
                    msg="get log message failed"
                #
                count=count+1
                #print time,type,code,source,process,thread,methodName,machine,user,msg
                conn.execute("insert into LOG values (?,?,?,?,?,?,?,?,?,?,?,?);", (count,time,msg.decode('utf-8'),type,code,source,process,thread,methodName,machine,i.decode("utf8"),user))

        conn.commit()
        conn.close()
     #

    except Exception,ex:
        print ex

def queryAndFilter(sqllite_file,whereClause,result_Path):
    conn=sqlite3.connect(sqllite_file)
    file=open(result_Path+"\\result.txt",'w')
    for row in conn.execute("select id,msgtime,msgtype,msg from log WHERE msgtype=? order by msgtime DESC;",(whereClause,)):
        file.write("Id="+str(row[0])+";time="+row[1]+";msgtype="+row[2]+";msg="+row[3])
        file.write("\n")
    file.close()






dbpath=''
whereclause=''
typeclause={'w':'WARNING','i':'INFO','f':'FINE','v':'VERBOSE','s':'SERVERE','d':'DEBUG'}
parser = argparse.ArgumentParser()
parser.add_argument("p",help="input directory or path of log file ",action="store")
parser.add_argument("-c",'--complete',metavar='',help="completely output format")

parser.add_argument("-l","--log",help="use msgType[warning,info,fine,verbose,severe,debug] to filter the log",\
                    choices=["w","i","f","v","s","d"],action="store")
parser.add_argument("-m","--machine",metavar='',help="machine name",action="store")
parser.add_argument("-t","--time",metavar='',help="time to filter log",action="store")
args=parser.parse_args()

files=[]
result_path=''
if  os.path.isfile(args.p):
    files.append(args.p)
    dbpath=os.path.split(args.p)[0]+"\\log.sqlite"
    result_path=os.path.split(args.p)[0]

elif os.path.isdir(args.p):
    files=getLogfile(args.p)
    if len(files)==0:
        print "The Current Dirtory don't container any log files"
        sys.exit()
    else:
        dbpath=args.p+"\\log.sqlite"
        result_path=args.p
else:
    print "please input a valid directory or .log file"
    sys.exit()

if args.log:
    if not args.log in ['w','i','f','v','s','d']:
        print "please choose a value from ['w','i','f','v','s','d']"
        sys .exit()
    else:
        whereclause=typeclause[args.log]
# if args.machine:
#     whereclause=args.log



# createDB
createDB(dbpath)
if len(files)!=0:
    readAllMsg(dbpath,files)
queryAndFilter(dbpath,whereclause,result_path)

#delteDB
os.remove(dbpath)

