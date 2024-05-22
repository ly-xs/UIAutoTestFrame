import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

# 配置文件
CONFIG_FILE = os.path.join(BASE_DIR, "config", "config.ini")
# 浏览器驱动目录
DRIVER_DIR = os.path.join(BASE_DIR, "driver")

# 测试报告目录
REPORT_DIR = os.path.join(BASE_DIR, "report")
# 日志文件目录
LOG_DIR = os.path.join(REPORT_DIR, "logs")

# 页面元素目录
PAGE_DATA_DIR = os.path.join(BASE_DIR, 'pageobject', "pagedata")
# 测试用例目录
TEST_CASE_DIR = os.path.join(BASE_DIR, "testcase")
# 测试数据文件
TEST_DATA_DIR = os.path.join(TEST_CASE_DIR, "testdata")
