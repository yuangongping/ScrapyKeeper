#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : TemplateCheckCtrl.py
# @Time    : 2020-5-12 11:37
# @Software: PyCharm
# @Author  : Taoz
# @contact : xie-hong-tao@qq.com
from flask import request
from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from ScrapyKeeper.utils import success_res, error_res
from ScrapyKeeper.service.TemplateParserSrv import TemplateParserSrv
import io


class TemplateParserCtrl(Resource):
    def post(self):
        """ 添加模板 """
        addr = request.remote_addr
        parser = reqparse.RequestParser()
        parser.add_argument('tpl_zip', required=True, type=FileStorage, location='files')
        args = parser.parse_args(strict=True)
        tpl_zip = args["tpl_zip"].stream.read()
        file_name = '%s%s' % (addr, secure_filename(args["tpl_zip"].filename))
        return success_res(TemplateParserSrv.parse(file_name, tpl_zip))
