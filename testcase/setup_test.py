import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from common.getYaml import GetYaml
from common.logger import Logger
from config.config import TEST_DATA_DIR
from pageobject.setupPage import setup
from ddt import ddt, data
from pageobject.loginPage import login
from testcase.baseTestcase import BaseTestCase

LoginData = GetYaml(TEST_DATA_DIR + r"\login_data.yaml").get_yaml()
phone = LoginData[5]['data']['phone']
password = LoginData[5]['data']['password']
logger = Logger(name="SetupTestCase").get_logger()


@ddt
class SetupTestCase(BaseTestCase):
    """
    首页---设置
    """
    def setUp(self):
        self.login = login(self.driver)
        self.setup = setup(self.driver)

    def tearDown(self):
        pass

    @data(*GetYaml(TEST_DATA_DIR + r"\setup_data.yaml").get_yaml())
    def test_setup(self, datayaml):
        """
        首页---设置操作测试
        :param datayaml: 加载login_data登录测试数据
        :return:
        """
        logger.info(f"当前执行测试用例ID-> {datayaml['id']}; 测试点-> {datayaml['detail']}")

        # 调用登录方法
        self.login.user_login(phone, password)

        # 调用设置接口
        self.setup.dig_setup(datayaml['data']['name'], datayaml['data']['sign'])
        if datayaml['screenshot'] == 'name_empty':
            self.assertEqual(self.setup.nick_error_hint(), datayaml['check'][0],
                             f"返回实际结果是->: {self.setup.nick_error_hint()}")
        else:
            self.assertEqual(self.setup.nick_setup_success_hint(), datayaml['check'][0],
                             f"返回实际结果是->: {self.setup.nick_setup_success_hint()}")
            self.assertEqual(self.setup.sign_setup_success_hint(), datayaml['check'][1],
                             f"返回实际结果是->: {self.setup.sign_setup_success_hint()}")
        self.login.save_web_img(datayaml['screenshot'])
        self.login.login_exit()
