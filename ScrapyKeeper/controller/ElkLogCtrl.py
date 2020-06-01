#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:chenlincui
# 获取ELK日志
from flask_restful import Resource, reqparse
from ScrapyKeeper.service.ElkLogSrv import ElkLogSrv

from ScrapyKeeper.utils import success_res


class ElkLogCtrl(Resource):
    def get(self):
        """ 计算各项目的错误日志数, 用于提示哪些项目有错误日志, 错误日志数大于0的项目将有预警标识 """
        data = ElkLogSrv.log_count()
        return success_res(data)

    def post(self):
        """ 根据项目查找该项目的错误日志信息 """
        parser = reqparse.RequestParser()
        parser.add_argument('project_name', required=True, type=str)
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('page_size', type=int, default=5)
        args = parser.parse_args(strict=True)

        data = ElkLogSrv.log_messages(
            project_name=args.get("project_name"),
            page=args.get("page"),
            page_size=args.get("page_size")
        )
        return success_res(data)

    def delete(self):
        """ 根据项目删除已经处理过得错误日志信息, 同时清除本地日志 """
        parser = reqparse.RequestParser()
        parser.add_argument('project_name', required=True, type=str)
        args = parser.parse_args(strict=True)
        data = ElkLogSrv.log_delete(
            project_name=args.get("project_name")
        )
        return success_res(data)
