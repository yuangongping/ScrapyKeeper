#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : router.py
# @Time    : 2020-4-28 14:11
# @Software: PyCharm
# @Author  : Taoz
# @contact : xie-hong-tao@qq.com
from ScrapyKeeper import restful_api
from ScrapyKeeper.controller.EmailCtrl import EmailCtrl
from ScrapyKeeper.controller.LogManageCtrl import LogManageCtrl
from ScrapyKeeper.controller.ServerMachineCtrl import ServerMachineCtrl
from ScrapyKeeper.controller.ProjectCtrl import ProjectCtrl
from ScrapyKeeper.controller.ProjectDataTrendCtrl import ProjectDataTrendCtrl
from ScrapyKeeper.controller.SchedulerCtrl import SchedulerCtrl
from ScrapyKeeper.controller.OriginalLogCtrl import OriginalLogCtrl
from ScrapyKeeper.controller.DataCentralCtrl import DataCentralCtrl
from ScrapyKeeper.controller.DataStorageCtrl import DataStorageCtrl
from ScrapyKeeper.controller.SendEmailCtrl import SendEmailCtrl
from ScrapyKeeper.controller.TemplateMangeCtrl import TemplateMangeCtrl
from ScrapyKeeper.controller.StartUrls import StartUrlsCtrl
from ScrapyKeeper.controller.RedisCtrl import RedisCtrl
from ScrapyKeeper.controller.DataExampleCtrl import DataExampleCtrl
from ScrapyKeeper.controller.TemplateParserCtrl import TemplateParserCtrl
from ScrapyKeeper.controller.ProxyIpAgencyCtrl import ProxyIpAgencyCtrl
from ScrapyKeeper.controller.ProxyIpCtrl import ProxyIpCtrl


def regist_router():
    restful_api.add_resource(LogManageCtrl, '/log_manage/error')
    restful_api.add_resource(ServerMachineCtrl, '/server_machine')
    restful_api.add_resource(ProjectCtrl, "/project")
    restful_api.add_resource(SchedulerCtrl, "/scheduler")
    restful_api.add_resource(OriginalLogCtrl, "/original_log")
    restful_api.add_resource(DataCentralCtrl, "/data_central")
    restful_api.add_resource(DataStorageCtrl, "/data_storage")
    restful_api.add_resource(SendEmailCtrl, "/send_email")
    restful_api.add_resource(TemplateMangeCtrl, "/template")
    restful_api.add_resource(StartUrlsCtrl, "/start_urls")
    restful_api.add_resource(ProjectDataTrendCtrl, "/data_trend")
    restful_api.add_resource(RedisCtrl, "/redis")
    restful_api.add_resource(DataExampleCtrl, "/data_example")
    restful_api.add_resource(TemplateParserCtrl, '/template_parser')
    restful_api.add_resource(ProxyIpAgencyCtrl, '/proxy_ip_agency')
    restful_api.add_resource(EmailCtrl, '/email')
    restful_api.add_resource(ProxyIpCtrl, '/proxy_ip')

