import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import smtplib
import configparser
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config.config import CONFIG_FILE
from common.logger import Logger

logger = Logger(logger="send_mail")


def send_mail(file_new):
    """
    定义发送邮件
    :param file_new:
    :return: 成功：打印发送邮箱成功；失败：返回失败信息
    """
    # 内容和附件一样
    with open(file_new, 'rb') as f:
        send_file = mail_body = f.read()

    # --------- 读取config.ini配置文件 ---------------

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE, encoding='utf-8')
    HOST = config.get("user", "HOST_SERVER")
    SENDER = config.get("user", "FROM")
    RECEIVER = config.get("user", "TO")
    USER = config.get("user", "user")
    PWD = config.get("user", "password")
    SUBJECT = config.get("user", "SUBJECT")

    # # 附件
    # att = MIMEText(send_file, 'base64', 'utf-8')
    # att["Content-Type"] = 'application/octet-stream'
    # att.add_header("Content-Disposition", "attachment", filename=("gbk", "", report))
    #
    # # 三个参数：第一个是文本内容，第二个plain设置文本格式，第三个utf-8设置编码
    # msg = MIMEMultipart('related')
    # msg.attach(att)
    # msg_text = MIMEText(mail_body, 'html', 'utf-8')
    # msg.attach(msg_text)
    # msg['Subject'] = SUBJECT  # 标题
    # msg['from'] = SENDER  # 发送者
    # msg['to'] = RECEIVER  # 接收者

    msg = MIMEMultipart()
    msg_text = MIMEText(mail_body, 'html', 'utf-8')
    msg.attach(msg_text)
    msg['Subject'] = SUBJECT  # 标题
    msg['from'] = SENDER  # 发送者
    msg['to'] = RECEIVER  # 接收者
    # msg['to'] = '.'.join(['xxx@qq.com', 'xxx@qq.com'])

    # 附件
    att = MIMEBase("application", 'octet-stream')
    att.set_payload(send_file)
    att.add_header("Content-Disposition", "attachment", filename=Header(file_new, "gbk").encode())
    encoders.encode_base64(att)
    msg.attach(att)

    try:
        # server = smtplib.SMTP()
        # server.connect(HOST)
        # server.starttls()
        # server.login(USER, PWD)
        # server.sendmail(SENDER, RECEIVER, msg.as_string())
        server = smtplib.SMTP_SSL(HOST, 465)  # 非QQ邮箱可以不使用SSL，发送服务器的端口号
        server.login(USER, PWD)
        server.sendmail(SENDER, RECEIVER, msg.as_string())
        server.quit()
        logger.info("邮件发送成功！")
    except Exception as e:
        logger.error(f"邮件发送失败！{e}")
