import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

from public.basePage import BasePage


# 定义class 继承 BasePage类
class BackGoodsAddPage(BasePage):
	# 定位器  类变量    类名.变量名      self.变量名
	# 输入商品名称
	goods_input = 'name=>goods_name'
	# 选择 商品 类型
	type_select = 'name=>cat_id'
	# 输入 本店售价
	price_input = 'name=>shop_price'

	# 提交
	submit_button = "x=>//input[contains(@value,'确定')]"

	# 点击新增商品
	def add_good(self, price):
		self.find_element(self.goods_input).send_keys('iphone12')
		Select(self.find_element(self.type_select)).select_by_index(2)
		self.find_element(self.price_input).send_keys(Keys.BACKSPACE)
		self.find_element(self.price_input).send_keys(price)

		# 提交
		self.find_element(self.submit_button).click()
		time.sleep(5)

	# def switch_iframe(self):
	#     self.switch_to.frame(self.iframe_loc)
