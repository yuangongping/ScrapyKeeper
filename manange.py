#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : manange.py
# @Time    : 2020-4-28 14:15
# @Software: PyCharm
# @Author  : Taoz
# @contact : xie-hong-tao@qq.com
import os
import sys
sys.path.append(os.getcwd())

from ScrapyKeeper import app, db


def create_db():
    db.init_app(app)
    db.create_all()


if __name__ == '__main__':
    create_db()
