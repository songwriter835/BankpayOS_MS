from pprint import pprint
import pytest
from ulid import ULID
from BankpayOS_MS.common.api  import OpenApi
from BankpayOS_MS.common.utils import send_request, random_12num

API = OpenApi()
bill_id = str(ULID())

""" 代收 """

######################## 创建
# adata = API.CreateReceipt(bill_id, "10000",'IND',
#                                     '1902225p16qojepfbsfcmo8app61wyhh','upi')

# pprint(adata)

######################### 确认
# bdata = API.ConfirmReceipt(bill_id=adata.get('data').get("bill_id"),pay_proof_id=random_12num())
# pprint(bdata)

######################### 取消
# cdata = API.CancelReceipt(bill_id=adata.get('data').get("bill_id"))
# pprint(cdata)

######################## 查询代收记录
# adata = API.GetReceipt('RC2025012003002353329245023244288', bill_id='01JHFBANWT5VXB0RPC6WRT3ZVW')
# pprint(adata)

######################### 查询代收记录列表

# # 时间筛选
# adata = API.GetReceiptList(int(str(time.time() - 89 * 24 * 3600).split(".")[0]),
#                            int(str(time.time()).split(".")[0]))
# 订单列表筛选
# adata = API.GetReceiptList(bill_ids = ['01JH4V46R57DEJ3HEK4PH8S7SW', '01JH4V1QT665JXKHHGE7R78CP9','01JH4TZKY97AR4N5T40B7MQDHS'])
# adata = API.GetReceiptList(record_ids = ['RC2025011403462351166494637166592',
#                                          'RC2025011403444851166094760611840',
#                                          'RC2025011403451651166209831342080'])
# pprint(adata)


""" 收银台收款 """
# adata = API.Checkout(bill_id,
#                            "1902225p16qojepfbsfcmo8app61wyhh",
#                            '1000',
#                            'IND',
#                            'UPI')
# pprint(adata)

""" 代付 """

######################## 创建代付记录
# adata = API.CreatePayment(bill_id,
#                             '1902225p16qojepfbsfcmo8app61wyhh',
#                             "5000",
#                             'IND',
#                             'jooo',
#                             vpa="sss@upi.com",
#                             # bank_code='bank_code',
#                             # holder_account='1234567894521356'
#                             )
# pprint(adata)

######################### 查询代付记录   01JHSVA0AS34BYRKXZJ5JHHDHC
# adata = API.GetPayment(bill_id='01JHSVBXVDZ7HH1AWYCS76XSYS')
# pprint(adata)

######################### 查询代付记录列表

# 时间筛选
# adata = API.GetPaymentList(1728921600,
#                            1736352000)
# 订单列表筛选
# adata = API.GetPaymentList(bill_ids = ['41e9981f-bd86-4491-b5ff-c2ad2062fe7f',
#                                        '9ecd0533-2421-49c1-9345-f32d415c5978',
#                                        '01154a27-1e16-457e-9604-fc2af6628086'])
# adata = API.GetPaymentList(record_ids = ['PM2024122003362942104304848343041',
#                                          'PM2024122002324142088250696798209',
#                                          'PM2024122002332742088443198574593'])
# pprint(adata)

"""资产管理"""
######################### 获取账户资产
# inr 1902225p16qojepfbsfcmo8app61wyhh
# usdt 5ddeeacb13244b0cb772e4af9830f0bf
# 测试币 646258fb44e54b3d82775187f9f3e032 '9.076838056954771552'
# adata = API.GetBalance("1902225p16qojepfbsfcmo8app61wyhh")
# pprint(adata)

######################## 代币换法币
# adata = API.CryptoToCurrency('5ddeeacb13244b0cb772e4af9830f0bf',
#                              '1902225p16qojepfbsfcmo8app61wyhh',
#                              '0.01',
#                              '0')
# pprint(adata)

######################### 法币换代币
# adata = API.CurrencyToCrypto('1902225p16qojepfbsfcmo8app61wyhh',
#                              '5ddeeacb13244b0cb772e4af9830f0bf',
#                              '0.01',
#                              '0')
# pprint(adata)

######################### 获取换币记录
# adata = API.GetSwap(adata.get("data").get("record_id"))
# pprint(adata)

######################### 获取换币记录列表
# adata = API.GetSwapList(['SW2025011002472249702087524618240',
#                          'SW2025011003192049710131864145920',
#                          'SW2025011003193749710203796459520'])
# pprint(adata)
# adata = API.GetSwapList(start_at=1728921600, end_at=1736352000)
# pprint(adata)

######################### 查询充值记录
# adata = API.GetDeposit('DP2024123008175445799005908635648')
# pprint(adata)
######################### 查询充值记录列表
# adata = API.GetDepositList(['DP2025010111143346568234698149888', 'DP2025010210492246924286107062272', 'DP2024123106252646133090539540480'])
# pprint(adata)

# adata = API.GetDepositList(start_at=1728921600, end_at=1736352000)
# pprint(adata)

######################### 代币提现
# adata = API.ApplyCryptoWithdraw(bill_id,
#                                 '646258fb44e54b3d82775187f9f3e032',
#                                 '0.001',
#                                 '0xCb74CF563753A49E40e938f7C4356faB83664b1A',
#                                 'ETH_SEPOLIA',
#                                 )
# pprint(adata)
######################### 查询提现记录
# adata = API.GetWithdraw(bill_id=bill_id)
# pprint(adata)
######################### 查询提现记录列表
# # 时间筛选
# adata = API.GetReceiptRecordList(1728921600,
#                                  1736352000)
# pprint(adata)
# 订单列表筛选
# adata = API.GetWithdrawList(bill_ids = ['01JH7JPCP842HDN730AYCCZ4N9',
#                                         '01JH7JW21WSWG1NEVXNXNGX7JP'])
# adata = API.GetWithdrawList(record_ids = ['WD2024123112211246222621515190273',
#                                           'WD2024123112192746222179636875265',
#                                           'WD2024123112171146221607881936897'])
# pprint(adata)

######################### 获取银行码列表
# adata = API.GetBankList()
# pprint(adata)

######################### 获取收款单配置
# adata = API.GetServiceConfigsReceipt('1902225p16qojepfbsfcmo8app61wyhh')
# pprint(adata)
#
#
# min_amount = [i.get("min_amount") for i in API.GetServiceConfigsReceipt('1902225p16qojepfbsfcmo8app61wyhh').get("data").get("records") if i.get("payment_method") == 'Upi']
# min_amount = sorted(min_amount)[0]
# print(min_amount)
######################### 获取付款单配置
# adata = API.GetServiceConfigsPayment('1902225p16qojepfbsfcmo8app61wyhh')
# pprint(adata)

""" openapi """
# if __name__ == '__main__':
#     pytest.main(['-vs','/Users/songwriter/Desktop/project/bankpayos-test-script/BankpayOS_MS/case/'
#                        'test_openapi.py::Test_api::test_GetServiceConfigsPayment'])

""" url_test """
# if __name__ == '__main__':
#     pytest.main(['-vs','/Users/songwriter/Desktop/project/bankpayos-test-script/BankpayOS_MS/case/'
#                        'test_official_url.py'])