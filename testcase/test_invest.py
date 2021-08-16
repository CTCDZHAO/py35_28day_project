"""
前置条件：
   1、普通用户登录（类级别）
   2、管理员登录（类级别）
   3、添加项目（类级别）
   4、管理员审核（类级别）

用例前置操作的封装优化：
    1、把多个用例要使用的一些前置步骤封装到一个类中
    2、需要使用这些前置步骤的测试类，直接去继承（多继承）我们封装好的前置步骤方法
    3、在类级别的前和用例级别的前置中，调用对应的前置方法即可



用例方法:
    1\准备数据
    2、发送请求
    3、断言
    #s数据库校验：
     用户表：用户余额投资前后会发生变化
        投资前后==投资金额
     流水记录表：投资成功会新增一个记录
          投资前后用户的投资流水数量==新增的投资量==1
     投资表：投资成功后新增一条投资记录
           投资前后用户的投资记录==新增的投资记录==1
    ----------扩展投资满标的情况：会生成回款计划-----
             1、先把项目的投资记录id都查询出来
             2、遍历投资记录ID
             3、根据没一个投资记录ID


"""
import unittest
import os
import requests
from jsonpath import jsonpath
from unittestreport import ddt,list_data
from common.handle_excel import HandlExcel
from common.handle_path import DATA_DIR
from common.handle_mysql import HandelDb
from common.handle_conf import conf
from testcase.fixture import BaseTest
from common.tools import replace_data
from common.handle_log import my_log
@ddt
class TestInvest(unittest.TestCase,BaseTest):
    excel=HandlExcel(os.path.join(DATA_DIR,'apicases.xlsx'),'invest')
    case=excel.read_data()
    db=HandelDb()
    @classmethod
    def setUpClass(cls):
       #  url = conf.get('dev', 'base_url') + '/member/login'
       #
       #  # 1、管理员登录----------------------------------------------------
       #  # 管理员账号13712345670  pwd:lemonban
       #  params = {"mobile_phone": conf.get('test_data', 'admin_phone'), "pwd": conf.get('test_data', 'admin_pwd')}
       #  headers = eval(conf.get('dev', 'headers'))
       #  response = requests.post(url=url, json=params, headers=headers)
       #  res = response.json()
       #  admin_token = jsonpath(res, "$..token")[0]
       #  admin_headers = headers
       #  admin_headers["Authorization"] = "Bearer " + admin_token
       #  cls.admin_headers = admin_headers
       #  cls.admin_member_id = jsonpath(res, '$..id')[0]
       #
       #  # 2、普通用户登录--------------------------------------------------------------
       #  params = {"mobile_phone": conf.get('test_data', 'mobile_phone'), "pwd": conf.get('test_data', 'pwd')}
       #  headers = eval(conf.get('dev', 'headers'))
       #  response = requests.post(url=url, json=params, headers=headers)
       #  res = response.json()
       #  token = jsonpath(res, "$..token")[0]
       #  headers["Authorization"] = "Bearer " + token
       #  cls.headers = headers
       #  cls.member_id = jsonpath(res, '$..id')[0]
       #  print(cls.admin_headers, cls.headers)
       #
       # # 3、新增项目------------------------------------
       #  url = conf.get('dev', 'base_url') + '/loan/add'
       #  params = {"member_id": cls.member_id,
       #            "title": "借钱实现财富自由",
       #            "amount": 2000,
       #            "loan_rate": 12.0,
       #            "loan_term": 3,
       #            "loan_date_type": 1,
       #            "bidding_days": 5
       #            }
       #
       #  # 第二步：请求添加项目的接口
       #  response = requests.post(url=url, json=params, headers=cls.headers)
       #  res = response.json()
       #  TestInvest.loan_id = jsonpath(res, '$..id')[0]  # 类方法保存参数


       #----------------------将以上方法封装为一个模块----------
       # 调用方法
       # 管理员登录
       cls.admin_login()
       # 普通用户登录
       cls.user_login()
       # 添加项目
       cls.add_project()
       #    审核
       cls.audit()

    @list_data(case)
    def test_invest(self,item):
        #1、准备用例数据
        url = conf.get('dev', 'base_url') + item['url']
        item['data'] = replace_data(item['data'], TestInvest)
        params = eval(item['data'])
        method = item['method']
        expected = eval(item['expected'])
#         -----------投资之前 查询数据库--------
        #查询用户表
        sql1='SELECT leave_amount FROM futureloan.member WHERE mobile_phone={}'.format(self.member_id)
        #投资记录表
        sql2='SELECT count(*) FROM futureloan.invest WHERE mobile_phone={}'.format(self.member_id)
        #查流水记录
        sql3 = 'SELECT count(*) FROM futureloan.financelog WHERE pay_member_id={}'.format(self.member_id)
        if item['check_sql']:
            s_amount=self.db.find_one(sql1)[0]
            s_invset=self.db.find_count(sql2)
            s_finacelog=self.db.find_count(sql3)

#         2、发送请求
        response=requests.request(method=method,url=url,json=params,headers=self.headers)
        res=response.json()
        #----------投资后查询数据库-------
        if item['check_sql']:
            e_amount=self.db.find_one(sql1)[0]
            e_invset=self.db.find_count(sql2)
            e_finacelog=self.db.find_count(sql3)
        #3、断言
        try:
            self.assertEqual(expected['code'], res['code'])
            self.assertIn(expected['msg'], res['msg'])
            #数据库校验
            if item['check_sql']:
                #断言用户余额
                self.assertEqual(params['amount'],float(s_amount-e_amount))
                #断言投资记录
                self.assertEqual(1,e_invset-s_invset)
                #流水记录
                self.assertEqual(1,e_finacelog-s_finacelog)
        except AssertionError as e:
            my_log.info('用例【{}】-执行失败'.format(item['title']))
            my_log.error(e)
            raise e
        else:
            my_log.info('用例【{}】-执行成功'.format(item['title']))
# self是实例方法的第一个参数，代表的是实例对像本身
#cls 是类方法的第一个参数，代表的时类的本身