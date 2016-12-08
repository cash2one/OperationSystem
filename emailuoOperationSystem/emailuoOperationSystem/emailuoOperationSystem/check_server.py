#!/usr/bin/env python
#coding=gbk

from optparse import OptionParser
import socket
import time
import sys
import re
from StringIO import StringIO

class Check(object):
    """
    ��socket����һ�����ӣ�����http���󣬸��ݷ��ص�״̬�����жϷ���Ľ�׳��
    """
    def __init__(self,address,port,resource):
        self.address = address
        self.port = port
        self.resource = resource

    def check(self):
        #if not self.resource.startswitch('/'):
            #self.resource = '/' + self.resource

        request = 'GET %s HTTP/1.1\r\nHOST:%s\r\n\r\n' %(self.resource, self.address)

        s = socket.socket()

        s.settimeout(10)

        print("start to connect %s on the  %s port......." %(self.address,int(self.port)))

        try:
            s.connect((self.address,self.port))
            #print("cocnnect %s on port %s success!" %(self.address,self.port))
            s.send(request)
            response = s.recv(100)

        except socket.error,e:
            #print("connect host %s on port %s fail��reason is %s" %(self.address,self.port,e))
            return False

        finally:
            s.close()

        line = StringIO(response).readline()

        try:
            (http_version, status, messages) = re.split(r'\s+',line,2)

        except ValueError:
            #print("�ָ���Ӧ��ʧ��")
            return False
        #print ("return status Code is %s" %(status))

        if status in ['200', '301', '302']:
            print('server status is well')
        else:
            print('���������״̬')




parser = OptionParser()
parser.add_option('-a','--address',dest = "address", default = 'localhost',help='Ҫ����������ַ')
parser.add_option('-p','--port',dest = 'port',default = 80, help = "Ҫ���������˿�")
parser.add_option('-r','--resource',dest = 'resource', default = '/', help = 'Ҫ������Դ')
(options, args) = parser.parse_args()


checks = Check(options.address,options.port,options.resource)
while True:
    checks.check()
    print("=======================")
    time.sleep(10)

'''
���������У�ִ�нű� python check_server.py --address hostname --resource ·�� --port �˿�����
notice�� ·��Ҫ����'/ ' ǰ׺
example��python check_server.py  --address 121.199.62.174 --resource /js/tmpl/login.ejs?.. --port 15672
'''

