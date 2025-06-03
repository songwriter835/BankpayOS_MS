#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @time    : 2024/11/3 11:41

"""
==========  启动框架  ==========
Used to start the test framework, you can configure parameters
"""
__author__ = 'songwriter'

import pytest
import BankpayOS_MS.common.utils as ut
# 时间
time_now = ut.get_time()
pytest.main(['-vs', f'--html={ut.report_path}/{time_now}.html', f"{ut.case_path}",'--reruns', '2','--reruns-delay', '2'])
