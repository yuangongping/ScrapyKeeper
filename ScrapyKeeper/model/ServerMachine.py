#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : Server.py
# @Time    : 2020-4-28 14:58
# @Software: PyCharm
# @Author  : Taoz
# @contact : xie-hong-tao@qq.com
from sqlalchemy import and_

from ScrapyKeeper.model import db, Base


class ServerMachine(Base):
    __tabelename__ = 'sk_server_machine'
    url = db.Column(db.String(50), unique=True)
    status = db.Column(db.SmallInteger, default=1)  # 1启动 0禁用
    is_master = db.Column(db.SmallInteger)  # 1主 2从

    @classmethod
    def master_url(cls):
        sm = cls.query.filter(and_(cls.status == 1, cls.is_master == 1)).first()
        return sm.url if sm is not None else None

    @classmethod
    def slave_urls(cls):
        sms = cls.query.filter(and_(cls.status == 1, cls.is_master == 0)).all()
        return [sm.url for sm in sms]

