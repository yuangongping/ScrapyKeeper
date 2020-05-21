from flask_restful import Resource, reqparse
from ScrapyKeeper.service.SchedulerSrv import SchedulerSrv
from ScrapyKeeper.utils import success_res


class StartUrlsCtrl(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('scheduler_id', type=str)
        args = parser.parse_args(strict=True)
        schedulerSrv = SchedulerSrv()
        data = schedulerSrv.getbyid(id=args.get("scheduler_id"))
        return success_res(data)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        args = parser.parse_args(strict=True)
        data = TemplateMangeSrv.get_candidate(args=args)
        return success_res(data)
