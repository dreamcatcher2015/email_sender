'''
Created on Aug 20, 2015

@author: root
'''

import datetime

def getDate(dayto, days):    
    daycount = datetime.timedelta(days=days)
    dayfrom = dayto - daycount
    return dayfrom

def getDateBySeconds(dayto, seconds):    
    daycount = datetime.timedelta(seconds=seconds)
    dayfrom = dayto - daycount
    return dayfrom