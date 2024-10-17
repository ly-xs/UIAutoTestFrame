import configparser
import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from selenium.common.exceptions import NoSuchElementException, NoSuchFrameException, NoAlertPresentException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from common.logger import Logger
from config.config import CONFIG_FILE, SCREENSHOTS_DIR
from selenium.webdriver import ActionChains

logger = Logger().get_logger(__name__)
# 读取config.ini配置文件
config = configparser.ConfigParser()
config.read(CONFIG_FILE, encoding="utf-8")
home_url = config.get("WebURL", "URL")


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

    def find_element(self, loc, lists=False, timeout=10):
        """
        单个元素定位
        :param loc: 传入元素属性
        :param lists: 是否返回元素列表
        :param timeout: 等待时间
        :return: 定位到的元素
        """
        try:
            WebDriverWait(self.driver, timeout).until(expected_conditions.visibility_of_element_located(loc))
            return self.driver.find_element(*loc) if not lists else self.driver.find_elements(*loc)
        except TimeoutError:
            logger.error(f"{self}页面加载超时")
        except Exception as e:
            logger.error(f"{self}页面中未能找到{loc}元素{e}")

    def save_web_img(self, file_name) -> None:
        """
        截图保存
        :param file_name: 截图名称
        :return: None
        """
        if not os.path.exists(SCREENSHOTS_DIR):
            os.makedirs(SCREENSHOTS_DIR)

        # 保留12张截图，login运行两次的数量
        log_files = sorted(
            (os.path.join(SCREENSHOTS_DIR, f) for f in os.listdir(SCREENSHOTS_DIR) if f.endswith('.png')),
            key=os.path.getmtime
        )
        while len(log_files) > 11:
            os.remove(log_files.pop(0))

        # filepath = 指图片保存目录/model(页面功能名称)_当前时间到秒.png
        # 当前时间
        dateNow = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        # 路径
        file_path = fr'{SCREENSHOTS_DIR}\{file_name}_{dateNow}.png'
        try:
            self.driver.save_screenshot(file_path)
            logger.info(f'截屏成功,图片路径为{file_path}')
        except Exception as e:
            logger.error(f'截屏失败!{e}')

    def send_key(self, loc, value, clear_first=True):
        try:
            if clear_first:
                self.find_element(loc).clear()
                logger.info(f"清空{loc}元素")
                self.find_element(loc).send_keys(value)
                logger.info(f"在{loc}元素输入{value}")
        except AttributeError:
            logger.error(f"{self}页面中无法输入{value}")

    def click(self, loc) -> None:
        try:
            self.find_element(loc).click()
            logger.info(f"点击{loc}元素")
        except NoSuchElementException:
            logger.error(f"{self}页面中未能找到{loc}元素")

    def script(self, src):
        """
        提供调用JavaScript方法
        :param src: 脚本文件
        :return: JavaScript脚本
        """
        try:
            result = self.driver.execute_script(src)
            logger.info(f"执行{src}脚本")
            return result
        except Exception as e:
            logger.error(f"{self}页面中未能执行{src}脚本！{e}")

    def switch_frame(self, loc):
        """
        多表单嵌套切换
        :param loc: 传元素的属性值
        :return: 定位到的元素
        """
        try:
            result = self.driver.switch_to.frame(loc)
            logger.info(f"切换到{loc}frame")
            return result
        except NoSuchFrameException:
            logger.error(f"{self}页面中未能切换到{loc}frame")

    def switch_window(self, loc):
        """
        多窗口切换
        :param loc:
        :return:
        """
        try:
            result = self.driver.switch_to.window(loc)
            logger.info(f"切换到{loc}窗口")
            return result
        except Exception as e:
            logger.error(f"{self}页面中未能找到{e}窗口")

    def switch_alert(self):
        """
        警告框处理
        :return:
        """
        try:
            result = self.driver.switch_to.alert
            logger.info(f"警告框处理")
            return result
        except NoAlertPresentException as msg:
            logger.error(f"{self}页面中未能找到{msg}警告窗")

    def hover(self, loc):
        """
        鼠标悬停
        :param loc: 元素
        :return: None
        """
        ActionChains(self.driver).move_to_element(self.find_element(loc)).perform()
        logger.info(f"在{loc}元素悬停")

    def forward(self):
        """
        浏览器前进操作
        :return: None
        """
        try:
            self.driver.forward()
            logger.info("前进一个页面")
        except Exception as e:
            logger.error(f"{self}页面中无法前进！{e}")

    def back(self):
        """
        浏览器后退操作
        :return: None
        """
        try:
            self.driver.back()
            logger.info("后退一个页面")
        except Exception as e:
            logger.error(f"{self}页面中无法后退！{e}")

    def implicitly_wait(self, second=10) -> None:
        """
        隐式等待
        :param second: 等待时间
        :return: None
        """
        try:
            self.driver.implicitly_wait(second)
            logger.info(f"隐式等待{second}秒")
        except Exception as e:
            logger.error(f"{self}页面中隐式等待失败！{e}")

    def maximize_window(self) -> None:
        try:
            self.driver.maximize_window()
            logger.info("最大化浏览器")
        except Exception as e:
            logger.error(f"{self}页面中无法最大化浏览器！{e}")

    def close(self):
        try:
            self.driver.close()
            logger.info("关闭窗口")
        except Exception as e:
            logger.error(f"关闭窗口失败！{e}")

    def quit(self):
        try:
            self.driver.quit()
            logger.info("关闭浏览器")
        except Exception as e:
            logger.error(f"关闭浏览器失败！{e}")
