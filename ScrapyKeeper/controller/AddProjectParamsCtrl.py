# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse
from ScrapyKeeper.service.ProjectSrv import ProjectSrv
from ScrapyKeeper.utils.format_result import success_res, error_res
import demjson


class AddProjectParamsCtrl(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int)
        args = parser.parse_args(strict=True)
        return success_res('')

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int)
        args = parser.parse_args(strict=True)
        return success_res('')