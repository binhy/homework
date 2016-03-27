#!_*_coding:utf-8_*_


'''
handle all the logging works
'''
# import sys,os
# #print(sys.path)
# sys.path.append(os.path.dirname(os.path.dirname(__file__)))
# print(sys.path)


import logging
from conf import settings




def logger(log_type):

    #create log
    logger = logging.getLogger(log_type)
    logger.setLevel(settings.LOG_LEVEL)


    # create console handler and set level to debug
    #ch = logging.StreamHandler()
    #ch.setLevel(settings.LOG_LEVEL)

    # create file handler and set level to warning
    #log_file = "%s/log/%s" %(settings.BASE_DIR, settings.LOG_TYPES[log_type])
    log_file =settings.LOGS_PATH
    fh = logging.FileHandler(log_file)
    fh.setLevel(settings.LOG_LEVEL)
    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch and fh
    #ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # add ch and fh to log
    #logger.addHandler(ch)
    logger.addHandler(fh)

    return logger
    # 'application' code
    '''log.debug('debug message')
    log.info('info message')
    log.warn('warn message')
    log.error('error message')
    log.critical('critical message')'''

# test=logger('access')
# test.error('hu eererror')