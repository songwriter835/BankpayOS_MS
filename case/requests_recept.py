#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @time    : 2025/7/16 20:31

""" a test module """

__author__ = 'songwriter'

import time
import concurrent.futures
from ulid import ULID
from BankpayOS_MS.common.utils import *
from BankpayOS_MS.data.openapi_testcase_info import *
from BankpayOS_MS.common.api import OpenApi

# # 测试数据读取
API = OpenApi()
RESET = "\033[0m"  # 重置样式
BLUE = "\033[34m"  # 设置蓝色
YELLOW = "\033[33m"# 设置黄色

receipt_info = payments_info.get("receipt")
return_url = receipt_info.get("return_url")
is_buyer_kyc = receipt_info.get("is_buyer_kyc")
buyer_name = receipt_info.get("buyer_name")
buyer_email = receipt_info.get("buyer_email")
buyer_phone = receipt_info.get("buyer_phone")
buyer_vpa = receipt_info.get("buyer_vpa")
# 创建收银台-upi

def Checkout():

    # 获取最小代收单金额
    max_amount = API.GetServiceConfigsReceipt(API.getcoinid(fiat_coin[0])).get("data").get("record").get("max_amount")
    print(f"{BLUE}用例名称：正确传入参数，能够创建收银台代收交易{RESET}")

    # 创建收银台
    bill_id = str(ULID())
    if is_buyer_kyc:
        adata = API.Checkout(
            f'{bill_id}',
            f'{max_amount}',
            f'{API.getcoinid(fiat_coin[0])}',
            f'{country}',
            f'{return_url}',
            is_buyer_kyc,
            f'{buyer_name}'
        )
    else:
        adata = API.Checkout(
            f'{bill_id}',
            f'{min_amount}',
            f'{API.getcoinid(fiat_coin[0])}',
            f'{country}',
            f'{return_url}',
            is_buyer_kyc,
            f'{buyer_name}',
            f'{buyer_email}',
            f'{buyer_phone}'
        )
    print("创建收银台", adata)


    assert adata.get("code") == 1000 and adata.get("msg") == 'Success', \
        f'{YELLOW}创建收银台代收交易失败，错误码[{adata.get("code")}]{adata.get("msg")}'

    checkout_url = adata.get('data').get('checkout_url')
    url_status_code = send_request(checkout_url, 'get', )[0].status_code

    assert url_status_code == 200, f'{YELLOW}生成收银台链接访问失败，状态码[{url_status_code}]，链接[{url}]'
def run_test_checkout():

    Checkout()  # 调用你的测试函数

if __name__ == '__main__':
    for i in range(100):
        CONCURRENCY = 200  # 并发数量

        with concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENCY) as executor:
            futures = [executor.submit(run_test_checkout) for _ in range(CONCURRENCY)]

            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"执行异常: {e}")
        time.sleep(0.1)


