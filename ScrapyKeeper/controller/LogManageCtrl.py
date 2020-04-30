#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:chenlincui
from flask_restful import Resource, reqparse
from ScrapyKeeper.service.LogManageSrv import LogManageSrv
from ScrapyKeeper.utils import success_res


class LogCountCtrl(Resource):
    def get(self):
        data = LogManageSrv.log_count()
        return success_res(data)


class LogMessagesCtrl(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('project_name', required=True, type=str)
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('page_size', type=int, default=5)
        args = parser.parse_args(strict=True)

        data = LogManageSrv.log_messages(
            project_name=args.get("project_name"),
            page=args.get("page"),
            page_size=args.get("page_size"),
        )
        return success_res(data)
