#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:chenlincui
import smtplib
from email.mime.text import MIMEText
from ScrapyKeeper import app


def send_email(subject: str, msg: str, address: str):
    '''
    QQ邮箱发送邮件
    :param subject: 发送主题
    :param msg: 发送内容
    :param address: 收件人地址
    :return:
    '''
    email_sender = app.config.get('EMAIL_SENDER')  # 发送人
    email_auth_code = app.config.get('EMAIL_AUTH_CODE')  # 发送人QQ授权密码
    msg = MIMEText(msg, 'plain', 'utf-8')  # 发送信息内容
    msg['Subject'] = subject  # 发送的主题
    msg['From'] = email_sender
    msg['To'] = address
    try:
        srv = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 邮件服务器及端口号
        srv.login(email_sender, email_auth_code)  # 登录验证信息
        srv.sendmail(email_sender, address, msg.as_string())  # 发送消息指令
    except Exception as e:
        print('邮件无法发送：%s' % e)
