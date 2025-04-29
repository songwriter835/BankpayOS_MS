"""
==========  脚本控制  ==========
Environment configuration prod/test/local
"""

# 运行环境 prod/test/local
env = 'test'

"""=================================  接口地址  ======================================="""
# 生产环境
PROD_HOST = "https://agentstudio.site"
# 测试环境
TEST_HOST = "http://43.207.72.1:8032"
# 本地
LOCAL_HOST = "http://43.207.72.1:8032"
# addr
addr_info = {
    # 创建收银台
    'Checkout_addr':'/api/v1/receipt/checkout',
    # 创建代收订单
    'CreateReceipt_addr':'/api/v1/receipt/createReceipt',
    # 确认代收记录
    'ConfirmReceipt_addr':'/api/v1/receipt/confirmReceipt',
    # 取消订单
    'CancelReceipt_addr':'/api/v1/receipt/cancelReceipt',
    # 查询代收记录
    'GetReceipt_addr':'/api/v1/receipt/getReceipt',
    # 查询代收列表
    'GetReceiptList_addr':'/api/v1/receipt/getReceiptList',
    # 创建代付记录
    'CreatePayment_addr':'/api/v1/payment/createPayment',
    # 查询代付记录
    'GetPayment_addr':'/api/v1/payment/getPayment',
    # 查询代付列表
    'GetPaymentList_addr':'/api/v1/payment/getPaymentList',
    # 查询现金资产余额
    'GetBalance_addr':'/api/v1/asset/getBalance',
    # 代币换法币
    'CryptoToCurrency_addr':'/api/v1/asset/swap/cryptoToCurrency',
    # 法币换代币
    'CurrencyToCrypto_addr':'/api/v1/asset/swap/currencyToCrypto',
    # 获取换币记录
    'GetSwap_addr':'/api/v1/asset/swap/getSwap',
    # 获取换币记录列表
    'GetSwapList_addr':'/api/v1/asset/swap/getSwapList',
    # 查询充值记录
    'GetDeposit_addr': '/api/v1/asset/deposit/getDeposit',
    # 查询充值列表
    'GetDepositList_addr': '/api/v1/asset/deposit/getDepositList',
    # 代币提现
    'ApplyCryptoWithdraw_addr':'/api/v1/asset/withdraw/applyCryptoWithdraw',
    # 查询提现记录
    'GetWithdraw_addr':'/api/v1/asset/withdraw/getWithdraw',
    # 查询提现列表
    'GetWithdrawList_addr':'/api/v1/asset/withdraw/getWithdrawList',
    # 获取银行码列表
    'GetBankList_addr':'/api/v1/asset/getBankList',
    # 获取收款单配置
    'GetServiceConfigsReceipt_addr':'/api/v1/receipt/getServiceConfigs',
    # 获取付款单配置
    'GetServiceConfigsPayment_addr':'/api/v1/payment/getServiceConfigs',

}


"""=================================  正式环境参数  ======================================="""
envs = {
    # app-id
    'APP_ID': 'd7ec22d58086479fbeeae2c62b906060',
    # 私钥
    'PRIVATE_KEY': '''-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAuQL6jF94LEmJWU7bDYvC48+bj6N2x+0zFq3ZlDQSWzrRWGRd
ikJY/rmKT0b8I7TmIo9RTLPr+EdnahMcZ0+wYV2NBLNNGQ18LesWEJVwhYjaewQL
kJ77Q0/uLFiWl2Lq2lcWAVknRa8YvTHjW8EGapVUJ8+VxXbV5QlkRDzNvuLQVwHQ
yfJRTIZ54tiEzu8U1pTYBrbjcRHJbRb53S/ZDAV5TiOXNkgLznSCPhNeXU8p3ce+
jHUTosIbVtdmbTxvmCPgRzF7q3dkjIUSv4FJGXC42/Y5PLF+D8TvjglfVb0v6TL+
YeUJxQ/B2YoFPp2Wr/AAJdH/C84yfOgXouA1dQIDAQABAoIBAHMY0kvvvLA4k1TX
BNm5f+X/qvRCKkwYWbcbMofLmTveLIyD69luizT0soG9VHDWQnFvnZFNQVi0+zX3
a60t2znHXEp3TVhvljhuzsxEW7sHN3xeON+guAnZOP+noQ/O/vIUSWFPWGo2kvpo
hdv4CojWG4Ok1bUBx/Fz1UfKV+kO3MW2qf4QJVjaBJfrQXH13paYnnSKEx2I5XJf
kGSBnAX8l2Qk6O6dGXKhlOINcWMFoGflB8fG5fk3iiCc2Dx1p/AVXWGQ5alsJpwP
GZwqbGi1aZZDNmigMBVjCXsseWSbj8hFrkikKkoTbnaY2MJWgwkxl4YpISg2Zc/d
FcUu+GECgYEA4OtBEE+YTg0rrDGy8GvDSJ2c4A0L5A+mm86uf/vl1Uaq8whH7wm7
OgpkFnn+l84z225E+EWaYZ3V4xwiZ//qk0FzdsZn1CbVD3bc3CwJ45NujvPhbs+r
dm30HFBtuKIkQBjfsHW9ggPyJ70cXfWO5dueUgK2Bcl1gCAYammD7J0CgYEA0pP1
8vzaWJXDfXDZ3yzEoXqISMQMaWdIfKta8+FKAutk4EvSOBqHe1zU1I0+rcEP5RI3
EiwDgQYP8eD2OiAm4O4hN5xc+5XTvcw2uQuOzQzjYEQDTkxBkaC0HleVm3SU+Ogh
4qghqO5R2I/AlXogOCMFpMU9pVN0BDHbgJQxmLkCgYEA2cw1Vvwcegha8AW4RwOz
ONAXJwa7Kv7U0S+U3q4oYxxpUaoFLj34JT4GqZU8qfetU6E1/Ew6MKjMg32s+5Rf
rHTGwI9j35Yy3yS0vieO8+bCOn+DHvDOEoJqzjg753xrKf5sLc310r7LcRu5Kmst
EvxWFQg3BueMdqOdwP2oGCkCgYAYn0Jf4h7pwsEz9rES/loTg49R6tKEtJXuNd8R
qyMLSljmPRdchgWXcBhWrhlJGczw/PtBfbH/MSVGJAbGbyH8pPtvVDIvHKrAg5NW
ebp90Wb4x5sXWaVFEORes+EDZ1NP81ya8wvUg+FAEDb1g20nAzlStdlqbmKfZvEC
jNFryQKBgHmGSLCwmxj+7QeisLv178676lJZx41nHEPXh8tvsLWCs87ENEWCGpbq
H4HLn6pDBDhJOQSidwxPIKS234lYRGKy/seHvFZ7GXWCaH5lyVy4anyFwfw00Gc4
tH9M85GBlIL0C79abjA0KhqyuUOq/P67mqfWN+mr7bWi1J/9Ja+8
-----END RSA PRIVATE KEY-----'''
}

