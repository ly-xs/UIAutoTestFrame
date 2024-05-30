import configparser
import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from selenium.common.exceptions import NoSuchElementException, NoSuchFrameException, NoAlertPresentException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from common.logger import Logger
from config.config import CONFIG_FILE, REPORT_DIR
from selenium.webdriver import ActionChains

logger = Logger().get_logger(__name__)
# 读取config.ini配置文件
config = configparser.ConfigParser()
config.read(CONFIG_FILE, encoding="utf-8")
home_url = config.get("WebURL", "URL")
screenshot_path = REPORT_DIR + r"\screenshot"
if not os.path.exists(screenshot_path):
    os.makedirs(screenshot_path)


class BasePage:
    """
    基础类，对selenium的二次开发，用于页面对象类的继承
    """

    def __init__(self, driver, base_url=home_url):
        self.driver = driver
        self.base_url = base_url

    def open(self, url):
        """
        打开浏览器URL访问
        :return:
        """
        url = self.base_url + url
        self.driver.get(url)
        logger.info(f"进入{url}页面")
        assert url == self.driver.current_url, f"没有进入这个页面 {url}"

    def locator(self, loc, lists=False):
        """
        单个元素定位
        :param loc: 传入元素属性
        :param lists: 是否返回元素列表
        :return: 定位到的元素
        """
        try:
            WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located(loc))
            return self.driver.find_element(*loc) if lists is False else self.driver.find_elements(*loc)
        except TimeoutError:
            logger.error(f"{self}页面加载超时")
        except Exception as e:
            logger.error(f"{self}页面中未能找到{loc}元素{e}")

    def script(self, src):
        """
        提供调用JavaScript方法
        :param src: 脚本文件
        :return: JavaScript脚本
        """
        try:
            return self.driver.execute_script(src)
        except Exception as e:
            logger.error(f"{self}页面中未能执行{src}脚本！{e}")

    # 重写定义send_keys方法
    def send_key(self, loc, value, clear_first=True):
        try:
            if clear_first:
                self.locator(loc).clear()
                logger.info(f"清空{loc}元素")
                self.locator(loc).send_keys(value)
                logger.info(f"在{loc}元素输入{value}")
        except AttributeError:
            logger.error(f"{self}页面中无法输入{value}")

    def switch_frame(self, loc):
        """
        多表单嵌套切换
        :param loc: 传元素的属性值
        :return: 定位到的元素
        """
        try:
            return self.driver.switch_to.frame(loc)
        except NoSuchFrameException:
            logger.error(f"{self}页面中未能切换到{loc}frame")

    def switch_window(self, loc):
        """
        多窗口切换
        :param loc:
        :return:
        """
        try:
            return self.driver.switch_to.window(loc)
        except Exception as e:
            logger.error(f"{self}页面中未能找到{e}窗口")

    def switch_alert(self):
        """
        警告框处理
        :return:
        """
        try:
            return self.driver.switch_to.alert()
        except NoAlertPresentException as msg:
            logger.error(f"{self}页面中未能找到{msg}警告窗")

    def click(self, loc) -> None:
        try:
            self.locator(loc).click()
            logger.info(f"点击{loc}元素")
        except NoSuchElementException:
            logger.error(f"{self}页面中未能找到{loc}元素")

    @staticmethod
    def sleep(seconds) -> None:
        time.sleep(seconds)
        logger.info(f"等待{seconds}秒")

    # 隐式等待
    def wait(self, seconds):
        self.driver.implicitly_wait(seconds)
        logger.info(f"隐式等待{seconds}秒")

    # 等待元素可见
    def wait_eleVisible(self, loc, timeout=10, poll_frequency=0.5, model=None):
        """
        :param loc:元素定位表达;元组类型,表达方式(元素定位类型,元素定位方法)
        :param timeout:等待的上限
        :param poll_frequency:轮询频率
        :param model:等待失败时,截图操作,图片文件中需要表达的功能标注
        :return:None
        """
        try:
            start = time.time()
            WebDriverWait(self.driver, timeout, poll_frequency).until(
                expected_conditions.visibility_of_element_located(loc))
            end = time.time()
            logger.info(f'等待时长:{end - start}秒')
            logger.info(f'{model} 等待元素可见:{loc}')
        except Exception as e:
            self.save_web_img(model)
            logger.error(f'{model} 等待元素可见失败:{loc}！{e}')

    # 悬停
    def hover(self, loc):
        ActionChains(self.driver).move_to_element(self.locator(loc)).perform()
        logger.info(f"在{loc}元素悬停")

    # 浏览器前进操作
    def forward(self):
        self.driver.forward()
        logger.info("前进一个页面")

    # 浏览器后退操作
    def back(self):
        self.driver.back()
        logger.info("后退一个页面")

    # 截图
    def save_web_img(self, file_name):

        # 保留12张截图，login运行两次的数量
        log_files = sorted(
            (os.path.join(screenshot_path, f) for f in os.listdir(screenshot_path) if f.endswith('.png')),
            key=os.path.getmtime
        )
        while len(log_files) > 11:
            os.remove(log_files.pop(0))

        # filepath = 指图片保存目录/model(页面功能名称)_当前时间到秒.png
        # 当前时间
        dateNow = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        # 路径
        filePath = fr'{screenshot_path}\{file_name}_{dateNow}.png'
        try:
            self.driver.save_screenshot(filePath)
            logger.info(f'截屏成功,图片路径为{filePath}')
        except Exception as e:
            logger.error(f'截屏失败!{e}')

    # 点击关闭当前窗口
    def close(self):
        try:
            self.driver.close()
            logger.info("关闭窗口")
        except NameError as e:
            logger.error(f"关闭窗口失败！{e}")

    def quit(self):
        self.driver.quit()
        logger.info("关闭浏览器")
