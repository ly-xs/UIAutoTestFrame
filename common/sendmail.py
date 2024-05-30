import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import smtplib
import configparser
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config.config import CONFIG_FILE
from common.logger import Logger

logger = Logger().get_logger(__name__)


def send_mail(filename):
    """
    定义发送邮件
    :param filename:
    :return: 成功：打印发送邮箱成功；失败：返回失败信息
    """
    # --------- 读取config.ini配置文件 ---------------
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE, encoding='utf-8')
    HOST = config.get("user", "HOST_SERVER")
    SENDER = config.get("user", "FROM")
    RECEIVER = config.get("user", "TO")
    USER = config.get("user", "user")
    PWD = config.get("user", "password")
    SUBJECT = config.get("user", "SUBJECT")

    # 内容和附件一样
    with open(filename, encoding='utf-8') as file:
        mail_body = file.read()

    msg = MIMEMultipart()
    msg['from'] = SENDER  # 发送者
    msg['to'] = RECEIVER  # 接收者
    msg['Subject'] = SUBJECT  # 标题
    msg_text = MIMEText(mail_body, 'html', 'utf-8')
    msg.attach(msg_text)

    # 附件
    with open(filename, 'rb') as send_file:
        send_file = send_file.read()
        att = MIMEBase("application", 'octet-stream')
        att.set_payload(send_file)
        encoders.encode_base64(att)
        att.add_header("Content-Disposition", f"attachment; filename= {filename}")
        msg.attach(att)

    # 初始化server变量
    server = None

    try:
        server = smtplib.SMTP_SSL(HOST, 465)  # 非QQ邮箱可以不使用SSL，发送服务器的端口号
        server.login(USER, PWD)
        server.sendmail(SENDER, RECEIVER, msg.as_string())
        logger.info("邮件发送成功！")
    except Exception as e:
        logger.error(f"邮件发送失败！{e}")
    finally:
        server.quit()
