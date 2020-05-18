#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : ProxyIpProvider.py
# @Time    : 2020-5-16 17:22
# @Software: PyCharm
# @Author  : Taoz
# @contact : xie-hong-tao@qq.com
import demjson
from flask_restful import Resource, reqparse
from ScrapyKeeper.service.ProxyIpSrv import ProxyIpSrv
from ScrapyKeeper.utils import success_res
from ScrapyKeeper.model.ProxyIp import ProxyIpAgency


class ProxyIpAgencyCtrl(Resource):
    srv = ProxyIpSrv(ProxyIpAgency)

    def get(self):
        return success_res(self.srv.all())

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('agency_name', type=str)
        parser.add_argument('req_url', type=str)
        parser.add_argument('req_num_per', type=int)
        parser.add_argument('req_num_max', type=int)
        parser.add_argument('live_time', type=int)
        parser.add_argument('method', type=str)
        parser.add_argument('params', type=str)
        parser.add_argument('headers', type=str)
        parser.add_argument('body', type=str)
        args = parser.parse_args(strict=True)

        return success_res(self.srv.save(**args))

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True)
        parser.add_argument('agency_name', type=str)
        parser.add_argument('req_url', type=str)
        parser.add_argument('req_num_per', type=int)
        parser.add_argument('req_num_max', type=int)
        parser.add_argument('live_time', type=int)
        parser.add_argument('method', type=str)
        parser.add_argument('params', type=str)
        parser.add_argument('headers', type=str)
        parser.add_argument('body', type=str)
        args = parser.parse_args()

        return success_res(self.srv.save(**args))

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, type=str)
        args = parser.parse_args(strict=True)
        self.srv.delete(**args)
        return success_res()
