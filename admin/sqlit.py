#coding:gbk
__author__ = 'jiangmb'
import os
import re
import sqlite3

import argparse
import os
import sys




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
                splitCode(i)
        #         time=re.findall(r'"([^"]*)"',re.findall('time="[^"]*"',i)[0])[0]
        #         type=re.findall(r'"([^"]*)"',re.findall('type="[^"]*"',i)[0])[0]
        #         code=re.findall(r'"([^"]*)"',re.findall('code="[^"]*"',i)[0])[0]
        #         process=re.findall(r'"([^"]*)"',re.findall('process="[^"]*"',i)[0])[0]
        #         thread=re.findall(r'"([^"]*)"',re.findall('thread="[^"]*"',i)[0])[0]
        #         methodName=re.findall(r'"([^"]*)"',re.findall('methodName="[^"]*"',i)[0])[0]
        #         source=re.findall(r'"([^"]*)"',re.findall('source="[^"]*"',i)[0])[0]
        #         machine=re.findall(r'"([^"]*)"',re.findall('machine="[^"]*"',i)[0])[0]
        #         user=re.findall(r'"([^"]*)"',re.findall('user="[^"]*"',i)[0])[0]
        #         msg1=re.findall('>[^/].*<',i)
        #
        #         if len(msg1)!=0:
        #             msg2=re.findall(r'>([^"]*)<',msg1[0])
        #         if len(msg2)!=0:
        #             msg=msg2[0]
        #         else:
        #             msg="get log message failed"
        #         #
        #         count=count+1
        #         #print time,type,code,source,process,thread,methodName,machine,user,msg
        #         conn.execute("insert into LOG values (?,?,?,?,?,?,?,?,?,?,?,?);", (count,time,msg.decode('utf-8'),type,code,source,process,thread,methodName,machine,i.decode("utf8"),user))
        #
        # conn.commit()
        # conn.close()
     #

    except Exception,ex:
        print ex


def splitCode(line):

    if '>' in line:
        text=line.split('>')

        if '<' in text[1]:

            msg=text[1].split('<')[0]

        else:
            msg=text[1]
        listt=text[0].split(' ')[1:]

        print listt
        print listt.append('msg='+msg)

    else:
        print line

