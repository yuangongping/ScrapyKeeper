#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:chenlincui
from flask import request
from flask_restful import Resource, reqparse, abort

from ScrapyKeeper.agent.ScrapyAgent import ScrapyAgent
from ScrapyKeeper.service.ServerMachineSrv import ServerMachineSrv
from ScrapyKeeper.utils import success_res, error_res

class ServerMachineCtrl(Resource):
    def get(self):
        """ 列出所有的服务器信息 """
        url = request.args.get('url')
        if url is None:
            data = ServerMachineSrv.list()
            return success_res(data)
        else:
            agent = ScrapyAgent(url)
            return success_res(agent.daemon_status())

    def post(self):
        """ 添加服务器 """
        parser = reqparse.RequestParser()
        parser.add_argument('url', required=True, type=str)
        parser.add_argument('is_master', type=int, required=True)
        parser.add_argument('status', type=int, required=True)
        args = parser.parse_args(strict=True)
        ServerMachineSrv.save(args)
        return success_res()

    def delete(self):
        """ 删除服务器 """
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, type=str)
        args = parser.parse_args(strict=True)
        ServerMachineSrv.delete(id=args.get("id"))
        return success_res()

    def put(self):
        """ 修改服务器信息 """
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, type=int)
        parser.add_argument('url', required=True, type=str)
        parser.add_argument('is_master', required=True, type=int)
        parser.add_argument('status', required=True, type=int)
        args = parser.parse_args(strict=True)

        data = ServerMachineSrv.save(args)
        return success_res(data)

