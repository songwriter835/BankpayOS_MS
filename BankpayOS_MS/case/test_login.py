# #!/user/bin/env python3
# # -*- coding:UTF-8
# # 2024/10/16 21:27
# import pytest
# from BankpayOS_MS.common.utils import *
# # 测试数据读取
# file = data_path + "\\test_login.csv"
# test_data = read_csv(file)
#
#
# class Test_login(object):
#
#     @staticmethod
#     def login(url, method, data, header=None):
#         """
#         功能描述: 登录函数
#         :param url:
#         :param method:
#         :param data:
#         :param header:
#         :return: 响应内容(json)
#         """
#         res = send_request(url, method, data, header)[0]
#         return res.json()
#
#     @staticmethod
#     @pytest.mark.skipif(test_data[5][1].lower() != 'y', reason="子版本不测试该接口")
#     @pytest.mark.parametrize("case_info", test_data[7:], ids=[i[0] for i in test_data[7:]])
#     def test_login(case_info):
#         url = test_data[1][1]
#         method = test_data[2][1]
#         data = str_split(case_info[1])
#         actual = Test_login.login(url=url, method=method, data=data)
#         assert str(actual.get("code")) == str(case_info[2]) and actual.get("msg") == case_info[3]
#
#
# if __name__ == '__main__':
#     pytest.main(["-v", __file__])
