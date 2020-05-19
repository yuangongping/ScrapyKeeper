# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse
from ScrapyKeeper.service.DataStorageSrv import DataStorageSrv
from ScrapyKeeper.utils.format_result import success_res, error_res
from flask_restful import request


class DataStorageCtrl(Resource):
    def get(self):
        pass

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('scheduler_id', required=True, type=str)
        parser.add_argument('type', required=True, type=str)
        parser.add_argument('num', type=float)
        parser.add_argument('file_size',  type=float)
        args = parser.parse_args(strict=True)
        args["ip"] = request.remote_addr
        dataStorageSrv = DataStorageSrv()
        scrapyd_url = "http://{}:6800".format(args.get("ip"))
        if args.get("type") == "openspider":
            dataStorageSrv.update_start_time(
                scheduler_id=args.get("scheduler_id"),
                scrapyd_url=scrapyd_url
            )
        elif args.get("type") == "closespider":
            dataStorageSrv.update_end_time(
                scheduler_id=args.get("scheduler_id"),
                scrapyd_url=scrapyd_url
            )
        else:
            dataStorageSrv.add(
                scheduler_id=args.get("scheduler_id"),
                scrapyd_url=scrapyd_url,
                num=args.get("num", 200),
                file_size=args.get("file_size", 0)
            )
        return success_res("")
