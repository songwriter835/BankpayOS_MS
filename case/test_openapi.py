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

class Test_api:

    # 创建代收交易-upi
    @staticmethod
    def test_CreateReceipt():

        # 获取最小代收单金额
        min_amount = [i.get("min_amount") for i in
                      API.GetServiceConfigsReceipt(API.getcoinid(fiat_coin[0])).get("data").get("records")
                      if i.get("payment_method") == f'{payment_method[0]}']
        min_amount = sorted(min_amount)[0]

        print(f"{BLUE}用例名称：正确传入参数，能够创建代收单{RESET}")

        # 创建代收记录
        bill_id = str(ULID())
        adata = API.CreateReceipt(bill_id,
                                  min_amount,
                                  f'{country}',
                                  f'{API.getcoinid(fiat_coin[0])}',
                                  f'{payment_method[0]}')
        print("创建代收记录", adata)

        # 订单id写入文件，其他查询用例依赖
        record_ida = adata.get('data').get("record_id")
        with open(f"{data_path}/record_ids_test.txt", "w", encoding="utf-8") as file:
            file.write(record_ida + " ")
        with open(f"{data_path}/bill_ids_test.txt", "w", encoding="utf-8") as file:
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

    # 创建代收交易-upi-bank
    @staticmethod
    def test_CreateReceipt1():

        # 获取最大代收单金额
        max_amount = [i.get("max_amount") for i in
                      API.GetServiceConfigsReceipt(API.getcoinid(fiat_coin[0])).get("data").get("records")
                      if i.get("payment_method") == f'{payment_method[0]}']
        max_amount = sorted(max_amount)[0]

        print(f"{BLUE}用例名称：正确传入参数，能够创建代收单-bank接单{RESET}")

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

        # 查询代收记录
        Test_api.bill_id = adata.get('data').get("bill_id")
        bdata = API.GetReceipt(bill_id=Test_api.bill_id)
        print("查询代收记录", bdata)

        assert bdata.get("code") == 1000 and bdata.get("msg") == 'Success' and bdata.get("data") != [],\
            f'{YELLOW}查询代收交易失败，错误码[{bdata.get("code")}]{bdata.get("msg")}'

        assert adata.get("data").get("status") == bdata.get("data").get("status"), \
            f'{YELLOW}status不一致,创建:{adata.get("data").get("state")}和查询:{bdata.get("data").get("status")}'

    # 确认代收交易-upi
    @staticmethod
    def test_ConfirmReceipt():

        # 获取最小代收单金额
        min_amount = [i.get("min_amount") for i in
                      API.GetServiceConfigsReceipt(API.getcoinid(fiat_coin[0])).get("data").get("records")
                      if i.get("payment_method") == f'{payment_method[0]}']
        min_amount = sorted(min_amount)[0]

        print(f"{BLUE}用例名称：正确传入参数，能够确认代收交易{RESET}")

        # 创建代收记录
        bill_id = str(ULID())
        adata = API.CreateReceipt(bill_id,
                                  min_amount,
                                  f'{country}',
                                  f'{API.getcoinid(fiat_coin[0])}',
                                  f'{payment_method[0]}')
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

    # 确认代收交易-upi-bank
    # 需要保证脚本测试商户配置，bank最大接单金额大于cashier，不然会导致cashier把bank单子接走，用例失败
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
            water = DB().select_table("select utr_id,amount from `bankpayos-db-bank`.message order by id desc limit 1;")
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

    # 创建收银台-upi
    @staticmethod
    def test_Checkout():

        # 获取最小代收单金额
        min_amount = [i.get("min_amount") for i in
                      API.GetServiceConfigsReceipt(API.getcoinid(fiat_coin[0])).get("data").get("records")
                      if i.get("payment_method") == f'{payment_method[0]}']
        min_amount = sorted(min_amount)[0]

        print(f"{BLUE}用例名称：正确传入参数，能够创建收银台代收交易{RESET}")

        # 创建收银台
        bill_id = str(ULID())
        adata = API.Checkout(bill_id,
                             min_amount,
                             f"{API.getcoinid(fiat_coin[0])}",
                             f'{country}',
                             f'{payment_method[0]}')
        print("创建收银台", adata)

        assert adata.get("code") == 1000 and adata.get("msg") == 'Success', \
            f'{YELLOW}创建收银台代收交易失败，错误码[{adata.get("code")}]{adata.get("msg")}'

        url = adata.get('data').get('checkout_url')
        url_status_code = send_request(url, 'get', )[0].status_code

        assert url_status_code == 200, f'{YELLOW}生成收银台链接访问失败，状态码[{url_status_code}]，链接[{url}]'

        # 查询代收记录
        Test_api.bill_id = adata.get('data').get("bill_id")
        bdata = API.GetReceipt(bill_id=Test_api.bill_id)
        print("查询代收记录", bdata)

        assert bdata.get("code") == 1000 and bdata.get("msg") == 'Success' and bdata.get("data") != [], \
            f'{YELLOW}查询代收交易失败，错误码[{bdata.get("code")}]{bdata.get("msg")}'

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

    # 查询现金资产余额-INR
    @staticmethod
    def test_GetBalance():
        print(f"{BLUE}用例名称：传入正确参数，能够查询INR资产余额{RESET}")
        # 查询现金资产余额
        adata = API.GetBalance(API.getcoinid(fiat_coin[0]))
        print("查询现金资产余额", adata)
        assert adata.get("code") == 1000 and adata.get("msg") == 'Success', \
            f'{YELLOW}查询现金资产余额，错误码[{adata.get("code")}]{adata.get("msg")}'
        assert 'assets' in adata.get("data"), \
            f'{YELLOW}查询结果不准确:{adata.get("data").get('assets')}'

    # 查询现金资产余额-USDT
    @staticmethod
    def test_GetBalance1():
        print(f"{BLUE}用例名称：传入正确参数，能够查询USDT资产余额{RESET}")
        # 查询现金资产余额
        adata = API.GetBalance(API.getcoinid(token_coin[0]))
        print("查询现金资产余额", adata)
        assert adata.get("code") == 1000 and adata.get("msg") == 'Success', \
            f'{YELLOW}查询现金资产余额，错误码[{adata.get("code")}]{adata.get("msg")}'
        assert 'assets' in adata.get("data"), \
            f'{YELLOW}查询结果不准确:{adata.get("data").get('assets')}'

    # 法币换代币
    @staticmethod
    def test_CurrencyToCrypto():
        print(f"{BLUE}用例名称：传入正确参数，法币换代币换币成功{RESET}")
        # 查询现金资产余额
        adata = API.GetBalance(API.getcoinid(fiat_coin[0]))
        print("查询现金资产余额", adata)
        assert adata.get("code") == 1000 and adata.get("msg") == 'Success', \
            f'{YELLOW}查询现金资产余额失败，错误码[{adata.get("code")}]{adata.get("msg")}'
        coin_amount = adata.get("data").get("assets")[0].get("balance")
        # 法币换代币
        bdata = API.CurrencyToCrypto(f'{API.getcoinid(fiat_coin[0])}',
                                     f'{API.getcoinid(token_coin[0])}',
                                     '100',
                                     '0')
        print("法币换代币", bdata)
        assert bdata.get("code") == 1000 and bdata.get("msg") == 'Success', \
            f'{YELLOW}代币换法币失败，错误码[{bdata.get("code")}]{bdata.get("msg")}'
        coin_amount = round(float(coin_amount) - float('100'), 4)

        # 订单id写入文件，其他查询用例依赖
        record_ida = bdata.get('data').get("record_id")
        with open(f"{data_path}/record_ids_test.txt", "w", encoding="utf-8") as file:
            file.write(record_ida + " ")

        # 查询现金资产余额
        cdata = API.GetBalance(API.getcoinid(fiat_coin[0]))
        print("查询现金资产余额", cdata)
        assert cdata.get("code") == 1000 and cdata.get("msg") == 'Success', \
            f'{YELLOW}查询现金资产余额失败，错误码[{cdata.get("code")}]{cdata.get("msg")}'
        assert coin_amount == round(float(cdata.get("data").get("assets")[0].get("balance")), 4), \
            f"{YELLOW}换币后余额不正确"

    # 代币换法币
    @staticmethod
    def test_CryptoToCurrency():
        print(f"{BLUE}用例名称：传入正确参数，代币换法币换币成功{RESET}")
        # 查询现金资产余额
        adata = API.GetBalance(API.getcoinid(token_coin[0]))
        print("查询USDT资产余额", adata)
        assert adata.get("code") == 1000 and adata.get("msg") == 'Success', \
            f'{YELLOW}查询USDT资产余额失败，错误码[{adata.get("code")}]{adata.get("msg")}'
        coin_amount = adata.get("data").get("assets")[0].get("balance")
        # 代币换法币
        bdata = API.CryptoToCurrency(f'{API.getcoinid(token_coin[0])}',
                                     f'{API.getcoinid(fiat_coin[0])}',
                                     '0.1',
                                     '0')
        print("代币换法币", bdata)
        assert bdata.get("code") == 1000 and bdata.get("msg") == 'Success', \
            f'{YELLOW}代币换法币失败，错误码[{bdata.get("code")}]{bdata.get("msg")}'
        coin_amount = round(float(coin_amount) - float('0.1'), 4)

        # 订单id写入文件，其他查询用例依赖
        record_ida = bdata.get('data').get("record_id")
        with open(f"{data_path}/record_ids_test.txt", "a", encoding="utf-8") as file:
            file.write(record_ida + " ")

        # 查询现金资产余额
        cdata = API.GetBalance("5ddeeacb13244b0cb772e4af9830f0bf")
        print("查询USDT资产余额", cdata)
        assert cdata.get("code") == 1000 and cdata.get("msg") == 'Success', \
            f'{YELLOW}查询USDT资产余额失败，错误码[{cdata.get("code")}]{cdata.get("msg")}'
        assert coin_amount == round(float(cdata.get("data").get("assets")[0].get("balance")), 4), \
            f"{YELLOW}换币后余额不正确"

    # 获取换币记录-record_id
    @staticmethod
    def test_GetSwap():
        print(f"{BLUE}用例名称：传入正确参数，获取换币记录成功{RESET}")
        # 获取record_ids文件内容
        with open(f"{data_path}/record_ids_test.txt", encoding="utf-8") as file:
            record_ids = file.read().split()
        # 获取换币记录
        adata = API.GetSwap(record_ids[0])
        print("查询现金资产余额", adata)
        assert adata.get("code") == 1000 and adata.get("msg") == 'Success', \
            f'{YELLOW}获取换币记录失败，错误码[{adata.get("code")}]{adata.get("msg")}'
        assert len(adata.get("data")) > 0,\
            f'{YELLOW}获取换币记录失败，未查找到订单'

    # 获取换币记录列表-record_ids
    @staticmethod
    def test_GetSwapList():
        print(f"{BLUE}用例名称：正确传入参数record_ids，获取换币记录列表成功{RESET}")
        # 获取record_ids文件内容
        with open(f"{data_path}/record_ids_test.txt", encoding="utf-8") as file:
            record_ids = file.read().split()
        # 获取换币记录列表
        adata = API.GetSwapList(record_ids)
        print("获取换币记录列表", adata)
        assert adata.get("code") == 1000 and adata.get("msg") == 'Success', \
            f'{YELLOW}获取换币记录列表失败，错误码[{adata.get("code")}]{adata.get("msg")}'
        assert len(adata.get("data").get("records")) == 2,\
            f'{YELLOW}获取换币记录列表失败，查找到的订单数量不对'

    # 获取换币记录列表-time
    @staticmethod
    def test_GetSwapList1():
        print(f"{BLUE}用例名称：传入当前时间往前推三个月时间戳，获取换币记录列表成功{RESET}")
        # 获取换币记录列表
        adata = API.GetSwapList(start_at=int(str(time.time() - 89 * 24 * 3600).split(".")[0]),
                                end_at=int(str(time.time()).split(".")[0]))
        print("获取换币记录列表", adata)
        assert adata.get("code") == 1000 and adata.get("msg") == 'Success', \
            f'{YELLOW}获取换币记录列表失败，错误码[{adata.get("code")}]{adata.get("msg")}'
        assert len(adata.get("data").get('records')) > 2, \
            f'{YELLOW}获取换币记录列表失败，查找到的订单数量不对'

    # 查询充值记录
    @staticmethod
    def test_GetDeposit():
        print(f"{BLUE}用例名称：传入正确参数，查询充值记录成功{RESET}")
        # 查询充值记录
        adata = API.GetDeposit('DP2025042703445688492079289733120')
        print("查询充值记录", adata)
        assert adata.get("code") == 1000 and adata.get("msg") == 'Success', \
            f'{YELLOW}查询充值记录失败，错误码[{adata.get("code")}]{adata.get("msg")}'
        assert len(adata.get("data")) > 0, \
            f'{YELLOW}查询充值记录失败，未查找到订单'

    # 查询充值列表-record_ids
    @staticmethod
    def test_GetDepositList():
        print(f"{BLUE}用例名称：正确传入参数record_ids，查询充值列表成功{RESET}")
        # 查询充值列表
        adata = API.GetDepositList(['DP2025042703445688492079289733120',
                                    'DP2025042206312886722047366926336',
                                    'DP2025042206292286721519757037568'])
        print("查询充值列表", adata)
        assert adata.get("code") == 1000 and adata.get("msg") == 'Success', \
            f'{YELLOW}查询充值列表失败，错误码[{adata.get("code")}]{adata.get("msg")}'
        assert len(adata.get("data").get("records")) == 3, \
            f'{YELLOW}查询充值列表失败，查找到的订单数量不对'

    # 查询充值列表-time
    @staticmethod
    def test_GetDepositList1():
        print(f"{BLUE}用例名称：传入当前时间往前推三个月时间戳，查询充值列表成功{RESET}")
        # 查询充值列表
        adata = API.GetDepositList(start_at=int(str(time.time() - 89 * 24 * 3600).split(".")[0]),
                                   end_at=int(str(time.time()).split(".")[0]))
        print("查询充值列表", adata)
        assert adata.get("code") == 1000 and adata.get("msg") == 'Success', \
            f'{YELLOW}查询充值列表失败，错误码[{adata.get("code")}]{adata.get("msg")}'
        assert len(adata.get("data").get("records")) > 3, \
            f'{YELLOW}查询充值列表失败，查找到的订单数量不对(除非三个月内没有充值订单)'

    # 代币提现
    @staticmethod
    def test_ApplyCryptoWithdraw():

        print(f"{BLUE}用例名称：正确传入参数，创建代币提现订单成功{RESET}")
        # 代币提现
        bill_id = str(ULID())
        adata = API.ApplyCryptoWithdraw(bill_id,
                                        f'{API.getcoinid(token_coin[0])}',
                                        '0.1',
                                        f'{Withdraw_addr}',
                                        'POLYGON',
                                        )
        print("代币提现", adata)
        assert adata.get("code") == 1000 and adata.get("msg") == 'Success', \
            f'{YELLOW}创建代币提现订单失败，错误码[{adata.get("code")}]{adata.get("msg")}'

        # 订单id写入文件，其他查询用例依赖
        record_ida = adata.get('data').get("record_id")
        with open(f"{data_path}/record_ids_test.txt", "w", encoding="utf-8") as file:
            file.write(record_ida + " ")
        with open(f"{data_path}/bill_ids_test.txt", "w", encoding="utf-8") as file:
            file.write(bill_id + " ")

        # 查询提现记录
        Test_api.bill_id = adata.get('data').get("bill_id")
        bdata = API.GetWithdraw(bill_id=Test_api.bill_id)
        print("查询提现记录", bdata)
        assert bdata.get("code") == 1000 and bdata.get("msg") == 'Success', \
            f'{YELLOW}查询提现记录失败，错误码[{bdata.get("code")}]{bdata.get("msg")}'
        assert len(bdata.get("data")) > 0, \
            f'{YELLOW}查询提现记录失败，未查到订单'

    # 查询提现记录-record_id
    @staticmethod
    def test_GetWithdraw():
        print(f"{BLUE}用例名称：正确传入record_id，查询提现记录成功{RESET}")
        # 代币提现
        bill_id = str(ULID())
        adata = API.ApplyCryptoWithdraw(bill_id,
                                        f'{API.getcoinid(token_coin[0])}',
                                        '0.1',
                                        f'{Withdraw_addr}',
                                        'POLYGON',
                                        )
        print("代币提现", adata)
        assert adata.get("code") == 1000 and adata.get("msg") == 'Success', \
            f'{YELLOW}创建代币提现订单失败，错误码[{adata.get("code")}]{adata.get("msg")}'

        # 订单id写入文件，其他查询用例依赖
        record_ida = adata.get('data').get("record_id")
        with open(f"{data_path}/record_ids_test.txt", "a", encoding="utf-8") as file:
            file.write(record_ida + " ")
        with open(f"{data_path}/bill_ids_test.txt", "a", encoding="utf-8") as file:
            file.write(bill_id + " ")

        # 查询提现记录
        bdata = API.GetWithdraw(record_id=adata.get("data").get("record_id"))
        print("查询提现记录", adata)
        assert bdata.get("code") == 1000 and bdata.get("msg") == 'Success', \
            f'{YELLOW}查询提现记录失败，错误码[{bdata.get("code")}]{bdata.get("msg")}'
        assert len(bdata.get("data")) > 0, \
            f'{YELLOW}查询提现记录失败，未查到订单'

    # 查询提现记录-bill_id
    @staticmethod
    def test_GetWithdraw1():
        print(f"{BLUE}用例名称：正确传入bill_id，查询提现记录成功{RESET}")
        # 代币提现
        bill_id = str(ULID())
        adata = API.ApplyCryptoWithdraw(bill_id,
                                        f'{API.getcoinid(token_coin[0])}',
                                        '0.1',
                                        f'{Withdraw_addr}',
                                        'POLYGON',
                                        )
        print("代币提现", adata)
        assert adata.get("code") == 1000 and adata.get("msg") == 'Success', \
            f'{YELLOW}创建代币提现订单失败，错误码[{adata.get("code")}]{adata.get("msg")}'

        # 订单id写入文件，其他查询用例依赖
        record_ida = adata.get('data').get("record_id")
        with open(f"{data_path}/record_ids_test.txt", "a", encoding="utf-8") as file:
            file.write(record_ida + " ")
        with open(f"{data_path}/bill_ids_test.txt", "a", encoding="utf-8") as file:
            file.write(bill_id + " ")

        # 查询提现记录
        bdata = API.GetWithdraw(bill_id=adata.get("data").get("bill_id"))
        print("查询提现记录", adata)
        assert bdata.get("code") == 1000 and bdata.get("msg") == 'Success', \
            f'{YELLOW}查询提现记录失败，错误码[{bdata.get("code")}]{bdata.get("msg")}'
        assert len(bdata.get("data")) > 0, \
            f'{YELLOW}查询提现记录失败，未查到订单'

    # 查询提现列表-record_ids
    @staticmethod
    def test_GetWithdrawList():
        print(f"{BLUE}用例名称：正确传入record_ids，查询提现列表成功{RESET}")
        # 获取record_ids文件内容
        with open(f"{data_path}/record_ids_test.txt", encoding="utf-8") as file:
            record_ids = file.read().split()
        # 查询提现记录
        adata = API.GetWithdrawList(record_ids=record_ids)
        print("查询提现记录列表", adata)
        assert adata.get("code") == 1000 and adata.get("msg") == 'Success', \
            f'{YELLOW}查询提现列表失败，错误码[{adata.get("code")}]{adata.get("msg")}'
        assert len(adata.get("data").get('records')) == 3, \
            f'{YELLOW}查询提现记录数量不对，未查到订单'

    # 查询提现列表-bill_ids
    @staticmethod
    def test_GetWithdrawList1():
        print(f"{BLUE}用例名称：正确传入bill_ids，查询提现列表成功{RESET}")
        # 查询代付记录列表
        # 获取bill_ids文件内容
        with open(f"{data_path}/bill_ids_test.txt", encoding="utf-8") as file:
            bill_ids = file.read().split()
        # 查询提现记录
        adata = API.GetWithdrawList(bill_ids=bill_ids)
        print("查询提现记录列表", adata)
        assert adata.get("code") == 1000 and adata.get("msg") == 'Success', \
            f'{YELLOW}查询提现列表失败，错误码[{adata.get("code")}]{adata.get("msg")}'
        assert len(adata.get("data").get('records')) == 3, \
            f'{YELLOW}查询提现记录数量不对，未查到订单'

    # 查询提现列表-time
    @staticmethod
    def test_GetWithdrawList2():
        print(f"{BLUE}用例名称：传入当前时间往前推三个月时间戳，查询提现列表成功{RESET}")
        # 查询提现记录
        adata = API.GetWithdrawList(start_at=int(str(time.time() - 89 * 24 * 3600).split(".")[0]),
                                    end_at=int(str(time.time()).split(".")[0]))
        print("查询提现记录列表", adata)
        assert adata.get("code") == 1000 and adata.get("msg") == 'Success', \
            f'{YELLOW}查询提现列表失败，错误码[{adata.get("code")}]{adata.get("msg")}'
        assert len(adata.get("data").get('records')) > 2, \
            f'{YELLOW}查询提现记录数量不对，未查到订单'

    # 获取银行码列表
    @staticmethod
    def test_GetBankList():
        print(f"{BLUE}用例名称：调用接口，获取银行码列表成功{RESET}")
        # 获取银行码列表
        adata = API.GetBankList()
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
        assert len(adata.get("data").get('records')) > 1, \
            f'{YELLOW}获取收款单配置数量不对，至少存在两种支付方式配置'

    # 获取付款单配置-INR
    @staticmethod
    def test_GetServiceConfigsPayment():
        print(f"{BLUE}用例名称：传入正确参数，获取付款单配置成功{RESET}")
        # 获取付款单配置
        adata = API.GetServiceConfigsPayment(f"{API.getcoinid(fiat_coin[0])}")
        print("获取付款单配置", adata)
        assert adata.get("code") == 1000 and adata.get("msg") == 'Success', \
            f'{YELLOW}获取付款单配置失败，错误码[{adata.get("code")}]{adata.get("msg")}'
        assert len(adata.get("data").get('records')) > 0, \
            f'{YELLOW}获取付款单配置数量不对，至少存在一种支付方式配置'
