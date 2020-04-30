#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:chenlincui
from flask_restful import reqparse, Resource
from ScrapyKeeper.service.DataCountSrv import DataCountSrv
from ScrapyKeeper.utils import success_res


class DataCountCtrl(Resource):
    def post(self):
        """ 数据采集量统计 """
        parser = reqparse.RequestParser()
        parser.add_argument('project_name', required=True, type=str)
        parser.add_argument('developers', type=str, default=None)
        parser.add_argument('address', type=str, required=True)
        parser.add_argument('db_name', type=str, required=True)
        parser.add_argument('table_name', required=True, type=str)
        parser.add_argument('number', type=int, required=True)
        parser.add_argument('image_number', type=int, default=0)
        parser.add_argument('video_number', default=0, type=int)
        parser.add_argument('audio_number', type=int, default=0)
        parser.add_argument('file_number', type=int, default=0)
        parser.add_argument('image_size', default=0, type=float)
        parser.add_argument('video_size', type=float, default=0)
        parser.add_argument('audio_size', type=float, default=0)
        parser.add_argument('file_size', default=0, type=float)
        args = parser.parse_args(strict=True)
        data = DataCountSrv.save(args)
        return success_res(data)
