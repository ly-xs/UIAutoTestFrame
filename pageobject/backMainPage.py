from public.basePage import BasePage


# 定义class 继承 BasePage类
class BackMainPage(BasePage):
	# 定位器  类变量    类名.变量名      self.变量名
	# 用户名
	goodsAdd_link = 'l=>添加新商品'
	iframe_loc = 'main-frame'

	# 点击新增商品
	def click_goods_add(self):
		self.find_element(self.goodsAdd_link).click()

	# def switch_iframe(self):
	#     self.switch_to.frame(self.iframe_loc)

