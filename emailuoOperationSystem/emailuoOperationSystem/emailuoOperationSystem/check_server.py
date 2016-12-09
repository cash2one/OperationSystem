#!/usr/bin/env python
#coding= utf-8

#from optparse import OptionParser
import socket
import time
import sys
import re
from StringIO import StringIO
import pymongo
import database


class Check(object):
    """
    ��socket����һ�����ӣ�����http���󣬸��ݷ��ص�״̬�����жϷ���Ľ�׳��
    """
  
    def __call__(self,address, port):
        self.address = address
        self.port = port
        #self.resource = resource
        return Check

    def check(self,address,port):
        #if not self.resource.startswitch('/'):
            #self.resource = '/' + self.resource

        request = 'GET / HTTP/1.1\r\nHOST:%s\r\n\r\n' %( address)

        s = socket.socket()

        s.settimeout(10)

        #print("start to connect %s on the  %s port......." %(self.address,int(self.port)))

        try:
            s.connect((address,port))
            print("cocnnect %s on port %s success!" %(address,port))
            s.send(request)
            response = s.recv(100)

        except socket.error,e:
            #print("connect host %s on port %s fail��reason is %s" %(self.address,self.port,e))
            return 'error3'

        finally:
            s.close()

        line = StringIO(response).readline()

        try:
            (http_version, status, messages) = re.split(r'\s+',line,2)

        except ValueError:
            #print("�ָ���Ӧ��ʧ��")
            return 'error1'
        #print ("return status Code is %s" %(status))

        if status in ['200', '301', '302']:
            #print('server status is well')
            return status
        else:
            #print('���������״̬')
            return 'error2'

checks = Check()
data = database.Database()
server_data = data.get_host()

server_loop = []
for item in server_data:
        a = {
            'check_IP':item['IP_address'],
            'port':item['port']
            }
        server_loop.append(a)


def get_server_status():
    for item in server_loop:
        check_IP = item['check_IP']
        #print(check_IP)
        check_port = item['port']       
        check_result = checks.check(check_IP,check_port)
        return check_result
#time.sleep(5)
'''
#the function have loop-function
def check_server():
    while True:
        status = []
        try:
            for item in server_data:
                check_ip = item['IP_address']
                check_port = item['port']
                check_result = checks.check(check_ip,check_port)
                status.append({'server_name':check_result})
            return status
        except:
            return 'Noack'

def get_server_status():
'''
'''
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


���������У�ִ�нű� python check_server.py --address hostname --resource ·�� --port �˿�����
notice�� ·��Ҫ����'/ ' ǰ׺
example��python check_server.py  --address 121.199.62.174 --resource /js/tmpl/login.ejs?.. --port 15672

'''
