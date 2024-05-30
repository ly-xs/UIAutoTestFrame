import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from testcase.baseTestcase import BaseTestCase
from common.getYaml import GetYaml
from ddt import ddt, data
from config.config import TEST_DATA_DIR
from common.logger import Logger
from pageobject.loginPage import login

logger = Logger().get_logger(__name__)


@ddt
class LoginTestCase(BaseTestCase):
    """
    抽屉新热榜登录测试
    """
    def setUp(self):
        self.login = login(self.driver)

    def tearDown(self):
        pass

    @data(*GetYaml(TEST_DATA_DIR + r"\login_data.yaml").get_yaml())
    def test_login(self, datayaml):
        """
        登录测试
        :param datayaml: 加载login_data登录测试数据
        :return:
        """
        logger.info(f"当前执行测试用例ID-> {datayaml['id']}; 测试点-> {datayaml['detail']}")
        # 调用登录方法
        self.login.user_login(datayaml['data']['phone'], datayaml['data']['password'])
        if datayaml['screenshot'] == 'phone_pwd_success':
            self.assertEqual(self.login.user_login_success_hint(), datayaml['check'][0],
                             f"成功登录，返回实际结果是->: {self.login.user_login_success_hint()}")
            self.login.save_web_img(datayaml['screenshot'])
            self.login.login_exit()
            self.assertEqual(self.login.exit_login_success_hint(), datayaml['check'][1],
                             f"退出登录，返回实际结果是->: {self.login.exit_login_success_hint()}")
        else:
            self.login.save_web_img(datayaml['screenshot'])
            self.assertEqual(self.login.phone_pwd_error_hint(), datayaml['check'][0],
                             f"异常登录，返回实际结果是->: {self.login.phone_pwd_error_hint()}")
