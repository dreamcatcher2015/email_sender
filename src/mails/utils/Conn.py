'''
Created on Aug 17, 2015

@author: root
'''

from mails.utils import constants
from dbs.pgsql import Pgsql
from numpy.ma.core import ids
import types
from datetime import datetime

def dbconn():
    return Pgsql(constants.DATABASE_HOST, 
             constants.DATABASE_USER, 
             constants.DATABASE_PASS, 
             constants.DATABASE_NAME)
    
def updateStateByIds(state=0, ids=None, time=constants.TIME_FINISH):
    if type(ids) is types.IntType:
        sql = "update mails set state=%s, " + time + "=%s where id = %s"
        params = [state, datetime.now(), ids]   
    else:
        idstr = ",".join(ids)
        #print idstr
        sql = "update mails set state=%s, "  + time +  "=%s where id in ( " + idstr + ") "
        params = [state, datetime.now()]     
    return dbconn().update(sql=sql, param=params)

def updateStateAll(state=0):
    sql = "update mails set state=%s where state<=4 and state>0" % state
    return dbconn().update(sql=sql)

def updatePriority(mail=None, state=0, priority=0):
    sql = "update mails set priority=%s, state=%s where id = %s" % (priority, constants.MAIL_INIT, mail['id']) 
    return dbconn().update(sql)

if __name__ == "__main__":
    ids = [310, 100]
    updateStateByIds(constants.MAIL_INIT)