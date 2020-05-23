#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:chenlincui
from ScrapyKeeper.model.SendEmail import SendEmail
import smtplib
from email.mime.text import MIMEText
from ScrapyKeeper import app
from flask_restful import abort


class SendEmailSrv(object):
    @classmethod
    def add_email(cls, args: dict):
        email = args.get('email')
        if '@qq.com' not in email:
            args['email'] = email + '@qq.com'
        SendEmail.save(dic=args)

    @classmethod
    def send_email(cls, round_id: str, project_name: str, num: int, file_size: float, emails: list):
        email_sender = app.config.get('EMAIL_SENDER')  # 发送人
        email_auth_code = app.config.get('EMAIL_AUTH_CODE')  # 发送人QQ授权密码
        messages = '【多彩云-互联网大数据采集平台】工程：{}  \n本次采集数量情况如下：\n    结构化数据{}条，非结构化数据{}Kb'.format(project_name, num, file_size)
        msg = MIMEText(messages, 'plain', 'utf-8')  # 发送信息内容
        msg['Subject'] = '【多彩云-互联网大数据采集平台】工程：%s 数据采集监控邮件' % project_name   # 发送的主题
        msg['From'] = email_sender
        msg['To'] = ','.join(emails)
        print('--------- messages  ', messages)
        try:
            srv = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 邮件服务器及端口号
            srv.login(email_sender, email_auth_code)  # 登录验证信息
            srv.sendmail(email_sender, emails, msg.as_string())  # 发送消息指令

            SendEmail.save({
                "round_id": round_id,
                "title": msg['Subject'],
                "content": messages,
                "email": msg['To']
            })
            return True
        except Exception as e:
            abort(400, message="send email failed")
