import os
import sys
import yaml

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from common.logger import Logger

logger = Logger().get_logger(__name__)


class GetYaml:
    def __init__(self, filepath):
        self.path = filepath

    def get_yaml(self):
        """
        加载yaml文件数据
        :return:返回数据
        """
        try:
            with open(self.path, encoding="utf-8") as file:
                data = yaml.load(file, Loader=yaml.SafeLoader)
            return data
        except Exception as msg:
            logger.error(f"yaml文件获取数据异常{msg}")

    def get_element_info(self, i):
        """
        获取testcase项的element_info元素
        :param i: 位置序列号
        :return: 返回element_info元素数据
        """
        return self.get_yaml()['testcase'][i]['element_info']

    def get_find_type(self, i):
        """
        获取testcase项的find_type元素数据
        :param i: 位置序列号
        :return: 返回find_type元素数据
        """
        return self.get_yaml()['testcase'][i]['find_type']

    def get_operate_type(self, i):
        """
        获取testcase项的operate_type元素数据
        :param i: 位置序列号
        :return: 返回operate_type元素数据
        """
        return self.get_yaml()['testcase'][i]['operate_type']

    def get_check_element_info(self, i):
        """
        获取check项的element_info元素
        :param i: 位置序列号
        :return: 返回element_info元素数据
        """
        return self.get_yaml()['check'][i]['element_info']

    def get_check_find_type(self, i):
        """
        获取check项的find_type元素
        :param i: 位置序列号
        :return: 返回find_type元素数据
        """
        return self.get_yaml()['check'][i]['find_type']

    def get_check_operate_type(self, i):
        """
        获取check项的operate_type
        :param i: 位置序列号
        :return: 返回operate_type元素数据
        """
        return self.get_yaml()['check'][i]['operate_type']

    def get_test_info_url(self):
        """
        获取testinfo项的url
        :return: 返回url元素数据
        """
        return self.get_yaml()['testinfo'][0]['url']
