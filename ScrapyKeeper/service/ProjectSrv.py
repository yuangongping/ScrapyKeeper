#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : ProjectSrv.py
# @Time    : 2020-4-29 18:03
# @Software: PyCharm
# @Author  : Taoz
# @contact : xie-hong-tao@qq.com
import time
import re
from typing import BinaryIO

from xpinyin import Pinyin
from flask_restful import abort
from ScrapyKeeper.agent.ScrapyAgent import ScrapyAgent
from ScrapyKeeper.model.ServerMachine import ServerMachine
from ScrapyKeeper.model.Project import Project
from ScrapyKeeper.utils.scrapy_generator import TemplateGenerator
from ScrapyKeeper.utils.ThreadWithResult import ThreadWithResult


class ProjectSrv(object):
    def __init__(self):
        master_url = ServerMachine.master_url()
        if master_url is None:
            abort(500, message="No master server machine")
        slave_urls = ServerMachine.slave_urls()
        self.master_agent = ScrapyAgent(master_url)
        self.slave_agents = [ScrapyAgent(url) for url in slave_urls]

    def add_project(self, args: dict):
        url = args.get('url')
        name_zh = args.get('name_zh')
        template = args.get('template')
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

    def deploy(self, project: dict, egg_bytes_master: BinaryIO, egg_bytes_slave: BinaryIO = None) -> dict:
        if egg_bytes_slave is not None and project['is_msd'] == 1:
            version = int(time.time())
            proj = self.master_agent.deploy(project['project_name'], version, egg_bytes_master)

            threads = []
            for agent in self.slave_agents:
                t = ThreadWithResult(target=agent.deploy, args={
                    project['project_name'],
                    version,
                    egg_bytes_slave
                })
                threads.append(t)
                t.start()

            [t.join() for t in threads]
            slaved_res = [t.get_result() for t in threads]

            if proj and any(slaved_res):
                Project.save(project)
                return project
            else:
                abort(500, message="Deploy Failed")
