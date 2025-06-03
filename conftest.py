#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @time    : 2024/11/3 11:41
"""
==========  前后置配置  ==========
User front and back configuration
"""
__author__ = 'songwriter'


#  登录前置
# @pytest.fixture(scope='class', name="login")
# def login():
#     url = 'http://localhost:5000//login'
#     data = {"username": "admin", "password": "Milor123"}
#     header = None
#     res = send_request(url, method="POST", data=data, headers=header)   # 获取请求对象和session对象
#     return res


def pytest_collection_modifyitems(items):
    """pytest_collection_modifyitems 是pytest中的一个hook函数（内置的）
    是为了在测试用例收集完成后对测试项的 name 和 nodeid 进行处理，
    以确保它们在控制台上的显示是正确的。
    这段代码通过编码和解码操作来处理中文字符，从而解决了可能出现的乱码问题。"""
    print('\n')
    for item in items:
        print("处理前的测试用例名称", item.name)
        print("处理前的测试用例节点", item._nodeid)
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")