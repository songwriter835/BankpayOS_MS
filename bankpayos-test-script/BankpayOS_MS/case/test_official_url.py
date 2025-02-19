import pytest
from BankpayOS_MS.common.utils import *
# # 测试数据读取
file = data_path + "/test_official_url.csv"
test_data = read_csv(file)
RESET = "\033[0m"  # 重置样式
BLUE = "\033[34m"  # 字体颜色


class Test_official_url(object):

    # url访问测试
    @staticmethod
    @pytest.mark.parametrize("case_info", test_data[1:], ids=[i[0] for i in test_data[1:]])
    def test_official_url(case_info):
        print(f"{BLUE}用例名称：{case_info[1]}{RESET}")
        url = case_info[2]
        url_status_code = send_request(url, f'{case_info[3].lower()}', )[0].status_code
        assert str(url_status_code) == case_info[4], f'用例失败，状态码[{url_status_code}]，链接[{url}]'

if __name__ == '__main__':
    pytest.main(["-vs", __file__])
