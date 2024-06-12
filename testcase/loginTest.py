import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import unittest
import configparser
from common.driver import create_driver
from common.getYaml import GetYaml
from ddt import ddt, data
from config.config import TEST_DATA_DIR, CONFIG_FILE
from common.logger import Logger
from pageobject.loginPage import login

logger = Logger().get_logger(__name__)
# 读取config.ini配置文件
config = configparser.ConfigParser()
config.read(CONFIG_FILE, encoding="utf-8")
browser = config.get("Browser", "browser")


@ddt
class LoginTestCase(unittest.TestCase):
    """
    抽屉新热榜登录测试
    """
    def setUp(self):
        self.login = login(create_driver(browser=browser))
        self.login.implicitly_wait()
        self.login.maximize_window()

    def tearDown(self):
        self.login.quit()

    @data(*GetYaml(TEST_DATA_DIR + r"\login_data.yaml").get_yaml())
    def test_login(self, testdata):
        """
        登录测试
        :param testdata: 加载login_data登录测试数据
        :return:
        """
        logger.info(f"当前执行测试用例ID-> {testdata['id']}; 测试点-> {testdata['detail']}")
        # 调用登录方法
        self.login.user_login(testdata['data']['phone'], testdata['data']['password'])
        if testdata['screenshot'] == 'phone_pwd_success':
            self.assertEqual(self.login.user_login_success_hint(), testdata['check'][0],
                             f"成功登录，返回实际结果是->: {self.login.user_login_success_hint()}")
            self.login.save_web_img(testdata['screenshot'])
            self.login.user_login_exit()
            self.assertEqual(self.login.exit_login_success_hint(), testdata['check'][1],
                             f"退出登录，返回实际结果是->: {self.login.exit_login_success_hint()}")
        else:
            self.login.save_web_img(testdata['screenshot'])
            self.assertEqual(self.login.user_login_error_hint(), testdata['check'][0],
                             f"异常登录，返回实际结果是->: {self.login.user_login_error_hint()}")
