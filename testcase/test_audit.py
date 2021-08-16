"""
审核接口：管理员去审核
审核的前置条件：
   1、管理员登录（类级别）

   2 普通用户的角色添加项目
      1)\普通用户登录（类级别的前置）
      2）、创建一个项目（用例级别的前置）


"""
import unittest
import os
import requests
from jsonpath import jsonpath
from unittestreport import ddt,list_data
from common.handle_conf import conf
from common.handle_excel import HandlExcel
from common.handle_path import DATA_DIR
from common.tools import replace_data
from common.handle_log import my_log
from common.handle_mysql import HandelDb

@ddt
class TestAudit(unittest.TestCase):
    excel=HandlExcel(os.path.join(DATA_DIR,'apicases.xlsx'),'audit')
    case=excel.read_data()
    db=HandelDb()
    url = conf.get('dev', 'base_url') + '/member/login'
    headers = eval(conf.get('dev', 'headers'))
    @classmethod
    def setUpClass(cls):
        url = conf.get('dev', 'base_url') + '/member/login'

        # 1、管理员登录----------------------------------------------------
        #管理员账号13712345670  pwd:lemonban
        params = {"mobile_phone": conf.get('test_data', 'admin_phone'), "pwd": conf.get('test_data', 'admin_pwd')}
        headers = eval(conf.get('dev', 'headers'))
        response = requests.post(url=url, json=params, headers=headers)
        res = response.json()
        admin_token = jsonpath(res, "$..token")[0]
        admin_headers=headers
        admin_headers["Authorization"] = "Bearer " + admin_token
        cls.admin_headers = admin_headers
        cls.admin_member_id = jsonpath(res, '$..id')[0]


       #2、普通用户登录--------------------------------------------------------------
        params = {"mobile_phone": conf.get('test_data', 'mobile_phone'), "pwd": conf.get('test_data', 'pwd')}
        headers = eval(conf.get('dev', 'headers'))
        response = requests.post(url=url, json=params, headers=headers)
        res = response.json()
        token = jsonpath(res, "$..token")[0]
        headers["Authorization"] = "Bearer " + token
        cls.headers = headers
        cls.member_id = jsonpath(res, '$..id')[0]
        print(cls.admin_headers,cls.headers)
    def setUp(self):
        #用例的前置添加项目
        #第一步：准备数据
        url=conf.get('dev','base_url')+'/loan/add'
        params={"member_id":self.member_id,
                "title":"借钱实现财富自由",
                "amount":2000,
                "loan_rate":12.0,
                "loan_term":3,
                "loan_date_type":1,
                "bidding_days":5
                }

        #第二步：请求添加项目的接口
        response=requests.post(url=url,json=params,headers=self.headers)
        res=response.json()
        TestAudit.loan_id=jsonpath(res,'$..id')[0]#类方法保存参数

        #第三步：提取项目id

    @list_data(case)
    def test_audit(self,item):
        url=conf.get('dev','base_url')+item['url']
        item['data']=replace_data(item['data'],TestAudit)
        params=eval(item['data'])
        method=item['method']
        expected=eval(item['expected'])
        #第二部：请求接口
        response=requests.request(method=method,url=url,json=params,headers=self.admin_headers)
        res=response.json()
        #判断是否是审核通过用例，并且审核成功，如果是则保存项目ID，查询项目
        if item['title']=="审核通过" and res['msg']=="OK":
            TestAudit.pass_loan_id=self.loan_id
            # 或者TestAudit.pass_loan_id=params['loan_id']
        print("预期结果",expected)
        print("实际结果",res)
        #第三步：断言
        try:
            self.assertEqual(expected['code'], res['code'])
            self.assertEqual(expected['msg'], res['msg'])
            # 根据添加项目的情况：是否成功，来对数据库进行校验
            if item['check_sql']:
                sql=item['check_sql'].format(self.loan_id)
                status=self.db.find_one(sql)
                print('数据库中的状态',status)


        except AttributeError as e:
            my_log.info('用例【{}】-执行失败'.format(item['title']))
            my_log.error(e)
            raise e
        else:
            my_log.info('用例【{}】-执行成功'.format(item['title']))
