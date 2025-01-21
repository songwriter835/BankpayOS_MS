#!/user/bin/env python3
# -*- coding:UTF-8
# 2024/10/16 20:26
"""
公共函数

"""
import time, csv, os, hashlib, requests
import random

base_path = os.path.dirname(os.path.dirname(__file__))  # 项目路径
case_path = base_path + "/case"      # 测试用例路径
common_path = base_path + "/common"  # 公共函数路径
data_path = base_path + "/data"      # 测试数据路径
report_path = base_path + "/report"  # 测试报告路径

get_md5 = lambda s: hashlib.md5(s.encode('utf8')).hexdigest()  # 对字符串进行md5加密

def get_time():
    """
    功能描述: 获取当前时间
    返回值: str XXXX-XX-XX-XX-XX-XX
    """
    return time.strftime('%Y-%m-%d-%H-%M-%S')


def read_csv(file):
    """
    功能描述: 读取CSV文件
    输入参数: 文件路径
    返回值: list 文件每一行为一个list
    """
    # 判断路径是否存在
    if not os.path.exists(file):
        return "输入路径有误，未找到该文件"
    # 打开指定路径文件
    with open(file, encoding='utf-8') as f:
        return list(csv.reader(f))


def get_case_path():
    """
    功能描述: 获取测试用例路径
    返回值: str
    """
    return case_path


def str_split(stra):
    dic = {}
    for i in stra.strip().split():
        t = i.split("=")
        dic[t[0]] = t[1]

    """
    功能描述: 'username=xxx\npassword=xxx' >>> {'username': 'xxx', 'password': 'xxx'}
    返回值: dict
    """
    return dic


def send_request(url, method, data=None, headers=None):
    session = requests.session()
    res = None
    """
    功能描述: 发送请求
    返回值: tuple(res对象，session对象)
    """
    if method.lower() == "get":
        res = session.get(url=url, params=data, headers=headers)
    elif method.lower() == "post":
        res = session.post(url=url, data=data, headers=headers)
    elif method.lower() == "put":
        ...
    else:
        return False, "method Error"
    return res, session

def check_utf(string):
    """
    编码检查
    """
    for i, char in enumerate(string):
        try:
            char.encode('latin-1')
        except UnicodeEncodeError:
            return f"不能编码的位置 {i}: {char}"

def random_12num():
    return ''.join(str(random.randint(0, 9)) for _ in range(12))


if __name__ == '__main__':
    ...