"""=================================  测试环境参数  ======================================="""
envs_test = {
    # app-id
    'APP_ID': '3832dc1729a54ae3926b4b382dea5cc4',
    'APP_ID_testcoin': '3832dc1729a54ae3926b4b382dea5cc4',
    # 私钥
    'PRIVATE_KEY': '''-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAuQL6jF94LEmJWU7bDYvC48+bj6N2x+0zFq3ZlDQSWzrRWGRd
ikJY/rmKT0b8I7TmIo9RTLPr+EdnahMcZ0+wYV2NBLNNGQ18LesWEJVwhYjaewQL
kJ77Q0/uLFiWl2Lq2lcWAVknRa8YvTHjW8EGapVUJ8+VxXbV5QlkRDzNvuLQVwHQ
yfJRTIZ54tiEzu8U1pTYBrbjcRHJbRb53S/ZDAV5TiOXNkgLznSCPhNeXU8p3ce+
jHUTosIbVtdmbTxvmCPgRzF7q3dkjIUSv4FJGXC42/Y5PLF+D8TvjglfVb0v6TL+
YeUJxQ/B2YoFPp2Wr/AAJdH/C84yfOgXouA1dQIDAQABAoIBAHMY0kvvvLA4k1TX
BNm5f+X/qvRCKkwYWbcbMofLmTveLIyD69luizT0soG9VHDWQnFvnZFNQVi0+zX3
a60t2znHXEp3TVhvljhuzsxEW7sHN3xeON+guAnZOP+noQ/O/vIUSWFPWGo2kvpo
hdv4CojWG4Ok1bUBx/Fz1UfKV+kO3MW2qf4QJVjaBJfrQXH13paYnnSKEx2I5XJf
kGSBnAX8l2Qk6O6dGXKhlOINcWMFoGflB8fG5fk3iiCc2Dx1p/AVXWGQ5alsJpwP
GZwqbGi1aZZDNmigMBVjCXsseWSbj8hFrkikKkoTbnaY2MJWgwkxl4YpISg2Zc/d
FcUu+GECgYEA4OtBEE+YTg0rrDGy8GvDSJ2c4A0L5A+mm86uf/vl1Uaq8whH7wm7
OgpkFnn+l84z225E+EWaYZ3V4xwiZ//qk0FzdsZn1CbVD3bc3CwJ45NujvPhbs+r
dm30HFBtuKIkQBjfsHW9ggPyJ70cXfWO5dueUgK2Bcl1gCAYammD7J0CgYEA0pP1
8vzaWJXDfXDZ3yzEoXqISMQMaWdIfKta8+FKAutk4EvSOBqHe1zU1I0+rcEP5RI3
EiwDgQYP8eD2OiAm4O4hN5xc+5XTvcw2uQuOzQzjYEQDTkxBkaC0HleVm3SU+Ogh
4qghqO5R2I/AlXogOCMFpMU9pVN0BDHbgJQxmLkCgYEA2cw1Vvwcegha8AW4RwOz
ONAXJwa7Kv7U0S+U3q4oYxxpUaoFLj34JT4GqZU8qfetU6E1/Ew6MKjMg32s+5Rf
rHTGwI9j35Yy3yS0vieO8+bCOn+DHvDOEoJqzjg753xrKf5sLc310r7LcRu5Kmst
EvxWFQg3BueMdqOdwP2oGCkCgYAYn0Jf4h7pwsEz9rES/loTg49R6tKEtJXuNd8R
qyMLSljmPRdchgWXcBhWrhlJGczw/PtBfbH/MSVGJAbGbyH8pPtvVDIvHKrAg5NW
ebp90Wb4x5sXWaVFEORes+EDZ1NP81ya8wvUg+FAEDb1g20nAzlStdlqbmKfZvEC
jNFryQKBgHmGSLCwmxj+7QeisLv178676lJZx41nHEPXh8tvsLWCs87ENEWCGpbq
H4HLn6pDBDhJOQSidwxPIKS234lYRGKy/seHvFZ7GXWCaH5lyVy4anyFwfw00Gc4
tH9M85GBlIL0C79abjA0KhqyuUOq/P67mqfWN+mr7bWi1J/9Ja+8
-----END RSA PRIVATE KEY-----
'''
}


