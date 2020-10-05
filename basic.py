# 此文件存储基础方法
import smtplib
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import win32api
import win32con
from PyQt5.QtCore import QMimeData, QUrl
from PyQt5.QtWidgets import QApplication
import os


def parseStrListString(input_str):
    if not input_str:
        return []
    temp_list = input_str.split(',')
    tag_list = []
    for i in temp_list:
        tag_list.append(i.strip())
    return tag_list


# 此函数将str列表转换成一个字符串
def strListToString(str_list):
    if not str_list:
        return ""
    tag_str = ", ".join(str_list)
    return tag_str


# 将字符串转换成一个int型列表
def parseIntListString(list_str: str):
    if not list_str:
        return []
    temp_list = list_str.split(',')
    mylist = []
    for i in temp_list:
        mylist.append(int(i.strip()))
    return mylist


# 将int型列表转换成字符串
def intListToString(olist):
    if not olist:
        return ""
    str_list = [str(i) for i in olist]
    return strListToString(str_list)


def CtrlAltZ():
    win32api.keybd_event(0x11, 0, 0, 0)
    win32api.keybd_event(0x12, 0, 0, 0)
    win32api.keybd_event(0x5a, 0, 0, 0)
    win32api.keybd_event(0x11, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(0x12, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(0x5a, 0, win32con.KEYEVENTF_KEYUP, 0)


def CtrlAltW():
    win32api.keybd_event(0x11, 0, 0, 0)
    win32api.keybd_event(0x12, 0, 0, 0)
    win32api.keybd_event(0x57, 0, 0, 0)
    win32api.keybd_event(0x11, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(0x12, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(0x57, 0, win32con.KEYEVENTF_KEYUP, 0)


def copyFile(file_path):
    data = QMimeData()
    url = QUrl.fromLocalFile(file_path)
    data.setUrls([url])
    QApplication.clipboard().setMimeData(data)


def setClipText(text):
    clip = QApplication.clipboard()
    clip.setText(text)


def email_to(file_path, address):
    smtp_server = 'smtp.qq.com'
    from_address = '2587354021@qq.com'
    passwd = 'rxuowjfzqqindhhj'
    to_address = address

    server = smtplib.SMTP_SSL(smtp_server)
    server.login(from_address, passwd)

    msg = MIMEMultipart()
    path, filename = os.path.split(file_path)
    pre, suf = filename.split('.')

    msg['Subject'] = Header(pre)
    msg['From'] = Header(from_address)
    msg['To'] = Header(to_address)

    part = MIMEApplication(open(file_path, 'rb').read())
    part.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(part)
    try:
        server.sendmail(from_address, to_address, msg.as_string())
    except smtplib.SMTPException:
        server.quit()
        return False
    else:
        server.quit()
        return True
