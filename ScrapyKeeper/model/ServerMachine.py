#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : Server.py
# @Time    : 2020-4-28 14:58
# @Software: PyCharm
# @Author  : Taoz
# @contact : xie-hong-tao@qq.com
from ScrapyKeeper.model import db, Base


class ServerMachine(Base):
    __tabelename__ = 'sk_server_machine'
    url = db.Column(db.String(50), unique=True)
    status = db.Column(db.SmallInteger)
    is_master = db.Column(db.SmallInteger)

