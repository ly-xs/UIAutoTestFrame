import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import unittest
from common.driver import create_driver
from common.getYaml import GetYaml
from common.logger import Logger
from config.config import TEST_DATA_DIR
from pageobject.setupPage import setup
from ddt import ddt, data
from pageobject.loginPage import login

LoginData = GetYaml(TEST_DATA_DIR + r"\login_data.yaml").get_yaml()
phone = LoginData[5]['data']['phone']
password = LoginData[5]['data']['password']
logger = Logger().get_logger(__name__)


@ddt
class SetupTestCase(unittest.TestCase):
    """
    首页---设置
    """
    def setUp(self):
        self.driver = create_driver()
        self.login = login(self.driver)
        self.setup = setup(self.driver)
        self.setup.implicitly_wait()
        self.setup.maximize_window()

    def tearDown(self):
        self.setup.quit()

    @data(*GetYaml(TEST_DATA_DIR + r"\setup_data.yaml").get_yaml())
    def test_setup(self, testdata):
        """
        首页---设置操作测试
        :param testdata: 加载login_data登录测试数据
        :return:
        """
        logger.info(f"当前执行测试用例ID-> {testdata['id']}; 测试点-> {testdata['detail']}")

        # 调用登录方法
        self.login.user_login(phone, password)

        # 调用设置接口
        self.setup.dig_setup(testdata['data']['name'], testdata['data']['sign'])
        if testdata['screenshot'] == 'name_empty':
            self.assertEqual(self.setup.nick_error_hint(), testdata['check'][0],
                             f"返回实际结果是->: {self.setup.nick_error_hint()}")
        else:
            self.assertEqual(self.setup.nick_setup_success_hint(), testdata['check'][0],
                             f"返回实际结果是->: {self.setup.nick_setup_success_hint()}")
            self.assertEqual(self.setup.sign_setup_success_hint(), testdata['check'][1],
                             f"返回实际结果是->: {self.setup.sign_setup_success_hint()}")
        self.login.save_web_img(testdata['screenshot'])
        self.login.user_login_exit()
