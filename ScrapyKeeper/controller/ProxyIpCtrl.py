#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : ProxyIpCtrl.py
# @Time    : 2020-5-17 21:06
# @Software: PyCharm
# @Author  : Taoz
# @contact : xie-hong-tao@qq.com
import demjson
from flask_restful import Resource, reqparse
from ScrapyKeeper.service.ProxyIpSrv import ProxyIpSrv
from ScrapyKeeper.utils import success_res
from ScrapyKeeper.model.ProxyIp import ProxyIpAgency


class ProxyIpCtrl(Resource):
    srv = ProxyIpSrv(ProxyIpAgency)

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('timestamp', required=True, type=int)
        parser.add_argument('project', required=True, type=str)
        parser.add_argument('get_num', required=True, type=int)
        args = parser.parse_args(strict=True)
        return success_res(self.srv.get_ip(**args))
