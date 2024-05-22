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
    dig_login_button_loc = (pageData.get_find_type(0), pageData.get_element_info(0))
    # 手机号输入框
    login_phone_loc = (pageData.get_find_type(1), pageData.get_element_info(1))
    # 密码输入框
    login_password_loc = (pageData.get_find_type(2), pageData.get_element_info(2))
    # 取消自动登录
    keep_login_button_loc = (pageData.get_find_type(3), pageData.get_element_info(3))
    # 单击登录
    login_user_loc = (pageData.get_find_type(4), pageData.get_element_info(4))
    # 退出登录
    login_exit_loc = (pageData.get_find_type(5), pageData.get_element_info(5))
    # 选择退出
    login_exit_button_loc = (pageData.get_find_type(6), pageData.get_element_info(6))

    def login_dialog(self):
        """
        打开登录对话框
        :return:
        """
        self.click(self.dig_login_button_loc)

    def login_phone(self, phone):
        """
        登录手机号
        :param phone:手机号码
        :return:
        """
        self.send_key(self.login_phone_loc, phone)

    def login_password(self, password):
        """
        登录密码
        :param password:密码
        :return:
        """
        self.send_key(self.login_password_loc, password)

    def cancel_keep_login(self):
        """
        取消单选自动登录
        :return:
        """
        self.click(self.keep_login_button_loc)

    def login_button(self):
        """
        登录按钮
        :return:
        """
        self.click(self.login_user_loc)

    def login_exit(self):
        """
        退出系统
        :return:
        """
        self.hover(self.login_exit_loc)
        self.click(self.login_exit_button_loc)

    def user_login(self, phone, password):
        """
        登录入口
        :param phone: 手机号码
        :param password: 密码
        :return:
        """
        self.open(self.url)
        self.login_dialog()
        self.sleep(1)
        self.login_phone(phone)
        self.login_password(password)
        self.cancel_keep_login()
        self.login_button()

    phone_pwd_error_hint_loc = (pageData.get_check_find_type(0), pageData.get_check_element_info(0))
    user_login_hover_loc = (pageData.get_check_find_type(1), pageData.get_check_element_info(1))
    user_login_success_loc = (pageData.get_check_find_type(2), pageData.get_check_element_info(2))
    exit_login_success_loc = (pageData.get_check_find_type(3), pageData.get_check_element_info(3))

    # 手机号或密码错误提示
    def phone_pwd_error_hint(self):
        return self.locator(self.phone_pwd_error_hint_loc).text

    # 登录成功用户名
    def user_login_success_hint(self):
        self.hover(self.user_login_hover_loc)
        return self.locator(self.user_login_success_loc).text

    # 退出登录
    def exit_login_success_hint(self):
        return self.locator(self.exit_login_success_loc).text
