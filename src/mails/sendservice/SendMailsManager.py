#coding=utf-8
'''
Created on Aug 17, 2015

@author: root
'''

from mails.utils import constants
from mails.sendservice.SendMails import SendMails
from mails.utils.Conn import dbconn, updateStateByIds
from mails.utils.Logger import logger
import datetime

class SendMailsManager():
    
    def __init__(self, mail=None, event=None):
        self.mail = mail
        self.e = event
        pass
    
    def sendMails(self):
        #发送邮件
        logger.info("开始发送邮件：id=%s" % self.mail['id'])
        #time.sleep(1)
        #修改为正在发送状态
        updateStateByIds(constants.MAIL_SENDING, ids=self.mail['id'], time=constants.TIME_SENDING)
        sm = SendMails(self.mail)
        result = sm.sendMail()
        
        if result == constants.MAIL_SUCCESS:
            #发送邮件成功，将本邮件发到成功表
            updateStateByIds(state = constants.MAIL_SUCCESS, ids=self.mail['id'], time=constants.TIME_FINISH)
            logger.info("发送邮件成功，将本邮件发到成功表id=%s" % self.mail['id'])
        elif result == constants.MAIL_RETRY:
            #发送邮件失败，修改状态改为初始状态，发送次数count+1
            logger.debug("发送邮件失败，修改发送次数count+1 id=%s" % self.mail['id'])
            self.sendRetry(self.mail)
        elif result == constants.MAIL_NETWORK_EXCEPT:
            #修改邮件为初始状态
            updateStateByIds(state = constants.MAIL_INIT, ids=self.mail['id'])
            #将主进程睡眠
            global event_network_except
            event_network_except.set()
            logger.debug("发送邮件失败，网络错误，睡眠 id=%s" % self.mail['id'])
        elif result == constants.MAIL_ATTACH_EXCEPT:
            #发送邮件失败，附件错误
            updateStateByIds(state = constants.MAIL_ATTACH_EXCEPT, ids=self.mail['id'], time=constants.TIME_FINISH)
            logger.debug("发送邮件失败，附件路径错误,  id=%s" % self.mail['id'])
        return result
    
    def sendRetry(self, mail):
        sql = "update mails set send_count=%s, state=%s, finish_time=%s where id = %s"
        if mail['send_count'] < constants.SEND_RETRY_COUNT:
            param = [mail['send_count']+1, constants.MAIL_INIT, datetime.datetime.now(), mail['id']];
        else:
            param = [mail['send_count']+1, constants.MAIL_FAIL, datetime.datetime.now(), mail['id']];
        dbconn().update(sql, param=param)
