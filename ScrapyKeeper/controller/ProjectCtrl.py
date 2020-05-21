# -*- coding: utf-8 -*-
from flask import request
from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage

from ScrapyKeeper.service.ProjectSrv import ProjectSrv
from ScrapyKeeper.utils.format_result import success_res, error_res


class ProjectCtrl(Resource):
    def __init__(self):
        self.srv = ProjectSrv()

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page_index', required=True, type=int)
        parser.add_argument('page_size', required=True, type=int)
        parser.add_argument('category', type=str)
        parser.add_argument('status', type=str)
        parser.add_argument('project_name_zh', type=str)
        parser.add_argument('project_name', type=str)
        parser.add_argument('type', type=str)
        args = parser.parse_args()
        if args.get("type") == "info":
            data = self.srv.get_project_by_project_name(project_name_zh=args.get("project_name_zh"))
        else:
            data = self.srv.list_projects(args=args)
        return success_res(data)

    def post(self):
        if request.form.get('template'):
            parser = reqparse.RequestParser()
            parser.add_argument('project_name_zh', required=True, type=str)
            parser.add_argument('template', type=str)
            # parser.add_argument('tpl_input', required=True, type=str)
            args = parser.parse_args()
            args['tpl_input'] = '{}'
            tmpl = args.pop('template')
            args["category"] = tmpl
            data = self.srv.add_project_by_template(tpl_name=tmpl, tpl_args=args)
        else:
            parser = reqparse.RequestParser()
            parser.add_argument('project_name_zh', required=True, type=str)
            parser.add_argument('master_egg', required=True, type=FileStorage, location='files')
            parser.add_argument('slave_egg', type=FileStorage, location='files')
            args = parser.parse_args()
            data = self.srv.add_project(args['project_name_zh'], args['master_egg'], args.get('slave_egg'))
        return success_res(data)

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, type=int)
        parser.parse_args()
        data = self.srv.edit_project(**request.form.to_dict())
        return success_res(data)

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('project_id', required=True, type=int)
        parser.add_argument('project_name', required=True, type=str)
        args = parser.parse_args(strict=True)
        msg = self.srv.del_project(**args)
        return success_res(msg)
