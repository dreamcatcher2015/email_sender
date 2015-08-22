#coding=utf-8
'''
Created on Aug 21, 2015

@author: root
'''

import logging

def initlog():
    logger = logging.getLogger('')
    console = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s [%(levelname)-8s] [pid=%(process)d] %(message)s tid=%(thread)d %(pathname)s')
    console.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.setLevel(logging.WARNING)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(console)
    return logger

logger = initlog()
    
if __name__=="__main__":
    logger.info("info哈哈哈哈！")
    logger.warning("warning哈哈哈哈")
    logger.debug("debug哈哈哈哈！")
    pass