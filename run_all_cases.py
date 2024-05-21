import configparser
import os
import sys
import time
import unittest

sys.path.append(os.path.dirname(__file__))
from package.HTMLTestRunner import HTMLTestRunner
from common.sendmail import send_mail
from common.newReport import new_report
from config.config import REPORT_DIR, TEST_CASE_DIR, CONFIG_FILE

# 读取config.ini配置文件
config = configparser.ConfigParser()
config.read(CONFIG_FILE, encoding="utf-8")
browser = config.get("Browser", "browser")


def run_case(test_path=TEST_CASE_DIR, result_path=REPORT_DIR):
    """执行所有的测试用例"""
    now = time.strftime("%Y-%m-%d %H_%M_%S")
    filename = result_path + '/' + now + 'result.html'
    with open(filename, 'wb') as f:
        runner = HTMLTestRunner(stream=f, title='抽屉新热榜UI自动化测试报告', description=f'环境：windows 10 浏览器：{browser}')
        runner.run(unittest.defaultTestLoader.discover(test_path, pattern='login_test.py'))
    report = new_report(result_path)  # 调用模块生成最新的报告
    send_mail(report)  # 调用发送邮件模块


if __name__ == "__main__":
    run_case()
