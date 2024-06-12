import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from pageobject.basePage import BasePage
from common.getYaml import GetYaml
from config.config import PAGE_DATA_DIR

pageData = GetYaml(PAGE_DATA_DIR + r"\setup_element.yaml")


class setup(BasePage):
    """
    首页---设置页面
    """
    url = pageData.get_test_info_url()

    # 定位器，通过元素属性定位元素对象
    # 鼠标悬停控件
    userProNick_loc = (pageData.get_find_type(0), pageData.get_element_info(0))
    # 菜单设置元素
    text_setup_loc = (pageData.get_find_type(1), pageData.get_element_info(1))
    # 点击编辑按钮
    edit_btn_loc = (pageData.get_find_type(2), pageData.get_element_info(2))
    # 昵称文本框元素
    nick_loc = (pageData.get_find_type(3), pageData.get_element_info(3))
    # 签名语言本框元素
    user_sign_loc = (pageData.get_find_type(4), pageData.get_element_info(4))
    # 保存按钮元素
    save_btn_loc = (pageData.get_find_type(5), pageData.get_element_info(5))

    def dig_setup(self, *data):
        """
        设置操作
        :param data:
        :return:
        """
        # 选择菜单-> 设置
        self.hover(self.userProNick_loc)
        self.click(self.text_setup_loc)
        # 点击编辑按钮
        self.click(self.edit_btn_loc)
        # 清空昵称文本框并录入数据
        self.send_key(self.nick_loc, data[0])
        # 清空签名文本框并录入数据
        self.send_key(self.user_sign_loc, data[1])
        # 单击保存
        self.click(self.save_btn_loc)

    nick_error_loc = (pageData.get_check_find_type(0), pageData.get_check_element_info(0))
    nick_setup_success_loc = (pageData.get_check_find_type(1), pageData.get_check_element_info(1))
    sign_setup_success_loc = (pageData.get_check_find_type(2), pageData.get_check_element_info(2))

    def nick_error_hint(self):
        return self.find_element(self.nick_error_loc).text

    def nick_setup_success_hint(self):
        return self.find_element(self.nick_setup_success_loc).text

    def sign_setup_success_hint(self):
        return self.find_element(self.sign_setup_success_loc).text
