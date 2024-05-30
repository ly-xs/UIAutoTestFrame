import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from common.logger import Logger
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

logger = Logger().get_logger(__name__)


def create_driver(browser='chrome'):
    grid_url = 'http://localhost:4444/wd/hub'

    if browser == 'chrome':
        options = ChromeOptions()
    elif browser == 'edge':
        options = EdgeOptions()
    else:
        logger.error("驱动异常")
        raise ValueError(f"Unsupported browser: {browser}")

    driver = webdriver.Remote(
        command_executor=grid_url,
        options=options
    )

    return driver
