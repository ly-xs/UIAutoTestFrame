import datetime
import os.path
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from common.logger import Logger

# create a logger instance
logger = Logger(logger="BasePage").getlog()


class BasePage(object):
    """
	定义一个页面基类，让所有页面都继承这个类，封装一些常用的页面操作方法到这个类
	"""

    def __init__(self, driver):
        self.driver = driver

    # quit browser and end testing
    def quit_browser(self):
        self.driver.quit()

    # 浏览器前进操作
    def forward(self):
        self.driver.forward()
        logger.info("Click forward on current page.")

    # 浏览器后退操作
    def back(self):
        self.driver.back()
        logger.info("Click back on current page.")

    # 隐式等待
    def wait(self, seconds):
        self.driver.implicitly_wait(seconds)
        logger.info("wait for %d seconds." % seconds)

    # 点击关闭当前窗口
    def close(self):
        try:
            self.driver.close()
            logger.info("Closing and quit the browser.")
        except NameError as e:
            logger.error("Failed to quit the browser with %s" % e)

    # 保存图片
    def get_windows_img(self):
        """
		在这里我们把file_path这个参数写死，直接保存到我们项目根目录的一个文件夹.\Screenshots下
		"""
        file_path = os.path.dirname(os.path.abspath('../pageobject')) + '/screenshots/'
        rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        screen_name = file_path + rq + '.png'
        try:
            self.driver.get_screenshot_as_file(screen_name)

            logger.info("Had take screenshot and save to folder : /screenshots")
        except NameError as e:
            logger.error("Failed to take screenshot! %s" % e)
            self.get_windows_img()

    # 定位元素方法
    def find_element(self, selector):
        """
		 这个地方为什么是根据=>来切割字符串，请看页面里定位元素的方法
		 submit_btn = "id=>su"
		 login_lnk = "xpath => //*[@id='u1']/a[7]"  # 百度首页登录链接定位
		 如果采用等号，结果很多xpath表达式中包含一个=，这样会造成切割不准确，影响元素定位
		:param selector:
		:return: element
		"""
        element = ''
        if '=>' not in selector:
            return self.driver.find_element_by_id(selector)
        selector_by = selector.split('=>')[0]
        selector_value = selector.split('=>')[1]

        if selector_by == "i" or selector_by == 'id':
            try:
                element = self.driver.find_element_by_id(selector_value)
                logger.info("Had find the element \' %s \' successful "
                            "by %s via value: %s " % (
                                (element.value if element.text else element.tag_name), selector_by, selector_value))
            except NoSuchElementException as e:
                logger.error("NoSuchElementException: %s" % e)
                self.get_windows_img()  # take screenshot
        elif selector_by == "n" or selector_by == 'name':
            element = self.driver.find_element_by_name(selector_value)
        elif selector_by == "c" or selector_by == 'class_name':
            element = self.driver.find_element_by_class_name(selector_value)
        elif selector_by == "l" or selector_by == 'link_text':
            element = self.driver.find_element_by_link_text(selector_value)
        elif selector_by == "p" or selector_by == 'partial_link_text':
            element = self.driver.find_element_by_partial_link_text(selector_value)
        elif selector_by == "t" or selector_by == 'tag_name':
            element = self.driver.find_element_by_tag_name(selector_value)
        elif selector_by == "x" or selector_by == 'xpath':
            try:
                element = self.driver.find_element_by_xpath(selector_value)
                logger.info("Had find the element \' %s \' successful "
                            "by %s via value: %s " % (
                                (element.value if element.text else element.tag_name), selector_by, selector_value))
            except NoSuchElementException as e:
                logger.error("NoSuchElementException: %s" % e)
                self.get_windows_img()
        elif selector_by == "s" or selector_by == 'selector_selector':
            element = self.driver.find_element_by_css_selector(selector_value)
        else:
            raise NameError("Please enter a valid type of targeting elements.")

        return element

    # 输入
    def type(self, selector, text):

        el = self.find_element(selector)
        el.clear()
        try:
            el.send_keys(text)
            logger.info("Had type \' %s \' in inputBox" % text)
        except NameError as e:
            logger.error("Failed to type in input box with %s" % e)
            self.get_windows_img()

    # 清除文本框
    def clear(self, selector):

        el = self.find_element(selector)
        try:
            el.clear()
            logger.info("Clear text in input box before typing.")
        except NameError as e:
            logger.error("Failed to clear in input box with %s" % e)
            self.get_windows_img()

    # 点击元素
    def click(self, selector):

        el = self.find_element(selector)
        try:
            el.click()
            logger.info("The element \' %s \' was clicked." % (el.value if el.text else el.tag_name))
        except NameError as e:
            logger.error("Failed to click the element with %s" % e)

    # 或者网页标题
    def get_page_title(self):
        logger.info("Current page title is %s" % self.driver.title)
        return self.driver.title

    @staticmethod
    def sleep(seconds):
        time.sleep(seconds)
        logger.info("Sleep for %d seconds" % seconds)

    # 等待元素可见
    def wait_eleVisible(self, loc, timeout=20, poll_frequency=0.5, model=None):
        """
		:param loc:元素定位表达;元组类型,表达方式(元素定位类型,元素定位方法)
		:param timeout:等待的上限
		:param poll_frequency:轮询频率
		:param model:等待失败时,截图操作,图片文件中需要表达的功能标注
		:return:None
		"""
        logger.info('{} 等待元素可见:{}'.format(model, loc))
        try:
            start = time.time()
            WebDriverWait(self.driver, timeout, poll_frequency).until(EC.visibility_of_element_located(loc))
            end = time.time()
            logger.info('等待时长:%.2f 秒' % (end - start))
        except:
            logger.exception('{} 等待元素可见失败:{}'.format(model, loc))
            # 截图
            self.save_webImgs(model)
            raise

    # 等待元素不可见
    def wait_eleNoVisible(self, loc, timeout=20, poll_frequency=0.5, model=None):
        """
		:param loc:元素定位表达;元组类型,表达方式(元素定位类型,元素定位方法)
		:param timeout:等待的上限
		:param poll_frequency:轮询频率
		:param model:等待失败时,截图操作,图片文件中需要表达的功能标注
		:return:None
		"""
        logger.info('{} 等待元素不可见:{}'.format(model, loc))
        try:
            start = time.time()
            WebDriverWait(self.driver, timeout, poll_frequency).until_not(EC.visibility_of_element_located(loc))
            end = time.time()
            logger.info('等待时长:%.2f 秒' % (end - start))
        except:
            logger.exception('{} 等待元素不可见失败:{}'.format(model, loc))
            # 截图
            self.save_webImgs(model)
            raise

    # 查找一个元素element
    def find_Element(self, loc, model=None):
        logger.info('{} 查找元素 {}'.format(model, loc))
        try:
            return self.driver.find_element(*loc)
        except:
            logger.exception('查找元素失败.')
            # 截图
            self.save_webImgs(model)
            raise

    # 查找元素elements
    def find_Elements(self, loc, model=None):
        logger.info('{} 查找元素 {}'.format(model, loc))
        try:
            return self.driver.find_element(*loc)
        except:
            logger.exception('查找元素失败.')
            # 截图
            self.save_webImgs(model)
            raise

    # 输入操作
    def input_Text(self, loc, text, model=None):
        # 查找元素
        ele = self.find_Element(loc, model)
        # 输入操作
        logger.info('{} 在元素 {} 中输入文本: {}'.format(model, loc, text))
        try:
            ele.send_keys(text)
        except:
            logger.exception('输入操作失败')
            # 截图
            self.save_webImgs(model)
            raise

    # 清除操作
    def clean_Input_Text(self, loc, model=None):
        ele = self.find_Element(loc, model)
        # 清除操作
        logger.info('{} 在元素 {} 中清除'.format(model, loc))
        try:
            ele.clear()
        except:
            logger.exception('清除操作失败')
            # 截图
            self.save_webImgs(model)
            raise

    # 点击操作
    def click_Element(self, loc, model=None):
        # 先查找元素在点击
        ele = self.find_Element(loc, model)
        # 点击操作
        logger.info('{} 在元素 {} 中点击'.format(model, loc))
        try:
            ele.click()
        except:
            logger.exception('点击操作失败')
            # 截图
            self.save_webImgs(model)
            raise

    # 获取文本内容
    def get_Text(self, loc, model=None):
        # 先查找元素在获取文本内容
        ele = self.find_Element(loc, model)
        # 获取文本
        logger.info('{} 在元素 {} 中获取文本'.format(model, loc))
        try:
            text = ele.text
            logger.info('{} 元素 {} 的文本内容为 {}'.format(model, loc, text))
            return text
        except:
            logger.exception('获取元素 {} 的文本内容失败,报错信息如下:'.format(loc))
            # 截图
            self.save_webImgs(model)
            raise

    # 获取属性值
    def get_Element_Attribute(self, loc, model=None):
        # 先查找元素在去获取属性值
        ele = self.find_Element(loc, model)
        # 获取元素属性值
        logger.info('{} 在元素 {} 中获取属性值'.format(model, loc))
        try:
            ele_attribute = ele.get_attribute()
            logger.info('{} 元素 {} 的文本内容为 {}'.format(model, loc, ele_attribute))
            return ele_attribute
        except:
            logger.exception('获取元素 {} 的属性值失败,报错信息如下:'.format(loc))
            self.save_webImgs(model)
            raise

    # iframe 切换
    def switch_iframe(self, frame_refer, timeout=20, poll_frequency=0.5, model=None):
        # 等待 iframe 存在
        logger.info('iframe 切换操作:')
        try:
            # 切换 == index\name\id\WebElement
            WebDriverWait(self.driver, timeout, poll_frequency).until(
                EC.frame_to_be_available_and_switch_to_it(frame_refer))
            time.sleep(0.5)
            logger.info('切换成功')
        except:
            logger.exception('iframe 切换失败!!!')
            # 截图
            self.save_webImgs(model)
            raise

    # 窗口切换 = 如果是切换到新窗口,new. 如果是回到默认的窗口,default
    def switch_window(self, name, cur_handles=None, timeout=20, poll_frequency=0.5, model=None):
        """
		调用之前要获取window_handles
		:param name: new 代表最新打开的一个窗口. default 代表第一个窗口. 其他的值表示为窗口的 handles
		:param cur_handles:
		:param timeout:等待的上限
		:param poll_frequency:轮询频率
		:param model:等待失败时,截图操作,图片文件中需要表达的功能标注
		:return:
		"""
        try:
            if name == 'new':
                if cur_handles is not None:
                    logger.info('切换到最新打开的窗口')
                    WebDriverWait(self.driver, timeout, poll_frequency).until(EC.new_window_is_opened(cur_handles))
                    window_handles = self.driver.window_handles
                    self.driver.swich_to.window(window_handles[-1])
                else:
                    logger.exception('切换失败,没有要切换窗口的信息!!!')
                    self.save_webImgs(model)
                    raise
            elif name == 'default':
                logger.info('切换到默认页面')
                self.driver.switch_to.default()
            else:
                logger.info('切换到为 handles 的窗口')
                self.driver.swich_to.window(name)
        except:
            logger.exception('切换窗口失败!!!')
            # 截图
            self.save_webImgs(model)
            raise

    # 截图
    def save_webImgs(self, model=None):
        # filepath = 指图片保存目录/model(页面功能名称)_当前时间到秒.png
        # 当前时间
        dateNow = str(datetime.datetime.now()).split('.')[0]
        # 路径
        filePath = '{}/{}_{}.png'.format(r'..\screenshot', model, dateNow)
        try:
            self.driver.save_screenshot(filePath)
            logger.info('截屏成功,图片路径为{}'.format(filePath))
        except:
            logger.exception('截屏失败!')
