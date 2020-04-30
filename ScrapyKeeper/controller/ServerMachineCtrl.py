#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:chenlincui
from flask_restful import Resource, reqparse
from ScrapyKeeper.service.ParamConfigSrv import ParamConfigSrv
from ScrapyKeeper.utils import success_res


class AddMachinesCtrl(Resource):
    def get(self):
        data = ParamConfigSrv.list_machine()
        return success_res(data)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ip', required=True, type=str)
        parser.add_argument('is_master', type=str, required=True)
        parser.add_argument('status', type=str, required=True)
        args = parser.parse_args(strict=True)

        data = ParamConfigSrv.add_machine(
            ip=args.get("ip"),
            is_master=args.get("is_master"),
            status=args.get("status"),
        )
        return success_res(data)

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, type=int)
        args = parser.parse_args(strict=True)

        ParamConfigSrv.delete_machine(
            id=args.get("id"),
        )
        return success_res()

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, type=str)
        parser.add_argument('ip', required=True, type=str)
        parser.add_argument('is_master', type=str, required=True)
        parser.add_argument('status', type=str, required=True)
        args = parser.parse_args(strict=True)

        data = ParamConfigSrv.edit_machine(
            id=args.get("id"),
            ip=args.get("ip"),
            is_master=args.get("is_master"),
            status=args.get("status"),
        )
        return success_res(data)
