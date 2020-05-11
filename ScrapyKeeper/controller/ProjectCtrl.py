# -*- coding: utf-8 -*-
from flask import request
from flask_restful import Resource, reqparse
from ScrapyKeeper.service.ProjectSrv import ProjectSrv
from ScrapyKeeper.utils.format_result import success_res, error_res


class ProjectCtrl(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page_index', required=True, type=int)
        parser.add_argument('page_szie', required=True, type=int)
        args = parser.parse_args(strict=True)
        projectSrv = ProjectSrv()
        data = projectSrv.get_all_projects(args=args)
        return success_res(data)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('project_name_zh', required=True, type=str)
        parser.add_argument('url', required=True, type=str)
        parser.add_argument('template', required=True, type=str)
        args = parser.parse_args()

        tmpl = args.pop('template')
        projectSrv = ProjectSrv()
        data = projectSrv.add_project(tmpl_name=tmpl, tmpl_args=args)
        return success_res(data)

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, type=int)
        parser.add_argument('project_name_zh', required=True, type=str)
        parser.add_argument('category', required=True, type=str)
        parser.add_argument('is_msd', required=True, type=int)
        args = parser.parse_args(strict=True)
        projectSrv = ProjectSrv()
        data = projectSrv.edit_project(args=args)
        return success_res(data)

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, type=int)
        parser.add_argument('project_name', required=True, type=str)
        args = parser.parse_args(strict=True)
        projectSrv = ProjectSrv()
        data = projectSrv.del_projects(args=args)
        return success_res(data)

