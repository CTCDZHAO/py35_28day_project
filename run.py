import unittestreport
import unittest
from common.handle_path import CASE_DIR,REPORT_DIR




class Runtest:
    """程序的入口函数"""
    def main(self):
        suite=unittest.defaultTestLoader.discover(CASE_DIR)
        runner=unittestreport.TestRunner(suite,
                                         filename='python35.html',
                                         report_dir=REPORT_DIR,
                                         tester='赵海光',
                                         title='测试报告')
        runner.run()
    #钉钉推送消息
        webhook='https://oapi.dingtalk.com/robot/send?access_token=44c2b33eac42f7d27fed472113cad8155b98383265418ccc2c3b96fb4a148b59'
        runner.dingtalk_notice(url=webhook,key='测试')
    #企业微信参考企业微信api

        #发送报告到邮件
        # runner.send_email(host='smtp.qq.com',
        #                   port=465,
        #                   user='754125217@qq.com',
        #                   to_addrs='sishenheiqi114@163.com,zhaohaiguang754@163.com',
        #                   password='lchpiyhjhqgmbfdg',
        #                   is_file=True)
#_-------------------扩展：自定义邮件的内容和标题----------
# from unittestreport.core.sendEmail import SendEmail
# em=SendEmail(host='smtp.qq.com',
#                           port=465,
#                           user='754125217@qq.com',
#                           password='lchpiyhjhqgmbfdg',)
# em.send_email( subject="测试报告", content='邮件内容', filename=None, to_addrs='sishenheiqi114@163.com,zhaohaiguang754@163.com')

if __name__ == '__main__':
    test=Runtest()
    test.main()

"""扩展知识扩展：
一、测试结果推送：
    1、通过邮件发送给相关人邮箱（邮箱的smtp功能）
    2、推送结果到钉钉群
    


"""




