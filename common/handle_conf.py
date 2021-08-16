from configparser import ConfigParser
from common.handle_path import CONF_DIR
import os
class Config(ConfigParser):
    def __init__(self,conf_file):
        """在创建对象时，直接加载配置文件的内容"""
        super().__init__()
        self.read(conf_file,encoding='utf-8')

conf=Config(os.path.join(CONF_DIR,'conf.ini'))



# if __name__ == '__main__':
#
#     # conf = ConfigParser()
#     # conf.read('conf.ini',encoding='utf-8')
#     conf=Config('conf.ini')
#     name=conf.get('logging','name')
#     level = conf.get('logging','level')
#     filename = conf.get('logging','filename')
#     sh_level = conf.get('logging','sh_level')
#     fh_level = conf.get('logging','fh_level')
#     print(name)
#     print(level)
