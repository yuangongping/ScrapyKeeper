#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : ProjectSrv.py
# @Time    : 2020-4-29 18:03
# @Software: PyCharm
# @Author  : Taoz
# @contact : xie-hong-tao@qq.com
import time
from typing import Dict
from flask_restful import abort
from ScrapyKeeper.agent.ScrapyAgent import ScrapyAgent
from ScrapyKeeper.model.ServerMachine import ServerMachine
from ScrapyKeeper.model.Project import Project
from ScrapyKeeper.utils.scrapy_generator import TemplateGenerator
import re
from xpinyin import Pinyin


class ProjectSrv(object):
    def __init__(self):
        master_url = ServerMachine.master_url()
        if master_url is None:
            abort(500, message="No master server machine")
        slave_urls = ServerMachine.slave_urls()
        self.master_agent = ScrapyAgent(master_url)
        self.slave_agents = [ScrapyAgent(url) for url in slave_urls]

    def add_project(self, args: object):
        url = args.url
        name_zh = args.name_zh
        template = args.template
        pinyin = Pinyin()
        name_en = pinyin.get_pinyin(
            re.findall("[\u4e00-\u9fa5]+", name_zh)[0]
        )
        name_en = ''.join(name_en.split("-"))
        egg_path = TemplateGenerator.create(
            url=url, name_en=name_en,
            name_zh=name_zh, template=template
        )
        if egg_path and egg_path.get("slave") and egg_path.get("master"):
            return self.deploy(
                project={"is_msd": 1, "project_name": name_en},
                egg_bytes_master=open(egg_path.get("master"), "rb"),
                egg_bytes_slave=open(egg_path.get("slave"), "rb")
            )

    def del_projects(self, args: object):
        # 删除srcapyd主服务器的指定工程下的所有版本
        if self.master_agent.del_project(args.project_name):
            # 遍历srcapyd从服务器， 删除的指定工程下的所有版本
            for agent in self.slave_agents:
               if not agent.del_project(args.project_name):
                    abort(500, message="删除节点：{} 时出现错误！".format(agent.server_url))
        # 删除系统上的数据库
        Project.delete(id=args.id)
        return "已删除工程！"

    def deploy(self, project: dict, egg_bytes_master: bytes, egg_bytes_slave: bytes = None) -> dict:
        if egg_bytes_slave is not None and project['is_msd'] == 1:
            version = int(time.time())
            proj = self.master_agent.deploy(project['project_name'], version, egg_bytes_master)
            proj_slaves = [agent.deploy(project['project_name'], version, egg_bytes_slave)
                           for agent in self.slave_agents]
            if proj and any(proj_slaves):
                Project.save(project)
                return project
            else:
                abort(500, message="Deploy Failed")