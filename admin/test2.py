import sys

# print 'ddd'
# msg="'networkserver' license expired on 'Tue Jun 02 00:00:00 GMT+08:00 2015'. Please contact Esri Customer Support to obtain a new license.  To reauthorize your server, launch the Software Authorization tool and then restart ArcGIS Server."
# eee=['time="2015-07-11T19:25:05,476"', 'type="WARNING"', 'code="7269"', 'source="Admin"', 'process="72525"', 'thread="1"', 'methodName=""', 'machine="WEBSERVER.1.SITE"', 'user=""', 'elapsed=""']
# eee.append(msg)
# print eee

with open(r"C:\Users\jiangmb\Desktop\server\server-20150711.192504-72525-0.0.log") as file:

   allmsg= file.read()
   text0= allmsg.split('</')[0].split('>')
   #text0 format [<Msg time="" type="" code="" source="" process="" thread="" methodName="" machine="" user="" elapsed=""', "msg..."]
   text0[0].split(" ").append(text0[1]) #split text[0] by white space
   print text0[0].split(" ")
   for i in allmsg.split('</')[1:]:
        print i.split('>')[1:]