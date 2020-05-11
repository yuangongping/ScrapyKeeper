# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse
from ScrapyKeeper.service.DataCentralSrv import DataCentralSrv
from ScrapyKeeper.utils.format_result import success_res, error_res


class DataCentralCtrl(Resource):
    def get(self):
        """
        获取数据中心的服务器状态，数据状态数据
        :return:
        """
        parser = reqparse.RequestParser()
        args = parser.parse_args(strict=True)
        dataCentralSrv = DataCentralSrv()
        data = dataCentralSrv.get()
        return success_res(data)

    def post(self):
        """
        获取近一周的数据入库柱状图数据
        :return:
        """
        dataCentralSrv = DataCentralSrv()
        data = dataCentralSrv.get_week_data()
        return success_res(data)
