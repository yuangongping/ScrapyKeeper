#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:chenlincui
from flask_restful import Resource, reqparse
from ScrapyKeeper.service.TemplateMangeSrv import TemplateMangeSrv
from ScrapyKeeper.utils import success_res, error_res

class TemplateMangeCtrl(Resource):
    def post(self):
        """ 添加模板 """
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, type=str)
        parser.add_argument('name_zh', required=True, type=str)
        parser.add_argument('crawl_name', required=True, type=str)
        parser.add_argument('crawl_url', required=True, type=str)
        args = parser.parse_args(strict=True)
        data = TemplateMangeSrv.add(args)
        if not data:
            return error_res("存储错误！")
        return success_res(data)

    def delete(self):
        """ 删除模板 """
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, type=int)
        args = parser.parse_args(strict=True)
        data = TemplateMangeSrv.delete(id=args.get("id"),)
        return success_res(data)

    def put(self):
        """ 修改模板 """
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, type=int)
        parser.add_argument('name', required=True, type=str)
        parser.add_argument('name_zh', required=True, type=str, )
        parser.add_argument('crawl_name', required=True, type=str)
        parser.add_argument('crawl_url', required=True, type=str)
        parser.add_argument('status', required=True, type=int)
        args = parser.parse_args(strict=True)
        data = TemplateMangeSrv.add(args)
        return success_res(data)

    def get(self):
        """ 列出所有的模板 """
        parser = reqparse.RequestParser()
        parser.add_argument('crawl_name', type=str)

        parser.add_argument('name_zh', type=str)
        parser.add_argument('status', type=str)
        parser.add_argument('page_index', type=int)
        parser.add_argument('page_size', type=int)
        args = parser.parse_args(strict=True)
        data = TemplateMangeSrv.list(args=args)
        return success_res(data)
