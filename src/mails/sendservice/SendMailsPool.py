#coding=utf-8
'''
Created on Aug 12, 2015
@author: root
'''

import multiprocessing as mul
from mails.sendservice.SendMailsManager import SendMailsManager
from mails.utils.Conn import dbconn, updateStateByIds, updateStateAll, updatePriority
from mails.utils import constants, DateUtils
import time
import datetime
from threading import Thread
from mails.utils.Logger import logger

global processCount    
processCount = 3 

global event_network_except
event_network_except = mul.Event()

def sendMails(mail):
    sendMailsManager = SendMailsManager(mail=mail, event=event_network_except)
    sendMailsManager.sendMails()

class SendMialsThread(Thread):
    
    def __init__(self, glocker):
        Thread.__init__(self)
        self.setDaemon(True)
        self.glocker = glocker
        
    def getMails(self):
        sql = "select id, sendto, smtp_host, subject, content, attach_files, send_count, priority, create_time, send_count, state, finish_time from mails where state=%s and send_count<%s order by priority desc, send_count asc, create_time asc, id asc limit %s" % (constants.MAIL_INIT, constants.SEND_RETRY_COUNT, constants.READ_CONUT)
        #print sql
        mails = dbconn().getAll(sql)
        if len(mails) != 0:#将读取到的邮件状态修改为加载完成状态(2)
            ids = map( lambda a: str(a["id"]), mails)
            updateStateByIds(state=constants.MAIL_LOADED, ids=ids, time='loaded_time')
        return mails
  
    def run(self):
        #启动服务器之前，先把邮件表的状态全部修改为初始状态
        updateStateAll(constants.MAIL_INIT)
        logger.info("服务器启动修改所有待发送邮件为初始状态")
        #time.sleep(1000)
        
        #创建进程池(大小为10)
        pool = mul.Pool(processes=3)
        global processCount
        processCount = 3 
        
        #i = 0
        unvalid_mial = False
        while True:
            #发邮件当网络堵塞，event_network_except会设置成true
            if event_network_except.is_set():
                event_network_except.wait(constants.SLEEP_TIME_NETWORK_EXCEPT)#等待
                event_network_except.clear()#清楚set
            
            #print "开始获取邮件"
            mails = []
            if unvalid_mial==False:
                mails = self.getMails()
                
            if len(mails) == 0:
                #print "获取邮件成功 count： %s" % len(mails)
                logger.info("主进程等待时间：%s" % constants.SLEEP_CLIENT_MAILS_REACH)
                self.glocker.wait(constants.SLEEP_CLIENT_MAILS_REACH)
                self.glocker.clear()
                unvalid_mial = False
            else:
                unvalid_mial = True
                logger.info("获取邮件成功 count： %s" % len(mails))
                for mail in mails:
                    while processCount <= 0:
                        time.sleep(1)
                    
                    if self.isContinue(mail):
                        #修改为初始状态，优先级降级
                        updatePriority(mail=mail, state=constants.MAIL_INIT, priority=mail['priority']-1)
                        continue
                    
                    unvalid_mial = False
                    
                    #判断邮件上次发送时间，如果再10内不需要发送
                    dayto = datetime.datetime.now()
                    datefrom = DateUtils.getDateBySeconds(dayto, constants.TIME_LIMIT_SECONDS)    
                    if mail['finish_time']!=None and mail['finish_time'] > datefrom:
                        logger.info("同一封邮件再10内被读取两次，修改邮件为初始状态，跳过该邮件id=%s" % mail['id'])
                        updateStateByIds(state = constants.MAIL_INIT, ids=mail['id'])
                        continue
                    
                    #i = i + 1
                    #print "i=%s" % i
                    #修改邮件为已分配状态，并将邮件分配给一个单独进程
                    processCount = processCount - 1
                    updateStateByIds(state=constants.MAIL_ASSIGNED, ids=mail['id'], time=constants.TIME_ASSIGN)
                    pool.apply_async(func=sendMails, args=(mail,), callback=self.increaseProcessCount)
                    #time.sleep(10000000)
                    
        pool.close()#关闭进程池，不再创建新的进程
        pool.join()#等带进程池中的所有进程结束
 
    def increaseProcessCount(self, result):
        global processCount  
        processCount = processCount + 1
        logger.info("increaseProcessCount-processCount: %s" % processCount)
    
    
    def isContinue(self, mail):
        dayto = datetime.datetime.now()
        datefrom = DateUtils.getDate(dayto, constants.TIME_LIMIT)
        
        sql = "select count(*) as count from mails where smtp_host='%s' and state=5 and finish_time between '%s'::timestamp and '%s'::timestamp" % (mail['smtp_host'], datefrom, dayto)
        result = dbconn().getOne(sql)
        if result['count'] >= constants.TIME_MAX_COUNT:
            return True
        else:
            return False    
    
def serviceLoop():
    sendMialsThread = SendMialsThread()
    sendMialsThread.start()
    sendMialsThread.join()
        
if __name__ == "__main__":
    #启动远程调用，接收邮件
    serviceLoop()
    
