#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : __init__.py.py
# @Time    : 2020-4-28 13:53
# @Software: PyCharm
# @Author  : Taoz
# @contact : xie-hong-tao@qq.com
from flask_sqlalchemy import SQLAlchemy
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
