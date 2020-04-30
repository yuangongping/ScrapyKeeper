#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : router.py
# @Time    : 2020-4-28 14:11
# @Software: PyCharm
# @Author  : Taoz
# @contact : xie-hong-tao@qq.com
from ScrapyKeeper import restful_api
from ScrapyKeeper.controller.LogManageCtrl import LogManageCtrl
from ScrapyKeeper.controller.ServerMachineCtrl import ServerMachineCtrl
from ScrapyKeeper.controller.ProjectCtrl import ProjectCtrl
from ScrapyKeeper.controller.DataCountCtrl import DataCountCtrl


def regist_router():
    restful_api.add_resource(LogManageCtrl, '/log_manage/error')
    restful_api.add_resource(ServerMachineCtrl, '/server_machine')
    restful_api.add_resource(ProjectCtrl, "/project")
    restful_api.add_resource(DataCountCtrl, "/data_count")

