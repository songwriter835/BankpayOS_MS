#!/user/bin/env python3
# -*- coding:UTF-8
# 2023/6/28 20:18
import pymysql
from BankpayOS_MS.data.database_info import database_info
from pymysql.cursors import DictCursor
from sshtunnel import SSHTunnelForwarder

class DB(object):
    def __init__(self):
        self.ssh_config = {
            'ssh_host': database_info.get('ssh_host'),
            'ssh_port': database_info.get('ssh_port', 22),
            'ssh_username': database_info.get('ssh_username'),
            'ssh_pkey': database_info.get('ssh_pkey'),
        }
        self.db_config = {
            'host': database_info['host'],
            'port': database_info['port'],
            'user': database_info['user'],
            'password': database_info['password'],
            'database': database_info['database'],
            "cursorclass": DictCursor
        }
        self.tunnel = None
        self.conn = None
        self.curs = None

    def __enter__(self):
        """
        功能描述：建立 SSH 隧道（如有）并连接数据库
        """
        if self.ssh_config['ssh_host']:
            # 使用 SSH 隧道
            self.tunnel = SSHTunnelForwarder(
                (self.ssh_config['ssh_host'], self.ssh_config['ssh_port']),
                ssh_username=self.ssh_config['ssh_username'],
                ssh_pkey=self.ssh_config['ssh_pkey'],
                remote_bind_address=(self.db_config['host'], self.db_config['port'])
            )
            self.tunnel.start()
            self.db_config['host'] = '127.0.0.1'
            self.db_config['port'] = self.tunnel.local_bind_port

        # 连接数据库
        self.conn = pymysql.connect(**self.db_config)
        self.curs = self.conn.cursor(DictCursor)
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
        if self.tunnel:
            self.tunnel.stop()

if __name__ == '__main__':

    with  DB() as db:
        query_sql = "select amount, utr_id from message order by id desc limit 1;"
        result = db.select_table(query_sql)[0]
        print(result)