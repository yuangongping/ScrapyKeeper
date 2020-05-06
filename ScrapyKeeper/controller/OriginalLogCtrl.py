# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse
from ScrapyKeeper.service.OriginalLogSrv import OriginalLogSrv
from ScrapyKeeper.utils.format_result import success_res, error_res


class OriginalLogCtrl(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, type=int)
        args = parser.parse_args(strict=True)
        originalLogSrv = OriginalLogSrv()
        data = originalLogSrv.view_log(args=args)
        return success_res(data)
