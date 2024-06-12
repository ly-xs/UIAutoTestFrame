import configparser
import os
import sys
import time
import unittest

sys.path.append(os.path.dirname(__file__))
from common.HTMLTestRunner import HTMLTestRunner
from common.sendmail import send_mail
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
        runner.run(unittest.defaultTestLoader.discover(test_path, pattern='loginTest.py'))

    # 删除超过五个的报告
    log_files = sorted(
        (os.path.join(result_path, f) for f in os.listdir(result_path) if f.endswith('.html')),
        key=os.path.getmtime
    )
    while len(log_files) > 5:
        os.remove(log_files.pop(0))

    # 调用发送邮件模块
    lists = os.listdir(result_path)
    lists.sort(key=lambda fn: os.path.getmtime(result_path + "\\" + fn))
    report = os.path.join(result_path, lists[-1])
    # send_mail(report)


if __name__ == "__main__":
    run_case()
