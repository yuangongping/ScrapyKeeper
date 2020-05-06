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
from ScrapyKeeper.controller.SchedulerCtrl import SchedulerCtrl
from ScrapyKeeper.controller.OriginalLogCtrl import OriginalLogCtrl
from ScrapyKeeper.controller.DataCentralCtrl import DataCentralCtrl
from ScrapyKeeper.controller.DataStorageCtrl import DataStorageCtrl
from ScrapyKeeper.controller.DataCountCtrl import DataCountCtrl



def regist_router():
    restful_api.add_resource(LogManageCtrl, '/log_manage/error')
    restful_api.add_resource(ServerMachineCtrl, '/server_machine')
    restful_api.add_resource(ProjectCtrl, "/project")
    restful_api.add_resource(SchedulerCtrl, "/scheduler")
    restful_api.add_resource(OriginalLogCtrl, "/original_log")
    restful_api.add_resource(DataCentralCtrl, "/data_central")
    restful_api.add_resource(DataStorageCtrl, "/data_storage")
    restful_api.add_resource(DataCountCtrl, "/data_count")


