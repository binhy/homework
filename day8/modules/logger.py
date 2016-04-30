#!_*_coding:utf-8_*_


'''
handle all the logging works
'''
# import sys,os
# #print(sys.path)
# sys.path.append(os.path.dirname(os.path.dirname(__file__)))
# print(sys.path)


import os,logging
from conf import settings




def logger(log_type,file_name):

    #create logs
    logger = logging.getLogger(log_type)
    logger.setLevel(settings.LOG_LEVEL)


    # create console handler and set level to debug
    #ch = logging.StreamHandler()
    #ch.setLevel(settings.LOG_LEVEL)

    # create file handler and set level to warning
    #log_file = "%s/logs/%s" %(settings.BASE_DIR, settings.LOG_TYPES[log_type])
    log_file =os.path.join(settings.LOGS_PATH,file_name)
    fh = logging.FileHandler(log_file)
    fh.setLevel(settings.LOG_LEVEL)
    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch and fh
    #ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # add ch and fh to logs
    #logger.addHandler(ch)
    logger.addHandler(fh)

    return logger
    # 'application' code
    '''logs.debug('debug message')
    logs.info('info message')
    logs.warn('warn message')
    logs.error('error message')
    logs.critical('critical message')'''

# test=logger('access')
# test.error('hu eererror')