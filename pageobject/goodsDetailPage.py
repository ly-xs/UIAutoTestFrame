from selenium.webdriver.common.keys import Keys

from public.basePage import BasePage
from selenium.webdriver.common.by import By
from public.logger import Logger

logger = Logger(logger="GoodsDetailPage").getlog()


class GoodsDetailPage(BasePage):
	# 页面元素定位器
	# 商品数量
	number_input = (By.ID,'number')
	# 加入购物车
	# submit_button = (By.CSS_SELECTOR,"li[class='padd'] > a:nth-child(1)")
	submit_button = "s=>li[class='padd'] > a:nth-child(1)"

	# 添加商品到购物车操作
	logger.info('添加商品到购物车')

	def cart_add(self,goods_num=1):
		self.find_Element(self.number_input).send_keys(Keys.BACKSPACE)
		self.find_Element(self.number_input).send_keys(goods_num)
		self.find_element(self.submit_button).click()
