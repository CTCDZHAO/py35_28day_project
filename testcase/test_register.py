import unittest
import requests
import os
import random
from unittestreport import ddt,list_data
from common.handle_excel import HandlExcel
from common.handle_path import DATA_DIR
from common.handle_conf import conf
from common.handle_log import my_log
from common.handle_mysql import HandelDb
from common.tools import replace_data
@ddt
class TestRegister(unittest.TestCase):
    excel=HandlExcel(os.path.join(DATA_DIR,'apicases.xlsx'),'register')
    # 读取测试数据
    case=excel.read_data()
    # 请求的地址
    base_url = conf.get('dev', 'base_url')
    # 请求头
    headers = eval(conf.get('dev','headers'))
    db=HandelDb()
    @list_data(case)
    def test_register(self,item):
        #第一步准备测试数据
        # 1、接口地址+路径
        url=self.base_url+item['url']
        # 2、接口的请求参数
        # 判断手机号是否需要替换
        if '#mobile#' in item['data']:#判断是否有可替换字符
            setattr(TestRegister,'mobile',self.random_mobile())
            # TestRegister.mobile=self.random_mobile()#与上一句一致为类添加属性
        item['data']=replace_data(item['data'],TestRegister)
        params = eval(item['data'])
        # 3、请求头
        # headers={"Content-Type": "application/json","X-Lemonban-Media-Type": "lemonban.v2"}
        # 4、请求方法,并小写
        method = item['method'].lower()
        # 5、预期结果
        expected=eval(item['expected'])

        # 第二步请求接口，获取返回的实际结果
        response=requests.request(method,url,json=params,headers=self.headers)
        res=response.json()
        # 查询数据库中该手机号对应的账户数量
        sql='SELECT * FROM futureloan.member WHERE mobile_phone={}'.format(params.get('mobile_phone'))
        count=self.db.find_count(sql)



        # requests.post(url=url,json=params,headers=self.headers)
        # 第三步：断言
        print('预期结果',expected)
        print('实际结果',res)
        try:
            # 断言code和msg字段是否一致
            self.assertEqual(expected['code'],res['code'])
            self.assertEqual(expected['msg'],res['msg'])
            # 判断是否需要sql数据校验
            if item['check_sql']:
                print('数据库中查询的数量为',count)
                self.assertEqual(1,count)
        except AssertionError as  e:
        #     记录日志
             my_log.error("用例-【{}】---执行失败".format(item['title']))
             my_log.error(e)
             # 回写结果到Excel:(不建议，根据公司实际需求决定是否添加)注意：回写Excel需要花费大量时间
             raise e
        else:
            my_log.error("用例-【{}】---执行成功".format(item['title']))

    def random_mobile(self):
        """随机生成手机号"""
        phone= str(random.randint(13000000000,13399999999))
        return phone
        # mobile="133"
        # for i in range(8):
        #     n=random.randint(0,9)
        #     mobile += n