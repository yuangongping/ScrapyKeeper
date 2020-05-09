#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:chenlincui
from ScrapyKeeper.model.TemplateMange import TemplateMange
from ScrapyKeeper.model import db
from sqlalchemy import and_
from flask_restful import abort


class TemplateMangeSrv(object):
    @classmethod
    def add(cls, args: dict):
        try:
            # 保存数据
            return TemplateMange.save(args)
        except Exception as e:
            abort(400, message='数据已经存在')

    @classmethod
    def list(cls, args:dict):
        try:
            # 帅选表达式列表
            exp_list = []
            if args.get("crawl_name") is not None and args.get("crawl_name") != '':
                words = args.get("crawl_name").split(' ')
                for word in words:
                    exp_list.append(TemplateMange.name.like('%{}%'.format(word)))
            if args.get("name_zh") is not None and args.get("name_zh")!='':
                exp_list.append(TemplateMange.name_zh == args.get("name_zh"))
            if args.get("status") is not None and args.get("status")!='':
                exp_list.append(TemplateMange.status == args.get("status"))

            order_exp = TemplateMange.date_created.desc()
            # 判断是否分页，分页
            if args.get("page_index"):
                if len(exp_list) > 0:
                    filter_exp = and_(*exp_list)
                    pagination = TemplateMange.query.filter(filter_exp).order_by(
                        order_exp).paginate(
                        args.get("page_index"), args.get("page_size"), error_out=False)
                    return {
                        "total": pagination.total,
                        "data": [dataset.to_dict() for dataset in pagination.items]
                    }
                else:
                    pagination = TemplateMange.query.order_by(
                        order_exp).paginate(
                        args.get("page_index"), args.get("page_size"), error_out=False)
                    return {
                        "total": pagination.total,
                        "data": [dataset.to_dict() for dataset in pagination.items]
                    }
            else:
                if len(exp_list) > 0:
                    filter_exp = and_(*exp_list)
                    pagination = TemplateMange.query.filter(filter_exp).order_by(
                        order_exp).all()
                    return {
                        "total": len(pagination),
                        "data": [dataset.to_dict() for dataset in pagination]
                    }
                else:
                    pagination = TemplateMange.query.order_by(
                        order_exp).all()
                    return {
                        "total": len(pagination),
                        "data": [dataset.to_dict() for dataset in pagination]
                    }
        except Exception as e:
            abort(500, message='Fail to list template')

    @classmethod
    def delete(cls, id: int):
        try:
            template = TemplateMange.query.filter_by(id=id).first()
            if template:
                db.session.delete(template)
                db.session.commit()
            return "删除成功！"
        except Exception as e:
            abort(400, message='delete template failed')

    @classmethod
    def get_start_urls(cls, args: dict):
        objs = TemplateMange.query.filter_by(
            status=args.get("status")
        ).all()
        return [obj.crawl_url for obj in objs]

    @classmethod
    def get_candidate(cls, args: dict):
        objs = TemplateMange.query.filter_by(
            name=args.get("name")
        ).all()
        return [{"crawl_name": obj.crawl_name, "crawl_url": obj.crawl_url} for obj in objs]
