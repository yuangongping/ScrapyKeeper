# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse
from ScrapyKeeper.service.RedisSrv import RedisSrv
from ScrapyKeeper.utils.format_result import success_res, error_res
import demjson


class RedisCtrl(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('project_id', type=int)
        parser.add_argument('project_name', type=str)
        args = parser.parse_args(strict=True)
        data = RedisSrv.getRedisUrls(args)
        return success_res(data)
