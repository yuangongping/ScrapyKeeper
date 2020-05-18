#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : Email.py
# @Time    : 2020-5-17 16:41
# @Software: PyCharm
# @Author  : Taoz
# @contact : xie-hong-tao@qq.com
from ScrapyKeeper.model import db, Base


class Email(Base):
    """  代理IP提供商 """
    __tablename__ = 'email'
    email = db.Column(db.String(255), comment='邮箱')
