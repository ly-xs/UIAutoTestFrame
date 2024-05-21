import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


def new_report(testreport):
    """
    生成最新的测试报告文件
    :param testreport:
    :return:返回文件
    """
    lists = os.listdir(testreport)
    lists.sort(key=lambda fn: os.path.getmtime(testreport + "\\" + fn))
    file_new = os.path.join(testreport, lists[-1])
    return file_new
