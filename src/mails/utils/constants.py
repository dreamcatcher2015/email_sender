#coding=utf-8

'''
Created on Aug 11, 2015

@author: root
'''

###########数据库相关配置##############
DATABASE_USER = "postgres"
DATABASE_PASS = ""
DATABASE_NAME = "mailsdb"
DATABASE_HOST = "mailsdb"

###########thrift相关配置#############
MAILS_SERVER_HOST = "mails_host"
MAILS_PORT        = "5051"

###########邮件服务器相关配置##########
MAIL_ATTACH_ROOT = '/home/mailfiles/'
mail_from        = '506767306@qq.com'
mail_password    = 'wfy311009060220'
mail_smtp        = 'smtp.qq.com'
mail_port        = 25

#####################################
SLEEP_CLIENT_MAILS_REACH  = 30 #数据表中没有待发送数据
SLEEP_TIME_NETWORK_EXCEPT = 100#网络异常
READ_CONUT                = 5 #主进程每次请求数据条数
SEND_RETRY_COUNT          = 3 #尝试次数
TIME_MAX_COUNT            = 10 #每天做多发送多少封邮件
TIME_LIMIT                = 1 #一天的时间
TIME_LIMIT_SECONDS        = 10#一次发送不对，10秒后才能再次发送
TIME_DELETE_PERIOD        = 10#每间隔10秒中删除一次数据库


############发送邮件相关配置###########
MAIL_INIT           = 0 #邮件为初始发送
MAIL_LOADED         = 1 #加载到队列
MAIL_ASSIGNED       = 2 #分配给一个进程
MAIL_SENDING        = 3 #正在发送
MAIL_RETRY          = 4 #发送失败，需要重新尝试
MAIL_SUCCESS        = 5 #发送成功
MAIL_NETWORK_EXCEPT = 0

MAIL_ATTACH_EXCEPT  = -1
MAIL_FAIL           = -2

############发送邮件时间相关配置###########
TIME_CREATE  = 'create_time'
TIME_LOADED  = 'loaded_time'
TIME_ASSIGN  = 'assigned_time'
TIME_SENDING = 'sending_time'
TIME_FINISH  = 'finish_time'
