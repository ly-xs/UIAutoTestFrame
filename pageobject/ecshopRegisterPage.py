from selenium.webdriver.support.select import Select

from public.basePage import BasePage
from public.logger import Logger

logger = Logger(logger="RegisterPage").getlog()


class RegisterPage(BasePage):
	# 页面元素定位器
	# 用户名
	user_input = 'name=>username'
	# email
	email_input = 'name=>email'
	# 密码
	pass1_input = 'name=>password'
	# 确认密码
	pass2_input = 'name=>confirm_password'
	# MSN
	msn_input = 'name=>extend_field1'
	# QQ
	qq_input = 'name=>extend_field2'
	# 办公电话
	officeTel_input = 'name=>extend_field3'
	# 家庭电话
	homeTel_input = 'name=>extend_field4'
	# 手机
	mobile_input = 'name=>extend_field5'
	# 密码提示问题
	prompt_select = 'name=>sel_question'
	# 密码问题答案
	answer_input = 'name=>passwd_answer'
	# 我已看过并接受协议
	# read_checkbox = (By.NAME,'')
	# 立即注册
	submit_button = 'name=>Submit'

	# 执行注册页面操作
	logger.info('执行注册操作')

	def reg(self, user, email, pass1, pass2, msn, qq, officetel, hometel, mobile, prompt='我最好朋友的生日？', answer='1111'):
		# 输入用户名
		self.find_element(self.user_input).send_keys(user)
		# 输入email
		self.find_element(self.email_input).send_keys(email)
		# 输入密码
		self.find_element(self.pass1_input).send_keys(pass1)
		# 确认密码
		self.find_element(self.pass2_input).send_keys(pass2)
		# 输入MSN
		self.find_element(self.msn_input).send_keys(msn)
		# 输入QQ
		self.find_element(self).send_keys(qq)
		# 输入办公电话
		self.find_element(self.officeTel_input).send_keys(officetel)
		# 输入家庭电话
		self.find_element(self.homeTel_input).send_keys(hometel)
		# 输入手机
		self.find_element(self.mobile_input).send_keys(mobile)
		# 选择密码提示问题
		Select(self.find_element(self.prompt_select)).select_by_visible_text(prompt)
		# 输入密码问题答案
		self.find_element(self.answer_input).send_keys(answer)

		# 点击 立即注册
		self.find_element(self.submit_button).click()
