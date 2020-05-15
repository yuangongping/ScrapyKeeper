# -*- coding: utf-8 -*-
from flask import request
from flask_restful import Resource, reqparse
from ScrapyKeeper.service.ProjectSrv import ProjectSrv
from ScrapyKeeper.utils.format_result import success_res, error_res


class ProjectCtrl(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page_index', required=True, type=int)
        parser.add_argument('page_size', required=True, type=int)
        parser.add_argument('category', type=str)
        parser.add_argument('status', type=str)
        parser.add_argument('project_name_zh', type=str)
        parser.add_argument('project_name', type=str)
        args = parser.parse_args()
        projectSrv = ProjectSrv()
        data = projectSrv.get_all_projects(args=args)
        return success_res(data)

    def post(self):
        # TODO 模板部署和普通部署分开
        parser = reqparse.RequestParser()
        parser.add_argument('project_name_zh', required=True, type=str)
        parser.add_argument('template', required=True, type=str)
        parser.add_argument('tpl_input', required=True, type=str)
        args = parser.parse_args()
        tmpl = args.pop('template')
        args["category"] = tmpl
        projectSrv = ProjectSrv()
        data = projectSrv.add_project(tmpl_name=tmpl, tmpl_args=args)
        return success_res(data)

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, type=int)
        parser.parse_args()
        projectSrv = ProjectSrv()
        data = projectSrv.edit_project(**request.form.to_dict())
        return success_res(data)

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, type=int)
        parser.add_argument('project_name', required=True, type=str)
        args = parser.parse_args(strict=True)
        projectSrv = ProjectSrv()
        msg = projectSrv.del_projects(**args)
        return success_res(msg)

