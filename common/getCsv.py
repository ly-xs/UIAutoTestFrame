import os
import sys
import csv
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from common.logger import Logger

logger = Logger(name="GetCsv").get_logger()


class GetCsv:
    def __init__(self, filepath):
        self.path = filepath

    def get_csv(self):
        """
        加载csv文件数据
        :return: 返回数据
        """
        try:
            with open(self.path, encoding="utf-8") as f:
                data = csv.reader(f)
                return list(data)
        except Exception as msg:
            logger.error(f"csv文件获取数据异常{msg}")
