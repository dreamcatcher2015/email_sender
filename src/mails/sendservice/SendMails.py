#coding=utf-8
'''
Created on Aug 12, 2015

@author: root
'''

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from mails.utils import FileUtils
from mails.utils import constants
import json
from mails.utils.Logger import logger

class SendMails():
    def __init__(self, mail):
        self.mail = mail
    
    '''
    根据文件名称构造附件
    '''   
    def getAttachs(self, filename):
        filepath = constants.MAIL_ATTACH_ROOT+filename
        if FileUtils.isExists(filepath):
            attach = MIMEText(open(filepath, 'rb').read(), 'base64', 'utf-8')
            attach["Content-Type"] = 'application/octet-stream'
            attach["Content-Disposition"] = 'attachment; filename="%s"' % filename#邮件中显示的名字
            return attach
        return None
    
    '''
    发送邮件
    1：发送成功
    -1：网络错误
    0：邮件错误
    -2：位置错误
    '''        
    def sendMail(self):
        try:
            #创建与邮件服务器链接
            server = smtplib.SMTP()
            try:
                server.connect(constants.mail_smtp, constants.mail_port)#smtp服务器主机名，端口（默认25）
            except Exception, e:
                print e
                #logger.debug("发送邮件失败(网络错误)")
                return constants.MAIL_NETWORK_EXCEPT
            
            #设置邮件基础信息
            msg = MIMEMultipart()#创建一个带附件的实例
            msg['from'] = constants.mail_from
            msg['pwd'] = constants.mail_password
            msg['to'] = self.mail['sendto']
            msg['subject'] = self.mail['subject']
            #msg['date'] = datetime.datetime()
            
            #设置邮件内容
            body = MIMEText(self.mail['content'])
            msg.attach(body)
            
            #构造附件
            if self.mail['attach_files']:#存在附件
                attach_files = json.loads(self.mail['attach_files'])
                for filename in attach_files:
                    #print constants.MAIL_ATTACH_ROOT+filename
                    attach = self.getAttachs(filename)
                    if attach is not None:
                        msg.attach(attach)
                    else:
                        #logger.debug("构造附件失败(附件路径不存在) id=%s" % self.mail['id'])
                        return constants.MAIL_ATTACH_EXCEPT
            #发送邮件 
            server.login(msg['from'], msg['pwd'])#from_address, password
            server.sendmail(msg['from'], msg['to'], msg.as_string())
           
            #logger.info('发送邮件成功: %s' % (msg['to']))
            
            return constants.MAIL_SUCCESS
        except Exception, e:  
            logger.debug("e=%s" % e)
            #logger.debug("发送邮件失败(未知错误--重新发送)id=%s" % self.mail['id'])
            return constants.MAIL_RETRY
        
        finally:
            if server is not None:
                server.quit()     
            