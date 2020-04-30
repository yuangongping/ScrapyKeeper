#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : router.py
# @Time    : 2020-4-28 14:11
# @Software: PyCharm
# @Author  : Taoz
# @contact : xie-hong-tao@qq.com
from ScrapyKeeper import restful_api
from ScrapyKeeper.controller.ProjectCtrl import ProjectCtrl


def regist_router():
    restful_api.add_resource(ProjectCtrl, "/project")
