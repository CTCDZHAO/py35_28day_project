import unittest
import os
import requests
from jsonpath import jsonpath
from unittestreport import ddt,list_data
from common.handle_excel import HandlExcel
from common.handle_path import DATA_DIR
from common.handle_mysql import HandelDb
from common.handle_conf import conf
from common.tools import replace_data
from common.handle_log import my_log
@ddt
class TestAdd(unittest.TestCase):
    excel = HandlExcel(os.path.join(DATA_DIR,'apicases.xlsx'),'add')
    case=excel.read_data()
    db=HandelDb()
    @classmethod
    def setUpClass(cls):
        url =conf.get('dev','base_url')+'/member/login'
        params={"mobile_phone":conf.get('test_data','mobile_phone'),"pwd":conf.get('test_data','pwd')}
        headers=eval(conf.get('dev','headers'))
        reponse=requests.post(url,json=params,headers=headers)
        res=reponse.json()
        print(res)
        token = jsonpath(res, "$..token")[0]
        # 将token添加到请求头中
        headers["Authorization"] = "Bearer " + token
        cls.headers=headers
        # 提取用户的ID给接口使用
        cls.member_id = jsonpath(res, '$..id')[0]

    @list_data(case)
    def test_add(self,item):
        #第一步准备数据
         url=conf.get('dev','base_url')+item['url']
         item['data']=replace_data(item['data'],TestAdd)
         params=eval(item['data'])
         expected=eval(item['expected'])
         method=item['method']
         # 查询数据库该用户的项目数量
         sql="SELECT * FROM futureloan.loan WHERE member_id={}".format(self.member_id)
         start_count=self.db.find_count(sql)
         print('调用接口之前的项目个数',start_count)
        #第二步请求接口
         response=requests.request(method=method,url=url,json=params,headers=self.headers)
         res=response.json()
        # 调用接口后查询用户项目数量
         end_count=self.db.find_count(sql)

         print('调用接口之前的项目个数', end_count)
        #接口断言
         try:
             self.assertEqual(expected['code'],res['code'])
             self.assertEqual(expected['msg'],res['msg'])
             # 根据添加项目的情况：是否成功，来对数据库进行校验
             if res['msg']=="OK":
                self.assertEqual(end_count-start_count,1)
             else:
                 self.assertEqual(end_count-start_count,0)
         except AttributeError as e:
             my_log.info('用例【{}】-执行失败'.format(item['title']))
             my_log.error(e)
             raise e
         else:
             my_log.info('用例【{}】-执行成功'.format(item['title']))

