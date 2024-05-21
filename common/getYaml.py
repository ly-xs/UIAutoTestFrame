import os
import sys
import yaml

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from common.logger import Logger

logger = Logger(logger="GetYaml")


class GetYaml:
    def __init__(self, filepath):
        self.path = filepath

    def get_yaml(self):
        """
        加载yaml文件数据
        :return:返回数据
        """
        try:
            with open(self.path, encoding="utf-8") as f:
                data = yaml.full_load(f)
            return data
        except Exception as msg:
            logger.error(f"yaml文件获取数据异常{msg}")

    def alldata(self):
        """
        读取yaml文件数据
        :return: 返回数据
        """
        data = self.get_yaml()
        return data

    def case_len(self):
        """
        testcase字典长度
        :return: 字典长度大小
        """
        data = self.alldata()
        length = len(data['testcase'])
        return length

    def check_len(self):
        """
        check字典长度
        :return: 字典长度大小
        """
        data = self.alldata()
        length = len(data['check'])
        return length

    def get_element_info(self, i):
        """
        获取testcase项的element_info元素
        :param i: 位置序列号
        :return: 返回element_info元素数据
        """
        data = self.alldata()
        return data['testcase'][i]['element_info']

    def get_find_type(self, i):
        """
        获取testcase项的find_type元素数据
        :param i: 位置序列号
        :return: 返回find_type元素数据
        """
        data = self.alldata()
        return data['testcase'][i]['find_type']

    def get_operate_type(self, i):
        """
        获取testcase项的operate_type元素数据
        :param i: 位置序列号
        :return: 返回operate_type元素数据
        """
        data = self.alldata()
        return data['testcase'][i]['operate_type']

    def get_check_element_info(self, i):
        """
        获取check项的element_info元素
        :param i: 位置序列号
        :return: 返回element_info元素数据
        """
        data = self.alldata()
        return data['check'][i]['element_info']

    def get_check_find_type(self, i):
        """
        获取check项的find_type元素
        :param i: 位置序列号
        :return: 返回find_type元素数据
        """
        data = self.alldata()
        return data['check'][i]['find_type']

    def get_check_operate_type(self, i):
        """
        获取check项的operate_type
        :param i: 位置序列号
        :return: 返回operate_type元素数据
        """
        data = self.alldata()
        return data['check'][i]['operate_type']

    def get_test_info_url(self):
        """
        获取testinfo项的url
        :return: 返回url元素数据
        """
        data = self.alldata()
        return data['testinfo'][0]['url']
