#coding=utf-8
'''
Created on Aug 20, 2015

@author: root
'''
from mails.sendservice.SendMailsPool import SendMialsThread 
from mails.sendservice.DeleteMails import DeleteMials
from mails.thriftservice import server
from mails.utils import constants
import threading
from mails.utils.Logger import logger

if __name__ == "__main__":
    
    logger.info("启动删除邮件线程")
    deleteMails = DeleteMials(constants.TIME_DELETE_PERIOD)
    deleteMails.start()
    
    #控制接收到邮件将进程池的睡眠去掉
    global glocker
    glocker = threading.Event()
    
    logger.info("启动进程去创建进程池发送邮件")
    sendMialsThread = SendMialsThread(glocker)
    sendMialsThread.start()
    
    logger.info("启动thrift接收邮件")
    server.startService(glocker)
    
    
    