# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse
from ScrapyKeeper.service.RedisSrv import RedisSrv
from ScrapyKeeper.utils.format_result import success_res, error_res
import demjson


class RedisCtrl(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('project_name', type=str)
        parser.add_argument('tpl_input', type=str)
        args = parser.parse_args(strict=True)
        tmp_input = demjson.decode(args.get("tpl_input"))
        host = tmp_input.get("redis_host").get("value")
        port = tmp_input.get("redis_port").get("value")
        redisSrv = RedisSrv(host=host, port=port)
        data = redisSrv.get(args)
        return success_res(data)
