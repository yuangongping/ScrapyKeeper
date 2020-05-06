# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse
from ScrapyKeeper.service.DataStorageSrv import DataStorageSrv
from ScrapyKeeper.utils.format_result import success_res, error_res


class DataStorageCtrl(Resource):
    def get(self):
        pass

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('project_name', required=True, type=str)
        parser.add_argument('project_alias', required=True, type=str)
        parser.add_argument('num', required=True, type=int)
        parser.add_argument('file_size', required=True, type=int)
        args = parser.parse_args(strict=True)
        dataStorageSrv = DataStorageSrv()
        data = dataStorageSrv.add(args=args)
        return success_res(data)
