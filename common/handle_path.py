"""
此模块专门用来处理项目中的绝对路径

"""

import os
# 获取项目的根目录
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 获取用例数据文件夹所在目录的绝对路径
DATA_DIR=os.path.join(BASE_DIR,'datas')

#配置文件的根目录
CONF_DIR=os.path.join(BASE_DIR,'conf')

#日志所在目录
LOG_DIR=os.path.join(BASE_DIR,'logs')

# 报告所在目录
REPORT_DIR=os.path.join(BASE_DIR,'reports')

# 用例模块所在目录
CASE_DIR=os.path.join(BASE_DIR,'testcase')