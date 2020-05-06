#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : Spider.py
# @Time    : 2020-4-29 14:57
# @Software: PyCharm
# @Author  : Taoz
# @contact : xie-hong-tao@qq.com
from ScrapyKeeper.model import db, Base


class Spider(Base):
    __tablename__ = 'spider'
    name = db.Column(db.String(100))
    project_id = db.Column(db.INTEGER, nullable=False, index=True)
    project_name = db.Column(db.String(100))
    type = db.Column(db.String(50))
    address = db.Column(db.String(100))
    job_id = db.Column(db.String(255))

