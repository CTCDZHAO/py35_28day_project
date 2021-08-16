import pymysql
from common.handle_conf import conf
class HandelDb:
    def __init__(self):
        self.con=pymysql.connect(host=conf.get('mysql','host'),
        port=conf.getint('mysql','port'),#读取类型为getint  ：int类型
        user=conf.get('mysql','user'),
        password=conf.get('mysql','password'),

        )

    def find_one(self,sql):
        cur=self.con.cursor()
        cur.execute(sql)
        self.con.commit()

        res=cur.fetchone()
        cur.close()
        return res
    def find_count(self,sql):
        cur = self.con.cursor()
        res=cur.execute(sql)
        self.con.commit()
        cur.close()
        return res
    def find_all(self,sql):
        cur = self.con.cursor()
        cur.execute(sql)
        self.con.commit()
        # cur.close()
        res=cur.fetchall()
            # cur.close()
        cur.close()
        return res
    def __del__(self):#魔法方法
        print('对象销毁时自动执行')
        # self.con.close()

if __name__ == '__main__':
    sql='SELECT * FROM futureloan.member LIMIT 5'
    # from common.handle_conf import conf
    db=HandelDb()
    res=db.find_one(sql)
    print(res)
    res2=db.find_one(sql)
    print(res2)