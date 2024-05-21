import configparser
import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from common.driver import create_driver
from config.config import CONFIG_FILE

# 读取config.ini配置文件
config = configparser.ConfigParser()
config.read(CONFIG_FILE, encoding="utf-8")
browser = config.get("Browser", "browser")


class BaseTestCase(unittest.TestCase):
    """
    自定义TestCase类
    """
    driver = None

    @classmethod
    def setUpClass(cls):
        cls.driver = create_driver(browser=browser)
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
