import pytest
import BankpayOS_MS.common.utils as ut
# 时间
time_now = ut.get_time()
pytest.main(['-vs', f'--html={ut.report_path}/{time_now}.html', f"{ut.case_path}",'--reruns', '2','--reruns-delay', '2'])
