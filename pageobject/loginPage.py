from common.basePage import BasePage


# 定义class 继承 BasePage类
class LoginPage(BasePage):
	# 定位器  类变量    类名.变量名      self.变量名
	# 用户名
	user_input = 'name=>username'
	# 密码
	pass_input = 'name=>password'
	# 立即登录
	submit_button = 'name=>submit'

	# 注册页面操作
	def login(self, user, pwd):
		# 输入用户名
		self.find_element(self.user_input).send_keys(user)
		# 输入密码
		self.type(self.pass_input, pwd)

		# 提交
		self.find_element(self.submit_button).click()
