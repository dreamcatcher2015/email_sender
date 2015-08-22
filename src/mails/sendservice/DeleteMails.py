#coding=utf-8
'''
Created on Aug 20, 2015

@author: root
'''
from threading import Thread
from mails.utils.Conn import dbconn
from mails.utils import constants, DateUtils
import time
import datetime
from mails.utils.Logger import logger

class DeleteMials(Thread):
    
    def __init__(self, interval):
        Thread.__init__(self)
        self.interval = interval
        self.setDaemon(True)
    
    def run(self):
        while True:
            self.delete()
            logger.info("定时删除邮件线程")
            time.sleep(self.interval)
    
    def delete(self):
        dayto = datetime.datetime.now()
        datefrom = DateUtils.getDate(dayto, constants.TIME_LIMIT)
        sql = "delete from mails where (state=%s or state<0) and finish_time < '%s'::timestamp"% (constants.MAIL_SUCCESS, datefrom)
        #print sql
        return dbconn().delete(sql)

def serviceLoop():
    deleteMails = DeleteMials(constants.TIME_DELETE_PERIOD)
    deleteMails.start()
    deleteMails.join()
        
if __name__ == "__main__":
    serviceLoop()