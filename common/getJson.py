import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from common.logger import Logger

logger = Logger(name="GetJson").get_logger()


class GetJson:
    def __init__(self, filepath):
        self.path = filepath

    def get_json(self):
        """
        加载json文件数据
        :return: 返回数据
        """
        try:
            with open(self.path, encoding="utf-8") as f:
                data = json.load(f)
                return list(data)
        except Exception as msg:
            logger.error(f"json文件获取数据异常{msg}")

