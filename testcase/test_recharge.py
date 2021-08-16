"""
充值的前提：登录--》获取token
unittest:
    用例级别的前置：setup
    测试类级别的前置：setupclass:
         1、提取token
         2、提取用户ID
         3、

"""
import os
import unittest
import requests
import re
from jsonpath import jsonpath
from unittestreport import ddt,list_data
from common.handle_excel import HandlExcel
from common.handle_path import DATA_DIR
from common.handle_conf import conf
from common.handle_log import my_log
from common.handle_mysql import HandelDb
from common.tools import replace_data
from testcase.fixture import BaseTest

@ddt
class TestRecharge(unittest.TestCase,BaseTest):
    excel=HandlExcel(os.path.join(DATA_DIR,'apicases.xlsx'),'recharge')
    case=excel.read_data()
    # db = HandelDb()
    @classmethod
    def setUpClass(cls):
        """用例类的前置方法"""
        # # 登录提取token
        # #1、请求登录接口，登录成功提取token
        # url =conf.get('dev','base_url')+'/member/login'
        # params={"mobile_phone":conf.get('test_data','mobile_phone'),"pwd":conf.get('test_data','pwd')}
        # headers=eval(conf.get('dev','headers'))
        # response=requests.post(url=url,json=params,headers=headers)
        # # print(response.json())
        # #2、登录成功之后，去提取token
        # res=response.json()
        # token=jsonpath(res,"$..token")[0]
        # # 将token添加到请求头中
        # headers["Authorization"]="Bearer "+token
        # # 保存含有token的请求头属性
        # cls.headers=headers
        # # setattr(TestRecharge,'headers',headers)
        # # 3、提取用户的ID给充值接口使用
        # cls.member_id=jsonpath(res,'$..id')[0]
        # # print(cls.headers)
        # # print(cls.member_id)
        #


        #     继承封装的登录模块
        cls.user_login()
    @list_data(case)
    def test_recharge(self,item):
        db = HandelDb()
        # 第一步准备数据
        url=conf.get('dev','base_url')+item['url']
        # ************************************************
        # 动态处理需要进行替换的参数--------
        # item['data']=item['data'].replace('#member_id#',str(self.member_id))
        # --------------------------------------
        # 通过封装的正则方法进行替换
        item['data']=replace_data(item['data'],TestRecharge)

        params=eval(item['data'])
        # ********************************************
        # print(params)
        method=item['method']
        expected=eval(item['expected'])
        #----------请求借口之前查询用户的余额
        sql='SELECT leave_amount FROM futureloan.member WHERE mobile_phone={}'.format(conf.get('test_data','mobile_phone'))
        # 执行sql查询余额
        stat_amount=db.find_one(sql)[0]
        print('用力执行之前的用户余额',stat_amount)
        # 第二部：发送请求，获取接口返回的实际结果
        response=requests.request(method,url=url,json=params,headers=self.headers)
        res = response.json()
        end_amount=db.find_one(sql)[0]
        print('用力执行之后的用户余额', end_amount)
        # 第三步断言
        try:
            # self.assertEqual(expected['code'], res['code'])
            # self.assertEqual(expected['msg'], res['msg'])
            self.assertDicIn(expected, res)
        #    断言数据库中用户育=余额的变化

        except AssertionError as e:
            my_log.info('用例【{}】-执行失败'.format(item['title']))
            my_log.error(e)
            if res['code']=='OK':
                # 充值成功
                self.assertEqual(float(end_amount-stat_amount),params['amount'])
            else:
                # 充值失败
                self.assertEqual(float(end_amount-stat_amount),0)
            raise e
        else:
            my_log.info('用例【{}】-执行成功'.format(item['title']))

    def assertDicIn(self, expected, res):
        """字典成员运算的逻辑"""
        for k, v in expected.items():
            if res.get(k) == v:
                pass
            else:
                raise AssertionError("{}not in {}".format(expected, res))


