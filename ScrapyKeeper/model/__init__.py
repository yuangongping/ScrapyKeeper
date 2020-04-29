#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : __init__.py.py
# @Time    : 2020-4-28 13:53
# @Software: PyCharm
# @Author  : Taoz
# @contact : xie-hong-tao@qq.com
from typing import List

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, Date, Numeric

from ScrapyKeeper import app

db = SQLAlchemy(app, session_options=dict(autocommit=False, autoflush=True))
db.init_app(app)


@app.teardown_request
def teardown_request(exception):
    if exception:
        db.session.rollback()
        db.session.remove()
    db.session.remove()


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    def to_dict(self) -> "dict":
        dic = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(column.type, Date):
                value = value.strftime('%Y-%m-%d')
            elif isinstance(column.type, DateTime):
                value = value.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(column.type, Numeric):
                value = float(value)
            dic[column.name] = value
        return dic

    def set(self, dic: dict):
        columns = [col.name for col in self.__table__.columns]
        for key, val in dic.items():
            if key not in columns:
                raise KeyError('%s has no column %s' % (self.__table__, key))
            else:
                setattr(self, key, val)

    @classmethod
    def save(cls, dic: dict) -> "Dict or None":
        if 'id' in dic:
            item = cls.query.filter(cls.id == dic['id']).first()
            if item is None:
                raise ValueError('Table %s has no data where id %s' % (cls.__table__, dic['id']))
            else:
                item.set(dic)
                dic = item.to_dict()
        else:
            new_one = cls()
            new_one.set(dic)
            db.session.add(new_one)
        db.session.commit()
        return dic

    @classmethod
    def find_by_id(cls, _id: int) -> 'cls or None':
        item = cls.query.filter(cls.id == _id).first()
        return item.to_dict() if item is not None else None

    @classmethod
    def all(cls, _to_dict: bool = True) -> "List":
        data = cls.query.all()
        return [item.to_dict() for item in data] if _to_dict else data
