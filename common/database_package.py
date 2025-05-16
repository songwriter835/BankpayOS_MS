#!/user/bin/env python3
# -*- coding:UTF-8
# 2023/6/28 20:18
import pymysql
from BankpayOS_MS.data.database_info import database_info


class DB(object):
    """
    数据库对象
    """

    def __init__(self):
        """
        功能描述：连接数据库，建立游标
        """
        self.conn = pymysql.connect(**database_info)                 # 连接数据库
        self.curs = self.conn.cursor(pymysql.cursors.DictCursor)    # 建立游标

    def cud_table(self, sql):
        """
        功能描述：增删改，没有返回值
        输入参数：sql
        """
        self.curs.execute(sql)                                      # 执行SQL语句
        self.conn.commit()                                          # 提交SQL语句(5.6版本以下需要)

    def select_table(self, sql):
        """
        功能描述：查
        输入参数：sql
        返回值：list(查询结果)
        """
        self.curs.execute(sql)                                      # 执行SQL语句
        return self.curs.fetchall()                                 # 返回查询结果

    def __del__(self):
        """
        功能描述：关闭游标，关闭连接
        """
        if hasattr(self, 'curs') and self.curs:                                          # 关闭游标
            self.curs.close()
        if hasattr(self, 'conn') and self.conn:                                          # 关闭连接
            self.conn.close()

if __name__ == '__main__':
    db = DB()
    r = db.select_table('select utr_id,amount from `bankpayos-db-bank`.message order by id desc limit 1;')
    print(r)
    amount = r[0].get('amount')
    utr = r[0].get('utr_id')
    print(float(amount))
    print(utr)