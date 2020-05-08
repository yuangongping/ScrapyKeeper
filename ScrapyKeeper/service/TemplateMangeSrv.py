#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:chenlincui
from ScrapyKeeper.model.TemplateMange import TemplateMange
from ScrapyKeeper.model import db
from flask_restful import abort


class TemplateMangeSrv(object):
    @classmethod
    def add(cls, args: dict):
        try:
            # 保存数据
            return TemplateMange.save(args)
        except Exception as e:
            abort(500, message='Save template failed')

    @classmethod
    def list(cls):
        try:
            templates = TemplateMange.query.all()
            data = []
            for template in templates:
                template_dict = template.to_dict()
                data.append(template_dict)
            return data
        except Exception as e:
            db.session.rollback()
            print(e)
            abort(500, message='Fail to list template')

    @classmethod
    def delete(cls, id: int):
        try:
            template = TemplateMange.query.filter_by(id=id).first()
            if template:
                db.session.delete(template)
                db.session.commit()
        except Exception as e:
            abort(400, message='delete template failed')
