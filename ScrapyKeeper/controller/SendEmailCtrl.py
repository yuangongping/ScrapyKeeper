#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:chenlincui
from flask_restful import Resource, reqparse
from ScrapyKeeper.service.SendEmailSrv import SendEmailSrv
from ScrapyKeeper.utils.format_result import success_res


class SendEmailCtrl(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('project_name', required=True, type=str)
        parser.add_argument('email', required=True, type=str)
        parser.add_argument('number', default=0, type=int)
        parser.add_argument('image_size', default=0, type=int)
        args = parser.parse_args(strict=True)
        SendEmailSrv.send_email(project_name=args.get('project_name'),
                                email=args.get('email'),
                                number=args.get('number'),
                                image_size=args.get('image_size'))
        return success_res()

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('project_name', required=True, type=str)
        parser.add_argument('project_id', required=True, type=str)
        parser.add_argument('job_id', required=True, type=str)
        parser.add_argument('email', required=True, type=str)
        args = parser.parse_args(strict=True)
        SendEmailSrv.add_email(args=args)
        return success_res()
