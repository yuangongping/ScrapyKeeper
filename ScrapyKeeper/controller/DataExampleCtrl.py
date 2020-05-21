#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:chenlincui
from flask_restful import Resource, reqparse
from ScrapyKeeper.service.DataExampleSrv import DataExampleSrv
from ScrapyKeeper.utils.format_result import success_res, error_res


class DataExampleCtrl(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('project_id', required=True, type=int)
        parser.add_argument('project_name', required=True, type=str)
        args = parser.parse_args(strict=True)
        data = DataExampleSrv.data_example(args)
        return success_res(data)
