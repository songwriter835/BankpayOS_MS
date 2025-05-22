#!/user/bin/env python3
# -*- coding:UTF-8
# 2023/6/28 20:18
import pymysql
from BankpayOS_MS.data.database_info import database_info


class DB(object):

    def __enter__(self):
        """
        功能描述：连接数据库，建立游标
        """
        self.conn = pymysql.connect(**database_info)
        self.curs = self.conn.cursor(pymysql.cursors.DictCursor)
        return self

    def cud_table(self,sql):
        """
        功能描述：增删改，没有返回值
        输入参数：sql
        """
        self.curs.execute(sql)
        self.conn.commit()

    def select_table(self,sql):
        """
        功能描述：查
        输入参数：sql
        返回值：list(查询结果)
        """
        self.curs.execute(sql)
        return self.curs.fetchall()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        功能描述：关闭游标，关闭连接
        """
        if hasattr(self, 'curs') and self.curs:  # 关闭游标
            self.curs.close()
        if hasattr(self, 'conn') and self.conn:  # 关闭连接
            self.conn.close()

if __name__ == '__main__':

    with  DB() as db:
        query_sql = "select amount, utr_id from message order by id desc limit 1;"
        result = db.select_table(query_sql)[0]
        print(result)