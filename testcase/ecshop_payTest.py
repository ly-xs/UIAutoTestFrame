import time
import unittest

from selenium import webdriver

# 导入 购物页面类
from pageobject.cartPage import CartPage
# 导入 商品详情页面类
from pageobject.goodsDetailPage import GoodsDetailPage
# 导入 登录页面类
from pageobject.loginPage import LoginPage


# 定义测试类
class EcshopGoodsPay(unittest.TestCase):
	#
	def setUp(self) -> None:
		self.driver = webdriver.Chrome()
		self.driver.maximize_window()
		self.url = 'http://192.168.126.134/ecshop/upload/user.php'
		self.driver.get(self.url)
		# 登录
		lp = LoginPage(self.driver)
		lp.login('ecshop', 'ecshop')

	# def tearDown(self) -> None:
	#     self.driver.quit()

	# 测试用例
	def test_goods_pay(self):
		goods_ids = ['19', '21']
		# 添加商品到购物车
		for ID in goods_ids:
			self.url = 'http://192.168.126.134/ecshop/upload/goods.php?id=' + ID
			gdp = GoodsDetailPage(self.driver)
			self.driver.get(self.url)
			gdp.cart_add()
			time.sleep(5)
		# 点击结算中心
		cp = CartPage(self.driver)
		cp.goods_pay()


if __name__ == '__main__':
	unittest.main()
