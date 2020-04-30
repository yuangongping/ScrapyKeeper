# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse
from ScrapyKeeper.service.ProjectSrv import ProjectSrv
from ScrapyKeeper.utils.format_result import success_res, error_res


class ProjectCtrl(Resource):
    def get(self):
        pass

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name_zh', required=True, type=str)
        parser.add_argument('url', required=True, type=str)
        parser.add_argument('template', required=True, type=str)
        args = parser.parse_args(strict=True)
        projectSrv = ProjectSrv()
        data = projectSrv.add_project(args=args)
        return success_res(data)

    def put(self):
        pass

    def delete(self):
        pass