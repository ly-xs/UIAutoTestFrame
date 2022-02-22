import time
import unittest
from selenium import webdriver
# 导入 商品新增页面
from pageobject.backGoodsAddPage import BackGoodsAddPage
# 导入 后台登录页面
from pageobject.backLoginPage import BackLoginPage
# 导入 后台主页面
from pageobject.backMainPage import BackMainPage


# 定义测试类
class EcshopGoodsPay(unittest.TestCase):

	def setUp(self) -> None:
		self.driver = webdriver.Edge()
		self.driver.maximize_window()
		self.url = 'http://192.168.35.128/ecshop/upload/admin/index.php'
		self.driver.get(self.url)
		# 登录
		lp = BackLoginPage(self.driver)
		lp.backLogin('admin', 'admin123')

	def tearDown(self) -> None:
		self.driver.quit()

	# 测试用例
	def test_goods_add(self):
		# 添加商品到购物车
		# 切换frame
		bmp = BackMainPage(self.driver)
		self.driver.switch_to.frame('menu-frame')
		time.sleep(2)

		# 点击 添加商品链接
		bmp.click_goods_add()
		time.sleep(2)

		# 切换frame
		self.driver.switch_to.default_content()
		self.driver.switch_to.frame('main-frame')
		time.sleep(2)

		# 新增商品
		bgap = BackGoodsAddPage(self.driver)
		bgap.add_good('8888')


if __name__ == '__main__':
	unittest.main()
