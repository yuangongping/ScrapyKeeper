from flask_restful import Resource, reqparse
from ScrapyKeeper.service.TemplateMangeSrv import TemplateMangeSrv
from ScrapyKeeper.utils import success_res


class StartUrlsCtrl(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('status', type=str)
        args = parser.parse_args(strict=True)
        data = TemplateMangeSrv.get_start_urls(args=args)
        return success_res(data)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        args = parser.parse_args(strict=True)
        data = TemplateMangeSrv.get_candidate(args=args)
        return success_res(data)
