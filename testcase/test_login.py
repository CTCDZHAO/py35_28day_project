import unittest
import os
import requests
from unittestreport import ddt,list_data
from common.handle_excel import HandlExcel
from common.handle_path import DATA_DIR
from common.handle_log import my_log
from common.handle_conf import conf
from common.tools import replace_data
@ddt
class TestLogin(unittest.TestCase):
    excel=HandlExcel(os.path.join(DATA_DIR,'apicases.xlsx'),'login')
    datas=excel.read_data()
    base_url = conf.get('dev','base_url')
    header=eval(conf.get('dev','headers'))
    @list_data(datas)
    def test_login(self,item):
        url= self.base_url+item['url']
        item['data']=replace_data(item['data'],TestLogin)
        data=eval(item['data'])

        method=item['method'].lower()
        expected=eval(item['expected'])
        response=requests.request(method,url,json=data,headers=self.header)
        res=response.json()
        try:
            # self.assertEqual(expected['code'], res['code'])
            # self.assertEqual(expected['msg'], res['msg'])
            self.assertDicIn(expected,res)

        except AssertionError as e:
            my_log.info('用例【{}】-执行失败'.format(item['title']))
            my_log.error(e)
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