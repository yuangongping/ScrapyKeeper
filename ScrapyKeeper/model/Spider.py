#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : Spider.py
# @Time    : 2020-4-29 14:57
# @Software: PyCharm
# @Author  : Taoz
# @contact : xie-hong-tao@qq.com
from ScrapyKeeper.model import db, Base


class Spider(Base):
    __tablename__ = 'sk_spider'
    spider_name = db.Column(db.String(100))
    project_id = db.Column(db.INTEGER, nullable=False, index=True)
    spider_name_slave = db.Column(db.String(100))

