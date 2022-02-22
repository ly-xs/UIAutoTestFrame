import time
import unittest

from ddt import ddt, data
from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from pageobject.baiduHomePage import BaiduPage


@ddt
class BaiduTest(unittest.TestCase):
	def setUp(self) -> None:
		self.driver = webdriver.Edge()
		self.driver.maximize_window()
		self.driver.get("https://www.baidu.com")

	def tearDown(self) -> None:
		self.driver.close()
		self.driver.quit()

	@data('python', 'selenium', 'unittest')
	def test_search_sth(self, keyword):
		WebDriverWait(self.driver, 20).until(expected_conditions.title_contains("百度一下"))
		BaiduPage(self.driver).search(keyword)
		time.sleep(2)


if __name__ == '__main__':
	unittest.main()
