from common.basePage import BasePage
from selenium.webdriver.common.by import By
from common.logger import Logger

logger = Logger(logger="CartPage").getlog()


class CartPage(BasePage):
	# 页面元素定位器
	# 结算中心
	pay_button = (By.XPATH, "//a[@href='flow.php?step=checkout']")

	# 进行商品结算
	logger.info('进行商品结算')

	def goods_pay(self):
		self.find_Element(self.pay_button).click()