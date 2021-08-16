import unittest
import os
import requests
from jsonpath import jsonpath
from unittestreport import ddt,list_data
from common.handle_excel import HandlExcel
from common.handle_path import DATA_DIR
from common.handle_mysql import HandelDb
from common.handle_conf import conf
class BaseTest:
    @classmethod
    def admin_login(cls):
        url = conf.get('dev', 'base_url') + '/member/login'

        # 1、管理员登录----------------------------------------------------
        # 管理员账号13712345670  pwd:lemonban
        params = {"mobile_phone": conf.get('test_data', 'admin_phone'), "pwd": conf.get('test_data', 'admin_pwd')}
        headers = eval(conf.get('dev', 'headers'))
        response = requests.post(url=url, json=params, headers=headers)
        res = response.json()
        admin_token = jsonpath(res, "$..token")[0]
        admin_headers = headers
        admin_headers["Authorization"] = "Bearer " + admin_token
        cls.admin_headers = admin_headers
        cls.admin_member_id = jsonpath(res, '$..id')[0]
    @classmethod
    def user_login(cls):
        url = conf.get('dev', 'base_url') + '/member/login'
        params = {"mobile_phone": conf.get('test_data', 'mobile_phone'), "pwd": conf.get('test_data', 'pwd')}
        headers = eval(conf.get('dev', 'headers'))
        response = requests.post(url=url, json=params, headers=headers)
        res = response.json()
        cls.token = jsonpath(res, "$..token")[0]
        headers["Authorization"] = "Bearer " + cls.token
        cls.headers = headers
        cls.member_id = jsonpath(res, '$..id')[0]
    @classmethod
    def add_project(cls):
        url = conf.get('dev', 'base_url') + '/loan/add'
        params = {"member_id": cls.member_id,
                  "title": "借钱实现财富自由",
                  "amount": 2000,
                  "loan_rate": 12.0,
                  "loan_term": 3,
                  "loan_date_type": 1,
                  "bidding_days": 5
                  }

        # 第二步：请求添加项目的接口
        response = requests.post(url=url, json=params, headers=cls.headers)
        res = response.json()
        BaseTest.loan_id = jsonpath(res, '$..id')[0]  # 类方法保存参数
    @classmethod
    def audit(cls):
        """审核"""
        url = conf.get('dev', 'base_url')+'/loan/audit'
        params={"loan_id":cls.loan_id,"approved_or_not":True}
        #请求添加项目的接口，进行审核
        response = requests.patch(url=url,json=params,headers=cls.admin_headers)

