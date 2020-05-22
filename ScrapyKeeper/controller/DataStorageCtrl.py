# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse
from ScrapyKeeper.service.DataStorageSrv import DataStorageSrv
from ScrapyKeeper.utils.format_result import success_res, error_res
from flask_restful import request, abort


class DataStorageCtrl(Resource):
    def get(self):
        pass

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('scheduler_id', required=True, type=str)
        parser.add_argument('round_id', type=str)
        parser.add_argument('type', required=True, type=str)
        parser.add_argument('num', type=float)
        parser.add_argument('file_size',  type=float)
        parser.add_argument('node_type', type=str)
        args = parser.parse_args()
        args["ip"] = request.remote_addr
        dataStorageSrv = DataStorageSrv()
        scrapyd_url = "http://{}:6800".format(args.get("ip"))
        if args.get("type") == "open_spider":
            dataStorageSrv.update_start_time(
                scheduler_id=args.get("scheduler_id"),
                scrapyd_url=scrapyd_url
            )
        elif args.get("type") == "close_spider":
            dataStorageSrv.update_end_time(
                scheduler_id=args.get("scheduler_id"),
                scrapyd_url=scrapyd_url
            )
            if not args.get("node_type"):
                dataStorageSrv.add(
                    scheduler_id=args.get("scheduler_id"),
                    scrapyd_url=scrapyd_url,
                    num=args.get("num"),
                    file_size=args.get("file_size")
                )
        elif args.get("type") == "statistics":
            dataStorageSrv.add(
                scheduler_id=args.get("scheduler_id"),
                scrapyd_url=scrapyd_url,
                round_id=args.get('round_id'),
                num=args.get("num"),
                file_size=args.get("file_size")
            )
        else:
          abort(400, message="type参数错误！")
        return success_res()
