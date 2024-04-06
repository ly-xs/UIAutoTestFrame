import unittest
from time import sleep
from ddt import ddt, file_data
from selenium import webdriver
from pageobject.ecshopRegisterPage import RegisterPage


@ddt
class EcshopRegisterTest(unittest.TestCase):
	def setUp(self) -> None:
		self.driver = webdriver.Edge()
		self.driver.maximize_window()
		self.url = 'http://192.168.35.128/ecshop/upload/user.php?act=register'
		self.driver.get(self.url)

	def tearDown(self) -> None:
		self.driver.close()
		self.driver.quit()

	@file_data(r'..\testdata\regpo.json')
	def test_ecshop_reg(self, user, email, pass1, pass2, msn, qq, officetel, hometel, mobile, prompt, answer):
		# 注册
		reg_obj = RegisterPage(self.driver)
		reg_obj.reg(user, email, pass1, pass2, msn, qq, officetel, hometel, mobile, prompt, answer)
		# 断言
		exp_url = 'http://192.168.35.128/ecshop/upload/user.php'
		sleep(5)
		self.assertEqual(exp_url, self.driver.current_url)


if __name__ == '__main__':
	unittest.main()
