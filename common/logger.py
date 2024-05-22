import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import config
import logging
from logging.handlers import RotatingFileHandler

# 日志存放文件夹，如不存在，则自动创建一个logs目录
if not os.path.exists(config.LOG_DIR):
    os.makedirs(config.LOG_DIR)


class Logger:
    """
    日志记录类
    """
    _instance = None
    _initialized = False
    file_handler = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    def __init__(self, name, level=logging.INFO):
        if not self._initialized:
            self._initialized = True

            # 文件命名
            self.logger = logging.getLogger(name)
            self.logger.setLevel(level)

            # Remove all handlers associated with the logger
            for handler in self.logger.handlers[:]:
                self.logger.removeHandler(handler)

            # Create a console handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(level)

            # Create a formatter and set it for the console handler
            formatter = logging.Formatter('%(asctime)s - %(name)s - line:%(lineno)3d - %(levelname)s: %(message)s')
            console_handler.setFormatter(formatter)

            # Add the console handler to the logger
            self.logger.addHandler(console_handler)

            # Initialize the file handler if it hasn't been done yet
            self.initialize_file_handler(level)

    @classmethod
    def initialize_file_handler(cls, level=logging.INFO):
        """
        Initialize the file handler for logging.
        """
        if cls.file_handler is None:
            # Create a file handler
            logger_name = os.path.join(config.LOG_DIR, f"{time.strftime('%Y-%m-%d %H_%M_%S')}.log")
            cls.file_handler = RotatingFileHandler(logger_name, encoding='utf-8', backupCount=5)
            cls.file_handler.setLevel(level)

            # Create a formatter and set it for the file handler
            formatter = logging.Formatter('%(asctime)s - %(name)s - line:%(lineno)3d - %(levelname)s: %(message)s')
            cls.file_handler.setFormatter(formatter)

            # Add the file handler to the root logger
            root_logger = logging.getLogger()
            root_logger.addHandler(cls.file_handler)

    def get_logger(self):
        """
        Return the logger instance.
        """
        return self.logger