"""=================================  本地环境参数  ======================================="""
envs_local = {
    # app-id
    'APP_ID': '3b85a684f8bb4acba05c1c5433e49c6f',
    # 私钥
    'PRIVATE_KEY': '''-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAuQL6jF94LEmJWU7bDYvC48+bj6N2x+0zFq3ZlDQSWzrRWGRd
ikJY/rmKT0b8I7TmIo9RTLPr+EdnahMcZ0+wYV2NBLNNGQ18LesWEJVwhYjaewQL
kJ77Q0/uLFiWl2Lq2lcWAVknRa8YvTHjW8EGapVUJ8+VxXbV5QlkRDzNvuLQVwHQ
yfJRTIZ54tiEzu8U1pTYBrbjcRHJbRb53S/ZDAV5TiOXNkgLznSCPhNeXU8p3ce+
jHUTosIbVtdmbTxvmCPgRzF7q3dkjIUSv4FJGXC42/Y5PLF+D8TvjglfVb0v6TL+
YeUJxQ/B2YoFPp2Wr/AAJdH/C84yfOgXouA1dQIDAQABAoIBAHMY0kvvvLA4k1TX
BNm5f+X/qvRCKkwYWbcbMofLmTveLIyD69luizT0soG9VHDWQnFvnZFNQVi0+zX3
a60t2znHXEp3TVhvljhuzsxEW7sHN3xeON+guAnZOP+noQ/O/vIUSWFPWGo2kvpo
hdv4CojWG4Ok1bUBx/Fz1UfKV+kO3MW2qf4QJVjaBJfrQXH13paYnnSKEx2I5XJf
kGSBnAX8l2Qk6O6dGXKhlOINcWMFoGflB8fG5fk3iiCc2Dx1p/AVXWGQ5alsJpwP
GZwqbGi1aZZDNmigMBVjCXsseWSbj8hFrkikKkoTbnaY2MJWgwkxl4YpISg2Zc/d
FcUu+GECgYEA4OtBEE+YTg0rrDGy8GvDSJ2c4A0L5A+mm86uf/vl1Uaq8whH7wm7
OgpkFnn+l84z225E+EWaYZ3V4xwiZ//qk0FzdsZn1CbVD3bc3CwJ45NujvPhbs+r
dm30HFBtuKIkQBjfsHW9ggPyJ70cXfWO5dueUgK2Bcl1gCAYammD7J0CgYEA0pP1
8vzaWJXDfXDZ3yzEoXqISMQMaWdIfKta8+FKAutk4EvSOBqHe1zU1I0+rcEP5RI3
EiwDgQYP8eD2OiAm4O4hN5xc+5XTvcw2uQuOzQzjYEQDTkxBkaC0HleVm3SU+Ogh
4qghqO5R2I/AlXogOCMFpMU9pVN0BDHbgJQxmLkCgYEA2cw1Vvwcegha8AW4RwOz
ONAXJwa7Kv7U0S+U3q4oYxxpUaoFLj34JT4GqZU8qfetU6E1/Ew6MKjMg32s+5Rf
rHTGwI9j35Yy3yS0vieO8+bCOn+DHvDOEoJqzjg753xrKf5sLc310r7LcRu5Kmst
EvxWFQg3BueMdqOdwP2oGCkCgYAYn0Jf4h7pwsEz9rES/loTg49R6tKEtJXuNd8R
qyMLSljmPRdchgWXcBhWrhlJGczw/PtBfbH/MSVGJAbGbyH8pPtvVDIvHKrAg5NW
ebp90Wb4x5sXWaVFEORes+EDZ1NP81ya8wvUg+FAEDb1g20nAzlStdlqbmKfZvEC
jNFryQKBgHmGSLCwmxj+7QeisLv178676lJZx41nHEPXh8tvsLWCs87ENEWCGpbq
H4HLn6pDBDhJOQSidwxPIKS234lYRGKy/seHvFZ7GXWCaH5lyVy4anyFwfw00Gc4
tH9M85GBlIL0C79abjA0KhqyuUOq/P67mqfWN+mr7bWi1J/9Ja+8
-----END RSA PRIVATE KEY-----
'''
}
