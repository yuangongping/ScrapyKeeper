# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse
from ScrapyKeeper.service.DataStorageSrv import DataStorageSrv
from ScrapyKeeper.utils.format_result import success_res, error_res


class ProjectDataTrendCtrl(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('project_name_zh', type=str)
        args = parser.parse_args(strict=True)
        dataStorageSrv = DataStorageSrv()
        data = dataStorageSrv.get_project_data_trend(args)
        return success_res(data)
