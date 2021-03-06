import unittest
import time
from HTMLTestRunner_PY3 import HTMLTestRunner

if __name__ == '__main__':

	# 测试用例存放的目录
	dir_path = '.\\testcase'
	# 测试报告名称中加上格式化时间
	now = time.strftime('%Y-%m-%d %H_%M_%S')
	# 测试报告路径
	report_path = '.\\report' + '\\' + now + 'Result.html'
	# discover()方式加载某路径下的所有测试用例
	discover = unittest.defaultTestLoader.discover(start_dir=dir_path, pattern='baidu*.py', top_level_dir=None)
	# print(discover)

	with open(report_path, 'wb') as f:
		runner = HTMLTestRunner(stream=f, verbosity=2, title='ECshop自动化测试报告', description='用例执行详细信息')
		runner.run(discover)
