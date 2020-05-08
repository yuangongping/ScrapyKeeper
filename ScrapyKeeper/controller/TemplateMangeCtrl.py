#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:chenlincui
from flask_restful import Resource, reqparse
from ScrapyKeeper.service.TemplateMangeSrv import TemplateMangeSrv
from ScrapyKeeper.utils import success_res


class TemplateMangeCtrl(Resource):
    def get(self):
        """ 列出所有的模板 """
        data = TemplateMangeSrv.list()
        return success_res(data)

    def post(self):
        """ 添加模板 """
        parser = reqparse.RequestParser()
        parser.add_argument('template_name', required=True, type=str)
        parser.add_argument('template_type', type=str, required=True)
        parser.add_argument('crawl_url', required=True, type=str)
        parser.add_argument('status', type=int, required=True)
        args = parser.parse_args(strict=True)
        data = TemplateMangeSrv.add(args)
        return success_res(data)

    def delete(self):
        """ 删除模板 """
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, type=int)
        args = parser.parse_args(strict=True)
        TemplateMangeSrv.delete(
            id=args.get("id"),
        )
        return success_res()

    def put(self):
        """ 修改模板 """
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, type=int)
        parser.add_argument('template_name', required=True, type=str)
        parser.add_argument('template_type', type=str, required=True)
        parser.add_argument('crawl_url', required=True, type=str)
        parser.add_argument('status', type=int, required=True)
        args = parser.parse_args(strict=True)

        data = TemplateMangeSrv.add(args)
        return success_res(data)
