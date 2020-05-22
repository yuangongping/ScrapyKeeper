# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse
from ScrapyKeeper.service.ScrapydLogSrv import ScrapydLogSrv
from ScrapyKeeper.utils.format_result import success_res, error_res


class ScrapydLogCtrl(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('scheduler_id', required=True, type=int)
        parser.add_argument('node_type', required=True, type=str)
        args = parser.parse_args(strict=True)
        originalLogSrv = ScrapydLogSrv()
        if args.get("node_type") == "master":
            data = originalLogSrv.view_master_log(scheduler_id=args.get("scheduler_id"))
            return success_res(data)
        else:
            data = originalLogSrv.view_slave_log(scheduler_id=args.get("scheduler_id"))
            return success_res(data)
