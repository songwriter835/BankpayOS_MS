import base64
import json
import requests
import inspect
from BankpayOS_MS.data.EnvConfig import *
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256


class OpenApi(object):


    def __init__(self):
        # 环境 prod/test/local
        match env:
            case "prod":
                # app_id 必要参数
                self.app_id = envs.get('APP_ID')
                # 私钥加密 必要参数
                keyPair = RSA.importKey(envs.get('PRIVATE_KEY'))
                self.signer = PKCS1_v1_5.new(keyPair)
                # host
                self.host = PROD_HOST
            case "test":
                # app_id 必要参数
                self.app_id = envs_test.get('APP_ID')
                # 私钥加密 必要参数
                keyPair = RSA.importKey(envs_test.get('PRIVATE_KEY'))
                self.signer = PKCS1_v1_5.new(keyPair)
                # host
                self.host = TEST_HOST
            case "local":
                # app_id 必要参数
                self.app_id = envs_local.get('APP_ID')
                # 私钥加密 必要参数
                keyPair = RSA.importKey(envs_local.get('PRIVATE_KEY'))
                self.signer = PKCS1_v1_5.new(keyPair)
                # host
                self.host = LOCAL_HOST

    def getHeaders(self):
        """
        获取请求头
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "AppId": self.app_id,
            "Sign": "",
        }
        return headers

    def getSign(self, params=None):
        """
        生成签名

        Args:
            params (dict): 参数字典，默认值为空字典。

        Returns:
            str: 签名字符串。
        """
        if params is None:
            params = {}

        # 确保 app_id 存在
        params["app_id"] = self.app_id

        # 对键排序
        sorted_keys = sorted(params.keys())
        # 构建签名字符串数组
        sign_components = []
        for key in sorted_keys:
            if key == "sign":
                continue  # 跳过签名字段
            value = params.get(key)
            if isinstance(value, list) and all(isinstance(item, str) for item in value):
                # 处理字符串列表：排序并用逗号连接
                sorted_list = sorted(value)
                value = ",".join(sorted_list)
            sign_components.append(f"{key}={value}")
        # 构建签名字符串
        sign_str = "&".join(sign_components)

        # 转换为字节并计算 SHA256 哈希
        sign_bytes = sign_str.encode("utf-8")
        hash_obj = SHA256.new(sign_bytes)

        # 使用签名器签名
        signature = self.signer.sign(hash_obj)

        # Base64 编码并移除换行符
        encoded_signature = base64.b64encode(signature).decode("utf-8").replace("\n", "")

        return encoded_signature

    def Unifiedrequest(self, data, aotug, defname):
        """
        统一请求
        签名控制
        """
        url = self.host+addr_info.get(f'{defname}_addr')
        header = self.getHeaders()
        if aotug:
            header['sign'] = self.getSign(data)
        else:
            header['sign'] = json.dumps(data)
        response = requests.post(url=url, headers=header, json=data)
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            print("not JSON response:", response.text)

    @staticmethod
    def getcoinid(coin_name):
        """
        获取货币coinid
        """
        try:
            coin_list_ = {x.lower(): y  for x,y in coin_list.items()}
            return coin_list_.get(coin_name.lower())
        except Exception as e:
            print("****** Please enter the correct currency abbreviation",e)


    def Checkout(self, bill_id, amount, coin_id, country, payment_method, aotug=True):
        """
        创建收银台
        """
        data={
            "bill_id":bill_id,
            "coin_id":coin_id,
            "amount":amount,
            "country":country,
            # UPI/GooglePay/BankTransfer
            "payment_method":payment_method,
            "return_url":"https://betamerchantconsole.agentstudio.site/developer/index"
        }
        return self.Unifiedrequest(data, aotug, inspect.currentframe().f_code.co_name)

    def CreateReceipt(self, bill_id, amount, country, coin_id, payment_method, aotug=True):
        """
        创建代收订单
        """
        data = {
            "bill_id": bill_id,
            "amount": amount,
            "coin_id": coin_id,
            "country": country,
            "payment_method":payment_method,
        }
        return self.Unifiedrequest(data, aotug, inspect.currentframe().f_code.co_name)

    def ConfirmReceipt(self, bill_id, pay_proof_id, aotug=True):
        """
        确认代收记录
        """

        data = {
            "bill_id": bill_id,
            "pay_proof_id": pay_proof_id
        }
        return self.Unifiedrequest(data, aotug, inspect.currentframe().f_code.co_name)

    def CancelReceipt(self, bill_id, aotug=True):
        """
        取消订单
        """
        data = {
            "bill_id": bill_id,
        }
        return self.Unifiedrequest(data, aotug, inspect.currentframe().f_code.co_name)

    def GetReceipt(self, record_id=None, bill_id=None, aotug=True):
        """
        查询代收记录
        """
        if record_id:
            data = {
                "record_id": record_id,
            }
        elif bill_id:
            data = {
                "bill_id": bill_id
            }
        else:
            raise Exception ('record_id or bill_id There must be one')

        return self.Unifiedrequest(data, aotug, inspect.currentframe().f_code.co_name)

    def GetReceiptList(self, start_at=None, end_at=None, record_ids=None, bill_ids=None, aotug=True):
        """
        查询代收列表
        """
        if record_ids:
            data = {
                "record_ids": record_ids,
            }
        elif bill_ids:
            data = {
                "bill_ids": bill_ids,
            }
        else:
            data = {
                "start_at": start_at,
                "end_at": end_at
            }
        return self.Unifiedrequest(data, aotug, inspect.currentframe().f_code.co_name)

    def CreatePayment(self, bill_id, amount, coin_id, country, payment_method, vpa=None, aotug=True):
        """
        创建代付记录
        """
        if vpa:
            data = {
                "bill_id": bill_id,
                "coin_id": coin_id,
                "amount": amount,
                'country': country,
                "payment_method": payment_method,
                "vpa": vpa
            }
        else:
            raise Exception('upa or holder_account There must be one')
        return self.Unifiedrequest(data, aotug, inspect.currentframe().f_code.co_name)

    def GetPayment(self, record_id=None, bill_id=None, aotug=True):
        """
        查询代付记录
        """
        if record_id:
            data = {
                "record_id": record_id,
            }
        elif bill_id:
            data = {
                "bill_id": bill_id
            }
        else:
            raise Exception('record_id or bill_id There must be one')
        return self.Unifiedrequest(data, aotug, inspect.currentframe().f_code.co_name)

    def GetPaymentList(self, start_at=None, end_at=None, record_ids=None, bill_ids=None, aotug=True):
        """
        查询代付列表
        """
        if record_ids:
            data = {
                "record_ids": record_ids,
            }
        elif bill_ids:
            data = {
                "bill_ids": bill_ids,
            }
        else:
            data = {
                "start_at": start_at,
                "end_at": end_at
            }
        return self.Unifiedrequest(data, aotug, inspect.currentframe().f_code.co_name)

    def GetBalance(self, coin_id, aotug=True):
        """
        查询现金资产余额
        """
        data = {
            "coin_id": coin_id
        }
        return self.Unifiedrequest(data, aotug, inspect.currentframe().f_code.co_name)

    def CryptoToCurrency(self, from_coin_id, to_coin_id, submit_amount, discount, aotug=True):
        """
        代币换法币
        """
        data = {
            "from_coin_id": from_coin_id,
            "to_coin_id": to_coin_id,
            "submit_amount": submit_amount,
            "discount": discount,
        }
        return self.Unifiedrequest(data, aotug, inspect.currentframe().f_code.co_name)

    def CurrencyToCrypto(self, from_coin_id, to_coin_id, submit_amount, discount, aotug=True):
        """
        法币换代币
        """
        data = {
            "from_coin_id": from_coin_id,
            "to_coin_id": to_coin_id,
            "submit_amount": submit_amount,
            "discount": discount,
        }
        return self.Unifiedrequest(data, aotug, inspect.currentframe().f_code.co_name)

    def GetSwap(self, record_id, aotug=True):
        """
        获取换币记录
        """
        data = {
                "record_id": record_id,
            }
        return self.Unifiedrequest(data, aotug, inspect.currentframe().f_code.co_name)

    def GetSwapList(self, record_ids=None, start_at=None, end_at=None, aotug=True):
        """
        获取换币记录列表
        """
        if record_ids:
            data = {
                "record_ids": record_ids,
            }
        else:
            data = {
                "start_at": start_at,
                "end_at": end_at
            }
        return self.Unifiedrequest(data, aotug, inspect.currentframe().f_code.co_name)

    def GetDeposit(self, record_id, aotug=True):
        """
        查询充值记录
        """
        data = {
            "record_id": record_id
        }
        return self.Unifiedrequest(data, aotug, inspect.currentframe().f_code.co_name)

    def GetDepositList(self, record_ids=None, start_at=None, end_at=None, aotug=True):
        """
        查询充值列表
        """
        if record_ids:
            data = {
                "record_ids": record_ids,
            }
        else:
            data = {
                "start_at": start_at,
                "end_at": end_at
            }
        return self.Unifiedrequest(data, aotug, inspect.currentframe().f_code.co_name)

    def ApplyCryptoWithdraw(self, bill_id, coin_id, amount, address, network, remark=None, aotug=True):
        """
        代币提现
        """
        if remark:
            data = {
                "bill_id": bill_id,
                "coin_id": coin_id,
                "amount": amount,
                "address": address,
                "network": network,
                "remark": remark
            }
        else:
            data = {
                "bill_id": bill_id,
                "coin_id": coin_id,
                "amount": amount,
                "address": address,
                "network": network
            }
        return self.Unifiedrequest(data, aotug, inspect.currentframe().f_code.co_name)

    def GetWithdraw(self, record_id=None, bill_id=None, aotug=True):
        """
        查询提现记录
        """
        if record_id:
            data = {
                "record_id": record_id,
            }
        elif bill_id:
            data = {
                "bill_id": bill_id
            }
        else:
            raise Exception ('record_id or bill_id There must be one')
        return self.Unifiedrequest(data, aotug, inspect.currentframe().f_code.co_name)

    def GetWithdrawList(self, start_at=None, end_at=None, record_ids=None, bill_ids=None, aotug=True):
        """
        查询提现列表
        """
        if record_ids:
            data = {
                "record_ids": record_ids,
            }
        elif bill_ids:
            data = {
                "bill_ids": bill_ids,
            }
        else:
            data = {
                "start_at": start_at,
                "end_at": end_at
            }
        return self.Unifiedrequest(data, aotug, inspect.currentframe().f_code.co_name)

    def GetBankList(self, aotug=True):
        """
        获取银行码列表
        """
        data = {
        }
        return self.Unifiedrequest(data, aotug, inspect.currentframe().f_code.co_name)

    def GetServiceConfigsReceipt(self, coin_id, aotug=True):
        """
        获取收款单配置
        """
        data = {
            'coin_id':coin_id
        }
        return self.Unifiedrequest(data, aotug, inspect.currentframe().f_code.co_name)

    def GetServiceConfigsPayment(self, coin_id, aotug=True):
        """
        获取付款单配置
        """
        data = {
            'coin_id':coin_id
        }
        return self.Unifiedrequest(data, aotug, inspect.currentframe().f_code.co_name)
