#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (c) UbuntuChina, http://www.ubuntu.org.cn
# (c) free software, GPLv3
# Connect: oneleaf@gmail.com
import BaseHTTPServer,SocketServer, cgi
from os import curdir,sep, path
uploadhtml='''<html><body>
<p>批量文件上传</p>
<form enctype="multipart/form-data" action="/" method="post">
<p>File: <input type="file" name="file1"></p>
<p>File: <input type="file" name="file2"></p>
<p>File: <input type="file" name="file3"></p>
<p>File: <input type="file" name="file4"></p>
<p>File: <input type="file" name="file5"></p>
<p><input type="submit" value="上传"></p>
</form>
</body></html>'''
class WebHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path=='/':
           self.send_response(200)
           self.send_header('Content-Type','text/html; charset=utf-8')
           self.end_headers()
           self.wfile.write(uploadhtml)
           return
        try:
           f = open(curdir+sep+self.path)
           self.send_response(200)
           self.end_headers()
           self.wfile.write(f.read())
           f.close()
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)
    def do_POST(self):
        form = cgi.FieldStorage(fp=self.rfile,headers=self.headers,environ={'REQUEST_METHOD':'POST','CONTENT_TYPE':self.headers['Content-Type'],})
        self.send_response(200)
        self.send_header('Content-Type','text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write('<Html>上传完毕。<br/><br/>');
        self.wfile.write('客户端: %s<br/>' % str(self.client_address))
        for field in form.keys():
            field_item = form[field]
            if field_item.filename:
                fn=curdir+sep+field_item.filename
                if path.exists(fn):
                   self.wfile.write('文件 <a href="%s">%s</a> 已经存在，忽略上传。<br/>' % (field_item.filename,field_item.filename))
                else:
                   upfile=open(fn,'w')
                   file_data=field_item.file.read()
                   upfile.write(file_data);
                   upfile.close()
                   file_len = len(file_data)
                   del file_data
                   self.wfile.write('文件 <a href="%s">%s</a> 成功上传，尺寸为：%d bytes<br/>' % (field_item.filename,field_item.filename,file_len))
        self.wfile.write('</html>')
class ThreadingHTTPServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer): pass
if __name__ == '__main__':
    server_address = ('0.0.0.0', 8080)
    httpd = ThreadingHTTPServer(server_address, WebHandler)
    print "Web Server On %s:%d" % server_address
    httpd.serve_forever()