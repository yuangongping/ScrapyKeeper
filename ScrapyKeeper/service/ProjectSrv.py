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

class ProjectSrv(object):
    def __init__(self):
        master_url = ServerMachine.master_url()
        if master_url is None:
            abort(500, message="No master server machine")
        slave_urls = ServerMachine.slave_urls()
        self.master_agent = ScrapyAgent(master_url)
        self.slave_agents = [ScrapyAgent(url) for url in slave_urls]

    def deploy(self, project: dict, egg_bytes_master: bytes, egg_bytes_slave: bytes = None) -> "Dict":
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




