#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:chenlincui
from flask_restful import Resource, reqparse
from ScrapyKeeper.service.TemplateMangeSrv import TemplateMangeSrv
from ScrapyKeeper.utils import success_res, error_res
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename


class TemplateMangeCtrl(Resource):
    def post(self):
        """ 添加模板 """
        parser = reqparse.RequestParser()
        parser.add_argument('tpl_name', required=True, type=str)
        parser.add_argument('tpl_zh', required=True, type=str)
        parser.add_argument('tpl_type', required=True, type=int)
        parser.add_argument('tpl_input', type=str)
        parser.add_argument('tpl_img', required=True, type=FileStorage, location='files')
        parser.add_argument('tpl_zip', required=True, type=FileStorage, location='files')
        args = parser.parse_args(strict=True)
        args["tpl_img"] = args["tpl_img"].stream.read()
        obj = {
            "tpl_name": args.get("tpl_name"),
            "tpl_zh": args.get("tpl_zh"),
            "tpl_type": args.get("tpl_type"),
            "tpl_input": args.get("tpl_input") if args.get("tpl_input") else '',
            "tpl_img": args.get("tpl_img")
        }
        # TODO: 将图片存到static目录，tpl_img存储该目录的路径
        file_name = secure_filename(args["tpl_zip"].filename)
        tpl_zip = args["tpl_zip"].stream.read()
        data = TemplateMangeSrv.add(obj, tpl_zip, file_name)
        if not data:
            return error_res("存储错误！")
        return success_res()

    def delete(self):
        """ 删除模板 """
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, type=int)
        args = parser.parse_args(strict=True)
        data = TemplateMangeSrv.delete(id=args.get("id"))
        return success_res(data)

    def put(self):
        """ 添加模板 """
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, type=int)
        parser.add_argument('tpl_name', required=True, type=str)
        parser.add_argument('tpl_zh', required=True, type=str)
        parser.add_argument('tpl_type', required=True, type=int)
        parser.add_argument('tpl_input', required=True, type=str)
        # parser.add_argument('tpl_img', type=FileStorage, location='files')
        # parser.add_argument('tpl_zip', type=FileStorage, location='files')
        args = parser.parse_args(strict=True)
        data = TemplateMangeSrv.save(args=args)
        if not data:
            return error_res("存储错误！")
        return success_res(data)

    def get(self):
        """ 列出所有的模板 """
        return success_res(TemplateMangeSrv.list())
