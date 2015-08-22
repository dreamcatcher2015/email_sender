# coding=utf-8
'''
Created on Aug 11, 2015

@author: root
'''
from mails.utils import constants
from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol
from mails.mailsvc import MailsService
from mails.mailsvc.ttypes import MailObject

def node_thrift_call(hostname, callback, *args):
    transport = None
    try:
        socket = TSocket.TSocket(hostname , constants.MAILS_PORT) 
        transport = TTransport.TBufferedTransport(socket)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)        
        client = MailsService.Client(protocol)        
        transport.open()            
        return callback(client, *args)    
    except Exception, e: 
        print e
        return None
    finally:
        if transport is not None:
            transport.close() 

def send_mails(mails):
    
    def qc(client, ): 
        return client.send_mails(mails)       

    return node_thrift_call(constants.MAILS_SERVER_HOST, qc)

def send_mails2(sendtos, subject="", content="", attach_files=[], priority=1):
    
    def qc(client, ): 
        return client.send_mails2(sendtos, subject, content, attach_files, priority)       

    return node_thrift_call(constants.MAILS_SERVER_HOST, qc)

def test_send_mails():
    sendto = '506767306@qq.com'
    subject = '我在测试，你好'
    content = '测试中文是否有乱码'
    attach_files = ['mails_attach/test.txt', 'attach_files/config.doc']
    
    mail1 = MailObject(sendto=sendto,
                             subject=subject,
                             content=content,
                             attach_files=attach_files) 
    
    sendto = 'wangfy2015@163.com'
    content = 'content 啦啦啦'
    subject = 'test, 你好'
    priority = 1
    mail2 = MailObject(sendto=sendto,
                             subject=subject,
                             content=content,
                             attach_files=attach_files,
                             priority=priority) 
      
    mails = []
    mails.append(mail1)
    mails.append(mail2)
    return send_mails(mails)
    

def test_send_mails2():
    sendtos = ['wfy@cnic.cn', 'wangfy2015@163.com']
    #subject = 'hello'
    #content = 'hello world'
    #attach_files = ['/home/mails_attach/test.txt', 'attach_files/config.doc']
    #priority = 3
    return send_mails2(sendtos)

#print test_send_mails()

# test_send_mails2()

# sendto = 'wfy@cnic.cn'
# subject = 'hello'
# content = 'hello world'
# attach_files = ['/home/mails_attach/test.txt', 'attach_files/config.doc']
#     
# mail = MailObject(sendto=sendto, subject=subject)
# 
# print mail.priority

if __name__ == "__main__":
    #print test_send_mails()
#     mail = MailObject()
#     print mail
    for i in xrange(2):
        test_send_mails()