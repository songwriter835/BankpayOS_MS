import pytest
from ulid import ULID
from BankpayOS_MS.common.api  import OpenApi
from BankpayOS_MS.common.utils import *
from BankpayOS_MS.common.database_package import DB
from BankpayOS_MS.data.openapi_testcase_info import *
from BankpayOS_MS.data.EnvConfig import env
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

class Test_api:




    # 确认代收交易-upi-bank
    @staticmethod
    def test_ConfirmReceipt1():

        # 如果是线上环境，没有真实汇款流水，pass
        if env == 'prod':
            return

        # 获取最大代收单金额
        max_amount = [i.get("max_amount") for i in
                      API.GetServiceConfigsReceipt(API.getcoinid(fiat_coin[0])).get("data").get("records")
                      if i.get("payment_method") == f'{payment_method[0]}']
        max_amount = sorted(max_amount)[0]

        print(f"{BLUE}用例名称：正确传入参数，能够确认代收交易-bank接单{RESET}")

        # 创建代收记录
        bill_id = str(ULID())
        adata = API.CreateReceipt(bill_id,
                                  max_amount,
                                  f'{country}',
                                  f'{API.getcoinid(fiat_coin[0])}',
                                  f'{payment_method[0]}')
        print("创建代收记录", adata)

        assert adata.get("code") == 1000 and adata.get("msg") == 'Success', \
            f'{YELLOW}创建代收交易失败，错误码[{adata.get("code")}]{adata.get("msg")}'
        # 记录record_id
        record_ida = adata.get("data").get("record_id")
        # 确认代收记录
        start_time = time.time()  # 记录开始时间
        utr_id = None
        timeout = 10  # 设定超时时间 /s
        while True:
            with  DB() as db:
                water = db.select_table("select utr_id,amount from `bankpayos-db-bank`.message order by id desc limit 1;")
            water_amount = str(int(water[0].get("amount")))
            if water_amount == max_amount and "0000" + record_ida[-8:] == water[0].get("utr_id"):
                utr_id = water[0].get("utr_id")
                break
            else:
                if time.time() - start_time > timeout:
                    print(f"{YELLOW}10秒未查找到该流水！utr获取失败")
                    break

        bdata = API.ConfirmReceipt(bill_id=bill_id, pay_proof_id=utr_id)
        print("确认代收记录", bdata)

        assert bdata.get("code") == 1000 and bdata.get("msg") == 'Success', \
            f'{YELLOW}确认代收交易失败，错误码[{bdata.get("code")}]{bdata.get("msg")}'
        assert bdata.get("data").get("status") in ['Confirming', 'Success'], \
            f'{YELLOW}status不正确,确认后:{bdata.get("data").get("status")}'

        # 查询代收记录
        cdata = API.GetReceipt(record_id=record_ida)
        print("查询代收记录", cdata)

        assert cdata.get("code") == 1000 and cdata.get("msg") == 'Success' and cdata.get("data") != [],\
            f'{YELLOW}查询代收交易失败，错误码[{cdata.get("code")}]{cdata.get("msg")}'
        assert cdata.get("data").get("status") in ['Confirming', 'Success'], \
            f'{YELLOW}status不正确,确认后:{cdata.get("data").get("status")}'

    # 取消代收交易-upi
    @staticmethod
    def test_CancelReceipt():

        # 获取最小代收单金额
        min_amount = [i.get("min_amount") for i in
                      API.GetServiceConfigsReceipt(API.getcoinid(fiat_coin[0])).get("data").get("records")
                      if i.get("payment_method") == f'{payment_method[0]}']
        min_amount = sorted(min_amount)[0]

        print(f"{BLUE}用例名称：正确传入参数，能够取消代收交易{RESET}")

        # 创建代收记录
        bill_id = str(ULID())
        adata = API.CreateReceipt(bill_id,
                                  min_amount,
                                  f'{country}',
                                  f'{API.getcoinid(fiat_coin[0])}',
                                  f'{payment_method[0]}')
        print("创建代收记录", adata)

        assert adata.get("code") == 1000 and adata.get("msg") == 'Success', \
            f'{YELLOW}创建代收交易失败，错误码[{adata.get("code")}]{adata.get("msg")}'

        # 取消代收记录
        bdata = API.CancelReceipt(bill_id)
        print("取消代收记录", bdata)

        assert bdata.get("code") == 1000 and bdata.get("msg") == 'Success', \
            f'{YELLOW}取消代收交易失败，错误码[{bdata.get("code")}]{bdata.get("msg")}'
        assert bdata.get("data").get("status") == 'Failure' and bdata.get("data").get("reason") == 'USER_CANCEL', \
            f'{YELLOW}status不正确,取消后:{bdata.get("data").get("status")}， reason={bdata.get("data").get("reason")}'

        # 查询代收记录
        cdata = API.GetReceipt(bill_id=bill_id)
        print("查询代收记录", cdata)

        assert cdata.get("code") == 1000 and cdata.get("msg") == 'Success' and cdata.get("data") != [], \
            f'{YELLOW}查询代收交易失败，错误码[{cdata.get("code")}]{cdata.get("msg")}'
        assert cdata.get("data").get("status") == 'Failure' and cdata.get("data").get("reason") == 'USER_CANCEL', \
            f'{YELLOW}status不正确,取消后:{cdata.get("data").get("status")}， reason={cdata.get("data").get("reason")}'

    # 取消代收交易-upi-bank
    @staticmethod
    def test_CancelReceipt1():

        # 获取最大代收单金额
        max_amount = [i.get("max_amount") for i in
                      API.GetServiceConfigsReceipt(API.getcoinid(fiat_coin[0])).get("data").get("records")
                      if i.get("payment_method") == f'{payment_method[0]}']
        max_amount = sorted(max_amount)[0]

        print(f"{BLUE}用例名称：正确传入参数，能够取消代收交易-bank接单{RESET}")

        # 创建代收记录
        bill_id = str(ULID())
        adata = API.CreateReceipt(bill_id,
                                  max_amount,
                                  f'{country}',
                                  f'{API.getcoinid(fiat_coin[0])}',
                                  f'{payment_method[0]}')
        print("创建代收记录", adata)
        assert adata.get("code") == 1000 and adata.get("msg") == 'Success', \
            f'{YELLOW}创建代收交易失败，错误码[{adata.get("code")}]{adata.get("msg")}'

        # 取消代收记录
        bdata = API.CancelReceipt(bill_id)
        print("取消代收记录", bdata)
        assert bdata.get("code") == 1000 and bdata.get("msg") == 'Success', \
            f'{YELLOW}取消代收交易失败，错误码[{bdata.get("code")}]{bdata.get("msg")}'
        assert bdata.get("data").get("status") == 'Failure' and bdata.get("data").get("reason") == 'USER_CANCEL', \
            f'{YELLOW}status不正确,取消后:{bdata.get("data").get("status")}， reason={bdata.get("data").get("reason")}'

        # 查询代收记录
        cdata = API.GetReceipt(bill_id=bill_id)
        print("查询代收记录", cdata)

        assert cdata.get("code") == 1000 and cdata.get("msg") == 'Success' and cdata.get("data") != [],\
            f'{YELLOW}查询代收交易失败，错误码[{cdata.get("code")}]{cdata.get("msg")}'
        assert cdata.get("data").get("status") == 'Failure' and cdata.get("data").get("reason") == 'USER_CANCEL', \
            f'{YELLOW}status不正确,取消后:{cdata.get("data").get("status")}， reason={cdata.get("data").get("reason")}'

    # 查询代收记录-upi-bill_id
    @staticmethod
    def test_GetReceipt():

        # 获取最小代收单金额
        min_amount = [i.get("min_amount") for i in
                      API.GetServiceConfigsReceipt(API.getcoinid(fiat_coin[0])).get("data").get("records")
                      if i.get("payment_method") == f'{payment_method[0]}']
        min_amount = sorted(min_amount)[0]

        print(f"{BLUE}用例名称：正确传入参数，能够查询代收交易{RESET}")

        # 创建代收记录
        bill_id = str(ULID())
        adata = API.CreateReceipt(bill_id,
                                  min_amount,
                                  f'{country}',
                                  f'{API.getcoinid(fiat_coin[0])}',
                                  f'{payment_method[0]}')
        print("创建代收记录", adata)

        assert adata.get("code") == 1000 and adata.get("msg") == 'Success', \
            f'{YELLOW}创建代收交易失败，错误码[{adata.get("code")}]{adata.get("msg")}'

        # 查询代收记录
        Test_api.bill_id = adata.get('data').get("bill_id")
        bdata = API.GetReceipt(bill_id=Test_api.bill_id)
        print("查询代收记录", bdata)

        assert bdata.get("code") == 1000 and bdata.get("msg") == 'Success' and bdata.get("data") != [],\
            f'{YELLOW}查询代收交易失败，错误码[{bdata.get("code")}]{bdata.get("msg")}'
        assert adata.get("data").get("status") == bdata.get("data").get("status"), \
            f'{YELLOW}status不一致,创建:{adata.get("data").get("state")}和查询:{bdata.get("data").get("status")}'

    # 查询代收记录-upi-record_id
    @staticmethod
    def test_GetReceipt1():

        # 获取最小代收单金额
        min_amount = [i.get("min_amount") for i in
                      API.GetServiceConfigsReceipt(API.getcoinid(fiat_coin[0])).get("data").get("records")
                      if i.get("payment_method") == f'{payment_method[0]}']
        min_amount = sorted(min_amount)[0]

        print(f"{BLUE}用例名称：正确传入参数，能够查询代收交易{RESET}")

        # 创建代收记录
        bill_id = str(ULID())
        adata = API.CreateReceipt(bill_id,
                                  min_amount,
                                  f'{country}',
                                  f'{API.getcoinid(fiat_coin[0])}',
                                  f'{payment_method[0]}')
        print("创建代收记录", adata)

        assert adata.get("code") == 1000 and adata.get("msg") == 'Success', \
            f'{YELLOW}创建代收交易失败，错误码[{adata.get("code")}]{adata.get("msg")}'

        # 查询代收记录
        record_ida = adata.get('data').get("record_id")
        # 订单id写入文件，其他查询用例依赖
        with open(f"{data_path}/record_ids_test.txt", "a", encoding="utf-8") as file:
            file.write(record_ida + " ")
        with open(f"{data_path}/bill_ids_test.txt", "a", encoding="utf-8") as file:
            file.write(bill_id + " ")
        bdata = API.GetReceipt(record_id=record_ida)
        print("查询代收记录", bdata)

        assert bdata.get("code") == 1000 and bdata.get("msg") == 'Success' and bdata.get("data") != [],\
            f'{YELLOW}查询代收交易失败，错误码[{bdata.get("code")}]{bdata.get("msg")}'
        assert adata.get("data").get("status") == bdata.get("data").get("status"), \
            f'{YELLOW}status不一致,创建:{adata.get("data").get("state")}和查询:{bdata.get("data").get("status")}'

    # 查询代收记录列表-time
    @staticmethod
    def test_GetReceiptList():

        print(f"{BLUE}用例名称：传入当前时间往前推三个月时间戳，能够查询代收交易列表{RESET}")

        # 查询代收记录列表
        adata = API.GetReceiptList(int(str(time.time() - 89 * 24 * 3600).split(".")[0]),
                           int(str(time.time()).split(".")[0]))
        print("查询代收记录列表", adata)

        assert adata.get("code") == 1000 and adata.get("msg") == 'Success', \
            f'{YELLOW}查询代收交易列表失败，错误码[{adata.get("code")}]{adata.get("msg")}'
        assert len(adata.get("data").get('records')) > 4, \
            f'{YELLOW}查询结果订单数量不准确:{adata.get("data").get('records')}'

    # 查询代收记录列表-upi-record_ids
    @staticmethod
    def test_GetReceiptList1():

        print(f"{BLUE}用例名称：传入record_ids，能够查询代收交易列表{RESET}")

        # 查询代收记录列表
        # 获取record_ids文件内容
        with open(f"{data_path}/record_ids_test.txt", encoding="utf-8") as file:
            record_ids = file.read().split()

        adata = API.GetReceiptList(record_ids = record_ids)
        print("查询代收记录列表", adata)

        assert adata.get("code") == 1000 and adata.get("msg") == 'Success', \
            f'{YELLOW}查询代收交易列表失败，错误码[{adata.get("code")}]{adata.get("msg")}'
        assert len(adata.get("data").get('records')) == len(record_ids), \
            f'{YELLOW}查询结果订单数量不准确:{adata.get("data").get('records')}'

    # 查询代收记录列表-upi-bill_ids
    @staticmethod
    def test_GetReceiptList2():

        print(f"{BLUE}用例名称：传入bill_ids，能够查询代收交易列表{RESET}")

        # 查询代收记录列表
        # 获取record_ids文件内容
        with open(f"{data_path}/bill_ids_test.txt", encoding="utf-8") as file:
            bill_ids = file.read().split()

        adata = API.GetReceiptList(bill_ids = bill_ids)
        print("查询代收记录列表", adata)

        assert adata.get("code") == 1000 and adata.get("msg") == 'Success', \
            f'{YELLOW}查询代收交易列表失败，错误码[{adata.get("code")}]{adata.get("msg")}'
        assert len(adata.get("data").get('records')) == len(bill_ids), \
            f'{YELLOW}查询结果订单数量不准确:{adata.get("data").get('records')}'

    # 创建代付记录-upi
    @staticmethod
    def test_CreatePayment():

        # 获取最小代付单金额
        min_amount = [i.get("min_amount") for i in
                      API.GetServiceConfigsPayment(API.getcoinid(fiat_coin[0])).get("data").get("records")
                      if i.get("payment_method") == f'{payment_method[0]}']
        min_amount = sorted(min_amount)[0]

        print(f"{BLUE}用例名称：正确传入参数（vpa账户），能够创建代付交易{RESET}")

        # 创建代付记录
        bill_id = str(ULID())
        adata = API.CreatePayment(bill_id,min_amount,payments_info,
                            f'{API.getcoinid(fiat_coin[0])}',
                            f'{country}',
                            f'{payment_method[0]}',
                            )
        print("创建代付记录", adata)
        assert adata.get("code") == 1000 and adata.get("msg") == 'Success', \
            f'{YELLOW}创建代付交易失败，错误码[{adata.get("code")}]{adata.get("msg")}'

        # 订单id写入文件，其他查询用例依赖
        record_ida = adata.get('data').get("record_id")
        with open(f"{data_path}/record_ids_test.txt", "w", encoding="utf-8") as file:
            file.write(record_ida + " ")
        with open(f"{data_path}/bill_ids_test.txt", "w", encoding="utf-8") as file:
            file.write(bill_id + " ")

        # 查询代付记录
        time.sleep(1)
        Test_api.bill_id = adata.get('data').get("bill_id")
        bdata = API.GetPayment(bill_id=Test_api.bill_id)
        print("查询代付记录", bdata)
        assert bdata.get("code") == 1000 and bdata.get("msg") == 'Success', \
            f'{YELLOW}查询代付交易失败，错误码[{bdata.get("code")}]{bdata.get("msg")}'
        assert bdata.get("data").get("status") in ["Pending"], \
            f'{YELLOW}status不正确:{bdata.get("data").get("status")}'

    # 创建代付记录-cash-NEFT
    @staticmethod
    def test_CreatePayment1():
        # 获取最小代付单金额-NEFT
        min_amount = [i.get("min_amount") for i in
                      API.GetServiceConfigsPayment(API.getcoinid(fiat_coin[0])).get("data").get("records")
                      if i.get("payment_method") == f'{payment_method[1]}']
        min_amount = sorted(min_amount)[0]
        print(f"{BLUE}用例名称：正确传入参数（cash账户），能够创建NEFT代付交易{RESET}")
        # 创建代付记录
        bill_id = str(ULID())
        adata = API.CreatePayment(bill_id,min_amount,payments_info,
                            f'{API.getcoinid(fiat_coin[0])}',
                            f'{country}',
                            f'{payment_method[1]}',
                            )
        print("创建代付记录", adata)
        assert adata.get("code") == 1000 and adata.get("msg") == 'Success', \
            f'{YELLOW}创建代付交易失败，错误码[{adata.get("code")}]{adata.get("msg")}'

        # 订单id写入文件，其他查询用例依赖
        record_ida = adata.get('data').get("record_id")
        with open(f"{data_path}/record_ids_test.txt", "a", encoding="utf-8") as file:
            file.write(record_ida + " ")
        with open(f"{data_path}/bill_ids_test.txt", "a", encoding="utf-8") as file:
            file.write(bill_id + " ")

        # 查询代付记录
        time.sleep(1)
        Test_api.bill_id = adata.get('data').get("bill_id")
        bdata = API.GetPayment(bill_id=Test_api.bill_id)
        print("查询代付记录", bdata)
        assert bdata.get("code") == 1000 and bdata.get("msg") == 'Success', \
            f'{YELLOW}查询代付交易失败，错误码[{bdata.get("code")}]{bdata.get("msg")}'
        assert bdata.get("data").get("status") in ["Pending"], \
            f'{YELLOW}status不正确:{bdata.get("data").get("status")}'

    # 创建代付记录-cash-IMPS
    @staticmethod
    def test_CreatePayment2():
        # 获取最小代付单金额-IMPS
        min_amount = [i.get("min_amount") for i in
                      API.GetServiceConfigsPayment(API.getcoinid(fiat_coin[0])).get("data").get("records")
                      if i.get("payment_method") == f'{payment_method[2]}']
        min_amount = sorted(min_amount)[0]
        print(f"{BLUE}用例名称：正确传入参数（cash账户），能够创建IMPS代付交易{RESET}")
        # 创建代付记录
        bill_id = str(ULID())
        adata = API.CreatePayment(bill_id,min_amount,payments_info,
                            f'{API.getcoinid(fiat_coin[0])}',
                            f'{country}',
                            f'{payment_method[2]}',
                            )
        print("创建代付记录", adata)
        assert adata.get("code") == 1000 and adata.get("msg") == 'Success', \
            f'{YELLOW}创建代付交易失败，错误码[{adata.get("code")}]{adata.get("msg")}'

        # 订单id写入文件，其他查询用例依赖
        record_ida = adata.get('data').get("record_id")
        with open(f"{data_path}/record_ids_test.txt", "a", encoding="utf-8") as file:
            file.write(record_ida + " ")
        with open(f"{data_path}/bill_ids_test.txt", "a", encoding="utf-8") as file:
            file.write(bill_id + " ")

        # 查询代付记录
        time.sleep(1)
        Test_api.bill_id = adata.get('data').get("bill_id")
        bdata = API.GetPayment(bill_id=Test_api.bill_id)
        print("查询代付记录", bdata)
        assert bdata.get("code") == 1000 and bdata.get("msg") == 'Success', \
            f'{YELLOW}查询代付交易失败，错误码[{bdata.get("code")}]{bdata.get("msg")}'
        assert bdata.get("data").get("status") in ["Pending"], \
            f'{YELLOW}status不正确:{bdata.get("data").get("status")}'

    # 查询代付记录-bill_id-upi
    @staticmethod
    def test_GetPayment():
        # 获取最小代付单金额
        min_amount = [i.get("min_amount") for i in
                      API.GetServiceConfigsPayment(API.getcoinid(fiat_coin[0])).get("data").get("records")
                      if i.get("payment_method") == f'{payment_method[0]}']
        min_amount = sorted(min_amount)[0]
        print(f"{BLUE}用例名称：正确传入参数bill_id，能够查询代付记录{RESET}")
        # 创建代付记录
        bill_id = str(ULID())
        adata = API.CreatePayment(bill_id,min_amount,payments_info,
                            f'{API.getcoinid(fiat_coin[0])}',
                            f'{country}',
                            f'{payment_method[1]}',
                            )
        print("创建代付记录", adata)
        assert adata.get("code") == 1000 and adata.get("msg") == 'Success', \
            f'{YELLOW}创建代付交易失败，错误码[{adata.get("code")}]{adata.get("msg")}'
        # 查询代付记录
        Test_api.bill_id = adata.get('data').get("bill_id")
        bdata = API.GetPayment(bill_id=Test_api.bill_id)
        print("查询代付记录", bdata)
        assert bdata.get("code") == 1000 and bdata.get("msg") == 'Success', \
            f'{YELLOW}查询代付交易失败，错误码[{bdata.get("code")}]{bdata.get("msg")}'

    # 查询代付记录-record_id-upi
    @staticmethod
    def test_GetPayment1():
        # 获取最小代付单金额
        min_amount = [i.get("min_amount") for i in
                      API.GetServiceConfigsPayment(API.getcoinid(fiat_coin[0])).get("data").get("records")
                      if i.get("payment_method") == f'{payment_method[0]}']
        min_amount = sorted(min_amount)[0]
        print(f"{BLUE}用例名称：正确传入参数record_id，能够查询代付记录{RESET}")
        # 创建代付记录
        bill_id = str(ULID())
        adata = API.CreatePayment(bill_id,min_amount,payments_info,
                            f'{API.getcoinid(fiat_coin[0])}',
                            f'{country}',
                            f'{payment_method[1]}',
                            )
        print("创建代付记录", adata)
        assert adata.get("code") == 1000 and adata.get("msg") == 'Success', \
            f'{YELLOW}创建代付交易失败，错误码[{adata.get("code")}]{adata.get("msg")}'
        # 查询代付记录
        Test_api.record_id = adata.get('data').get("record_id")
        bdata = API.GetPayment(record_id=Test_api.record_id)
        print("查询代付记录", bdata)
        assert bdata.get("code") == 1000 and bdata.get("msg") == 'Success', \
            f'{YELLOW}查询代付交易失败，错误码[{bdata.get("code")}]{bdata.get("msg")}'

    # 查询代付列表-record_ids-upi-NEFT-IMPS
    @staticmethod
    def test_GetPaymentList():
        print(f"{BLUE}用例名称：正确传入参数record_ids，能够查询代付记录列表{RESET}")
        # 查询代付记录列表
        # 获取record_ids文件内容
        with open(f"{data_path}/record_ids_test.txt", encoding="utf-8") as file:
            record_ids = file.read().split()
        adata = API.GetPaymentList(record_ids=record_ids)
        print("查询代付记录列表", adata)
        assert adata.get("code") == 1000 and adata.get("msg") == 'Success', \
            f'{YELLOW}查询代付记录列表失败，错误码[{adata.get("code")}]{adata.get("msg")}'
        assert len(adata.get("data").get('records')) == 3, \
            f'{YELLOW}查询结果订单数量不准确:{adata.get("data").get('records')}'

    # 查询代付列表-bill_ids-upi-NEFT-IMPS
    @staticmethod
    def test_GetPaymentList1():
        print(f"{BLUE}用例名称：正确传入参数bill_ids，能够查询代付记录列表{RESET}")
        # 查询代付记录列表
        # 获取bill_ids文件内容
        with open(f"{data_path}/bill_ids_test.txt", encoding="utf-8") as file:
            bill_ids = file.read().split()
        adata = API.GetPaymentList(bill_ids=bill_ids)
        print("查询代付记录列表", adata)
        assert adata.get("code") == 1000 and adata.get("msg") == 'Success', \
            f'{YELLOW}查询代付记录列表失败，错误码[{adata.get("code")}]{adata.get("msg")}'
        assert len(adata.get("data").get('records')) == 3, \
            f'{YELLOW}查询结果订单数量不准确:{adata.get("data").get('records')}'

    # 查询代付列表-time
    @staticmethod
    def test_GetPaymentList2():
        print(f"{BLUE}用例名称：传入当前时间往前推三个月时间戳，能够查询代付记录列表{RESET}")
        # 查询代付记录列表
        adata = API.GetPaymentList(int(str(time.time() - 89 * 24 * 3600).split(".")[0]),
                                   int(str(time.time()).split(".")[0]))
        print("查询代付记录列表", adata)
        assert adata.get("code") == 1000 and adata.get("msg") == 'Success', \
            f'{YELLOW}查询代付记录列表失败，错误码[{adata.get("code")}]{adata.get("msg")}'
        assert len(adata.get("data").get('records')) > 4, \
            f'{YELLOW}查询结果订单数量不准确:{adata.get("data").get('records')}'






    # 确认代收交易-upi
    @staticmethod
    def test_ConfirmReceipt():

        # 获取最小代收单金额
        min_amount = API.GetServiceConfigsReceipt(API.getcoinid(fiat_coin[0])).get("data").get("record").get(
            "min_amount")
        print(f"{BLUE}用例名称：正确传入参数，能够创建代收单{RESET}")

        # 创建代收记录
        bill_id = str(ULID())
        if is_buyer_kyc:
            adata = API.CreateReceipt(
                f'{bill_id}',
                f'{min_amount}',
                f'{API.getcoinid(fiat_coin[0])}',
                f'{country}',
                is_buyer_kyc,
                f'{buyer_name}',
                f'{buyer_vpa}',
            )
        else:
            adata = API.CreateReceipt(
                f'{bill_id}',
                f'{min_amount}',
                f'{API.getcoinid(fiat_coin[0])}',
                f'{country}',
                is_buyer_kyc,
                f'{buyer_name}',
                f'{buyer_vpa}',
                f'{buyer_email}',
                f'{buyer_phone}'
            )
        print("创建代收记录", adata)

        # 订单id写入文件，其他查询用例依赖
        record_ida = adata.get('data').get("record_id")
        with open(f"{data_path}/record_ids_test.txt", "a", encoding="utf-8") as file:
            file.write(record_ida + " ")
        with open(f"{data_path}/bill_ids_test.txt", "a", encoding="utf-8") as file:
            file.write(bill_id + " ")

        assert adata.get("code") == 1000 and adata.get("msg") == 'Success', \
            f'{YELLOW}创建代收交易失败，错误码[{adata.get("code")}]{adata.get("msg")}'

        # 确认代收记录
        bdata = API.ConfirmReceipt(bill_id=bill_id, pay_proof_id=random_12num())
        print("确认代收记录", bdata)

        assert bdata.get("code") == 1000 and bdata.get("msg") == 'Success' and bdata.get("data") != [], \
            f'{YELLOW}确认代收交易失败，错误码[{bdata.get("code")}]{bdata.get("msg")}'
        assert bdata.get("data").get("status") == 'Confirming', \
            f'{YELLOW}status不正确,确认后:{bdata.get("data").get("status")}'

        # 查询代收记录
        Test_api.bill_id = adata.get('data').get("bill_id")
        cdata = API.GetReceipt(bill_id=Test_api.bill_id)
        print("查询代收记录", cdata)

        assert cdata.get("code") == 1000 and cdata.get("msg") == 'Success' and cdata.get("data") != [], \
            f'{YELLOW}查询代收交易失败，错误码[{cdata.get("code")}]{cdata.get("msg")}'

    # 创建代收交易-upi-使用企业KYC
    @staticmethod
    def test_CreateReceipt():

        # 获取最小代收单金额
        min_amount = API.GetServiceConfigsReceipt(API.getcoinid(fiat_coin[0])).get("data").get("record").get("min_amount")
        print(f"{BLUE}用例名称：正确传入参数，能够创建代收单{RESET}")

        # 创建代收记录
        bill_id = str(ULID())
        if is_buyer_kyc:
            adata = API.CreateReceipt(
                f'{bill_id}',
                f'{min_amount}',
                f'{API.getcoinid(fiat_coin[0])}',
                f'{country}',
                is_buyer_kyc,
                f'{buyer_name}',
                f'{buyer_vpa}',
            )
        else:
            adata = API.CreateReceipt(
                f'{bill_id}',
                f'{min_amount}',
                f'{API.getcoinid(fiat_coin[0])}',
                f'{country}',
                is_buyer_kyc,
                f'{buyer_name}',
                f'{buyer_vpa}',
                f'{buyer_email}',
                f'{buyer_phone}'
            )
        print("创建代收记录", adata)

        # 订单id写入文件，其他查询用例依赖
        record_ida = adata.get('data').get("record_id")
        with open(f"{data_path}/record_ids_test.txt", "a", encoding="utf-8") as file:
            file.write(record_ida + " ")
        with open(f"{data_path}/bill_ids_test.txt", "a", encoding="utf-8") as file:
            file.write(bill_id + " ")

        assert adata.get("code") == 1000 and adata.get("msg") == 'Success', \
            f'{YELLOW}创建代收交易失败，错误码[{adata.get("code")}]{adata.get("msg")}{RESET}'

        # 查询代收记录
        Test_api.bill_id = adata.get('data').get("bill_id")
        bdata = API.GetReceipt(bill_id=Test_api.bill_id)
        print("查询代收记录", bdata)

        assert bdata.get("code") == 1000 and bdata.get("msg") == 'Success' and bdata.get("data") != [], \
            f'{YELLOW}查询代收交易失败，错误码[{bdata.get("code")}]{bdata.get("msg")}{RESET}'
        assert adata.get("data").get("status") == bdata.get("data").get("status"), \
            f'{YELLOW}status不一致,创建:{adata.get("data").get("state")}和查询:{bdata.get("data").get("status")}{RESET}'
        assert adata.get("data").get("status") in ["Pending"] and bdata.get("data").get("status") in ["Pending"], \
            f'{YELLOW}status不对,创建:{adata.get("data").get("state")}和查询:{bdata.get("data").get("status")}{RESET}'

    # 创建收银台-upi
    @staticmethod
    def test_Checkout():

        # 获取最小代收单金额
        min_amount = API.GetServiceConfigsReceipt(API.getcoinid(fiat_coin[0])).get("data").get("record").get("min_amount")
        print(f"{BLUE}用例名称：正确传入参数，能够创建收银台代收交易{RESET}")

        # 创建收银台
        bill_id = str(ULID())
        if is_buyer_kyc:
            adata = API.Checkout(
                f'{bill_id}',
                f'{min_amount}',
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

        # 订单id写入文件，其他查询用例依赖
        record_ida = adata.get('data').get("record_id")
        with open(f"{data_path}/record_ids_test.txt", "a", encoding="utf-8") as file:
            file.write(record_ida + " ")
        with open(f"{data_path}/bill_ids_test.txt", "a", encoding="utf-8") as file:
            file.write(bill_id + " ")

        assert adata.get("code") == 1000 and adata.get("msg") == 'Success', \
            f'{YELLOW}创建收银台代收交易失败，错误码[{adata.get("code")}]{adata.get("msg")}'

        checkout_url = adata.get('data').get('checkout_url')
        url_status_code = send_request(checkout_url, 'get', )[0].status_code

        assert url_status_code == 200, f'{YELLOW}生成收银台链接访问失败，状态码[{url_status_code}]，链接[{url}]'

        # 查询代收记录
        Test_api.bill_id = adata.get('data').get("bill_id")
        bdata = API.GetReceipt(bill_id=Test_api.bill_id)
        print("查询代收记录", bdata)

        assert bdata.get("code") == 1000 and bdata.get("msg") == 'Success' and bdata.get("data") != [], \
            f'{YELLOW}查询代收交易失败，错误码[{bdata.get("code")}]{bdata.get("msg")}'

        assert bdata.get("data").get("status") in ["Pending"], \
            f'{YELLOW}status不正确:{bdata.get("data").get("status")}'

    # 获取银行码列表
    @staticmethod
    def test_GetBankList():
        print(f"{BLUE}用例名称：调用接口，获取银行码列表成功{RESET}")
        # 获取银行码列表
        adata = API.GetBankList("ICICI Bank")
        print("获取银行码列表", adata)
        assert adata.get("code") == 1000 and adata.get("msg") == 'Success', \
            f'{YELLOW}获取银行码列表失败，错误码[{adata.get("code")}]{adata.get("msg")}'
        assert len(adata.get("data").get('records')) > 0, \
            f'{YELLOW}获取银行码列表数量不对，未查到'

    # 获取收款单配置-INR
    @staticmethod
    def test_GetServiceConfigsReceipt():
        print(f"{BLUE}用例名称：传入正确参数，获取收款单配置成功{RESET}")
        # 获取收款单配置
        adata = API.GetServiceConfigsReceipt(f"{API.getcoinid(fiat_coin[0])}")
        print("获取收款单配置", adata)
        assert adata.get("code") == 1000 and adata.get("msg") == 'Success', \
            f'{YELLOW}获取收款单配置失败，错误码[{adata.get("code")}]{adata.get("msg")}'
        assert len(adata.get("data").get('record')) > 1, \
            f'{YELLOW}获取收款单配置数量不对，至少存在一种货币代收配置'

    # 获取付款单配置-INR
    @staticmethod
    def test_GetServiceConfigsPayment():
        print(f"{BLUE}用例名称：传入正确参数，获取付款单配置成功{RESET}")
        # 获取付款单配置
        adata = API.GetServiceConfigsPayment(f"{API.getcoinid(fiat_coin[0])}")
        print("获取付款单配置", adata)
        assert adata.get("code") == 1000 and adata.get("msg") == 'Success', \
            f'{YELLOW}获取付款单配置失败，错误码[{adata.get("code")}]{adata.get("msg")}'
        assert len(adata.get("data").get('records')) > 1, \
            f'{YELLOW}获取付款单配置数量不对，至少存在一种货币代付钱配置'


