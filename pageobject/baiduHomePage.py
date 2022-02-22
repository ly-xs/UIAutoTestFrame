from common.basePage import BasePage


class BaiduPage(BasePage):
	input = "id=>kw"
	button = "id=>su"

	def get_input(self):
		return self.find_element(BaiduPage.input)

	def get_button(self):
		return self.find_element(BaiduPage.button)

	def search(self, keyword) -> None:
		self.get_input().send_keys(keyword)
		self.get_button().click()
