#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:chenlincui
from flask_restful import Resource, reqparse, abort
from ScrapyKeeper.service.ServerMachineSrv import ServerMachineSrv
from ScrapyKeeper.utils import success_res, error_res


class ServerMachineCtrl(Resource):
    def get(self):
        """ 列出所有的服务器信息 """
        data = ServerMachineSrv.list()
        return success_res(data)

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
        # abort(400, message="删除失败")
        ServerMachineSrv.delete(id=args.get("id"))
        return success_res()

    def put(self):
        """ 修改服务器信息 """
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, type=int)
        parser.add_argument('url', required=True, type=str)
        parser.add_argument('is_master', required=True, type=int)
        parser.add_argument('status', required=True, type=int)
        parser.add_argument('date_created', type=str)
        parser.add_argument('date_modified', type=str)
        args = parser.parse_args(strict=True)
        args.pop("date_created")
        args.pop("date_modified")
        print(args)
        data = ServerMachineSrv.save(args)
        return success_res(data)
