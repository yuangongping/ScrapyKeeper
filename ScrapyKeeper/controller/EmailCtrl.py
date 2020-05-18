#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : EmailCtrl.py
# @Time    : 2020-5-17 16:39
# @Software: PyCharm
# @Author  : Taoz
# @contact : xie-hong-tao@qq.com
# 接受邮件通知的邮箱
from flask_restful import Resource, reqparse
from ScrapyKeeper.service.EmailSrv import EmailSrv
from ScrapyKeeper.model.Email import Email
from ScrapyKeeper.utils import success_res


class EmailCtrl(Resource):
    srv = EmailSrv(Email)

    def get(self):
        return success_res(self.srv.all())

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str)
        args = parser.parse_args(strict=True)
        return success_res(self.srv.save(**args))

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, type=str)
        args = parser.parse_args(strict=True)
        self.srv.delete(**args)
        return success_res()