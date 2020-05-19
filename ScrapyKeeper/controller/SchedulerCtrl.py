# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse
from ScrapyKeeper.service.SchedulerSrv import SchedulerSrv
from ScrapyKeeper.utils.format_result import success_res, error_res
import json



class SchedulerCtrl(Resource):
    def get(self):
        """
        立即运行
        :return:
        """
        pass


    def post(self):
        """
        周期调度
        :return:
        """
        parser = reqparse.RequestParser()
        parser.add_argument('project_name', required=True, type=str)
        parser.add_argument('config', required=True, type=str)
        args = parser.parse_args(strict=True)
        schedulerSrv = SchedulerSrv()
        data = schedulerSrv.add_scheduler(args=args)
        return success_res(data)

    def put(self):
        """
        取消运行
        :return:
        """
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, type=int)
        args = parser.parse_args(strict=True)
        schedulerSrv = SchedulerSrv()
        data = schedulerSrv.cancel_running_project(args=args)
        return success_res(data)

    def delete(self):
        """
        取消调度
        :return:
        """
        parser = reqparse.RequestParser()
        parser.add_argument('project_id', required=True, type=int)
        args = parser.parse_args(strict=True)
        schedulerSrv = SchedulerSrv()
        data = schedulerSrv.cancel_scheduler(args=args)
        return success_res(data)