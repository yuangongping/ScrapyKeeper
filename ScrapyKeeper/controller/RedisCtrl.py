# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse
from ScrapyKeeper.service.RedisSrv import RedisSrv
from ScrapyKeeper.utils.format_result import success_res, error_res


class RedisCtrl(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('project_name', type=str)
        args = parser.parse_args(strict=True)
        redisSrv = RedisSrv(host='172.16.119.6', port=6379)
        data = redisSrv.get(args)
        return success_res(data)
