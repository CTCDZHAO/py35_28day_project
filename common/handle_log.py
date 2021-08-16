"""
为了避免程序中创建多个日志收集器而导致日志重复收集
那么我们可以只创建一个日志收集器，别的模块的使用时都导入这个日志收集器

"""
import configparser
import logging
from common.handle_conf import conf
from common.handle_path import LOG_DIR
import os
def create_log(name='mylog',level='DEBUG',filename='log.log',sh_level='DEBUG',fh_level='DEBUG'):
    # 第一步 创建日志收集器
    log=logging.getLogger(name)

    # 第二部 创建日志收集器日志的等级
    log.setLevel(level)
    # 第三步 设置输出日志渠道
    # 3.1 输出到文件
    fh = logging.FileHandler(filename, encoding='utf-8')
    fh.setLevel(fh_level)
    log.addHandler(fh)
    # 3。2输出到控制台
    sh = logging.StreamHandler()
    sh.setLevel(sh_level)
    log.addHandler(sh)
    # 第四部 设置日志输出的格式
    log_format = logging.Formatter('%(asctime)s --%(message)s--%(pathname)s--%(filename)s--%(levelname)s')
    # 创建格式对象
    sh.setFormatter(log_format)
    # 设置输出到文件的日志格式
    fh.setFormatter(log_format)
    # 返回一个日志收集器
    return log
'''
'''
my_log=create_log(
    name=conf.get('logging', 'name'),
    level = conf.get('logging','level'),
    filename = os.path.join(LOG_DIR,conf.get("logging","filename")),
    sh_level = conf.get('logging','sh_level'),
    fh_level = conf.get('logging','fh_level'),
)