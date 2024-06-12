import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from common.getYaml import GetYaml
from config.config import PAGE_DATA_DIR
from pageobject.basePage import BasePage

# 获取页面元素
pageData = GetYaml(PAGE_DATA_DIR + r"\login_element.yaml")


class login(BasePage):
    """
    用户登录页面
    """
    # login页面路径
    url = pageData.get_test_info_url()

    # 定位器，通过元素属性定位元素对象
    # 打开登录对话框
    dig_login_button = (pageData.get_find_type(0), pageData.get_element_info(0))
    # 手机号输入框
    login_phone = (pageData.get_find_type(1), pageData.get_element_info(1))
    # 密码输入框
    login_password = (pageData.get_find_type(2), pageData.get_element_info(2))
    # 取消自动登录
    keep_login_button = (pageData.get_find_type(3), pageData.get_element_info(3))
    # 单击登录
    login_user = (pageData.get_find_type(4), pageData.get_element_info(4))
    # 退出登录
    login_exit = (pageData.get_find_type(5), pageData.get_element_info(5))
    # 选择退出
    login_exit_button = (pageData.get_find_type(6), pageData.get_element_info(6))

    def user_login_exit(self):
        """
        退出系统
        :return:
        """
        self.hover(self.login_exit)
        self.click(self.login_exit_button)

    def user_login(self, phone, password):
        """
        登录入口
        :param phone: 手机号码
        :param password: 密码
        :return:
        """
        self.open(self.url)
        self.click(self.dig_login_button)
        self.send_key(self.login_phone, phone)
        self.send_key(self.login_password, password)
        self.click(self.keep_login_button)
        self.click(self.login_user)

    phone_pwd_error_hint = (pageData.get_check_find_type(0), pageData.get_check_element_info(0))
    user_login_hover = (pageData.get_check_find_type(1), pageData.get_check_element_info(1))
    user_login_success = (pageData.get_check_find_type(2), pageData.get_check_element_info(2))
    exit_login_success = (pageData.get_check_find_type(3), pageData.get_check_element_info(3))

    def user_login_error_hint(self):
        """
        获取登录失败提示
        :return: 登录失败提示
        """
        return self.find_element(self.phone_pwd_error_hint).text

    def user_login_success_hint(self):
        """
        获取登录成功提示
        :return: 登录成功提示
        """
        self.hover(self.user_login_hover)
        return self.find_element(self.user_login_success).text

    def exit_login_success_hint(self):
        """
        获取退出登录成功提示
        :return: 退出登录成功提示
        """
        return self.find_element(self.exit_login_success).text
