#coding=utf-8
'''
Created on Aug 11, 2015

@author: root
'''

from mails.mailsvc import MailsService
from mails.utils import constants
from thrift.server import TServer
from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol
from mails.mailsvc.ttypes import MailObject
from datetime import datetime
from mails.utils.Conn import dbconn
import json
from mails.utils.Logger import logger

'''
获取email的服务
xxxxxxxxxx@qq.com,会获取qq.com
'''
def getSmtpHost(email):
    start = email.index('@')
    #end = email.index('.', start)
    return email[start+1:]

class MailsHandler(MailsService.Iface):
    
    def __init__(self, glocker):
        self.glocker = glocker
    
    def send_mails(self, mails):
        """
        Parameters:
         - mails
        """
        try:
            for mailObject in mails:
                if not mailObject.sendto:
                    logger.info("mailObject.sendto is empty!")
                    continue
                smtp_host = getSmtpHost(mailObject.sendto)
                create_time = datetime.now() 
                attach_files = json.dumps(mailObject.attach_files)
                
                dbconn().insertOne("insert into mails (sendto, smtp_host, subject, content, attach_files, priority, create_time, send_count, state) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)" ,
                [mailObject.sendto, smtp_host, mailObject.subject, mailObject.content, attach_files, mailObject.priority, create_time, 0, constants.MAIL_INIT]) 
    
            #设置事件
            self.glocker.set()
            return True
        except Exception as e:
            print e
            return False 
        
    def send_mails2(self, sendtos, subject, content, attach_files, priority):
        """
        Parameters:
         - sendtos
         - subject
         - content
         - attach_files
         - priority
        """
        try:
            mails = []
            for sendto in sendtos:
                mailobject = MailObject(sendto=sendto,
                                        subject=subject,
                                        content=content,
                                        attach_files=attach_files,
                                        priority=priority)
                mails.append(mailobject)
            return self.send_mails(mails)
        except Exception as e:
            print e
            return False  

def startService(glocker): 
    mailsHandler = MailsHandler(glocker)
    
    processor = MailsService.Processor(mailsHandler)
    transport = TSocket.TServerSocket(host=constants.MAILS_SERVER_HOST,
                                      port=constants.MAILS_PORT)
    
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()
    
    server = TServer.TThreadedServer(processor, transport, tfactory, pfactory, daemon=True)
    
    logger.info("mails server start") 
    server.serve()
    
########启动thrift服务######### 
if __name__=="__main__":    
    startService()