import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import logging
from logging.handlers import RotatingFileHandler
from config import config
from threading import Lock


class Logger:
    """
    日志记录类
    """
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = super(Logger, cls).__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self, level: int = logging.INFO):
        if self._initialized:
            return

        self._initialized = True

        # 创建logger
        self.logger = logging.getLogger("AppLogger")
        self.logger.setLevel(level)

        # 移除所有旧的处理器
        self.logger.handlers.clear()

        # 创建并添加控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_formatter = logging.Formatter('%(asctime)s - %(name)s - line:%(lineno)3d - %(levelname)s: %(message)s')
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        # 确保日志目录存在
        if not os.path.exists(config.LOG_DIR):
            os.makedirs(config.LOG_DIR)

        # 创建并添加文件处理器
        log_file_name = os.path.join(config.LOG_DIR, f"{time.strftime('%Y-%m-%d_%H_%M_%S')}.log")
        file_handler = RotatingFileHandler(log_file_name, maxBytes=50 * 1024, encoding='utf-8', backupCount=5)
        file_handler.setLevel(level)
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - line:%(lineno)3d - %(levelname)s: %(message)s')
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

        # 删除超过三个的旧日志文件
        self._cleanup_old_logs(config.LOG_DIR, backup_count=3)

    @staticmethod
    def _cleanup_old_logs(log_dir, backup_count):
        """
        删除超过指定数量的旧日志文件
        """
        log_files = sorted(
            (os.path.join(log_dir, f) for f in os.listdir(log_dir) if f.endswith('.log')),
            key=os.path.getmtime
        )
        while len(log_files) > backup_count:
            os.remove(log_files.pop(0))

    def get_logger(self, module_name: str) -> logging.Logger:
        """
        根据模块名称返回日志记录器实例
        """
        return self.logger.getChild(module_name)
