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
from flask import Response
from xpinyin import Pinyin
from flask_restful import abort
from ScrapyKeeper.agent.ScrapyAgent import ScrapyAgent
from ScrapyKeeper.model.ServerMachine import ServerMachine
from ScrapyKeeper.model.Project import Project
from ScrapyKeeper.model.Spider import Spider, db
from ScrapyKeeper.utils.scrapy_generator import TemplateGenerator
from ScrapyKeeper.utils.ThreadWithResult import ThreadWithResult
from ScrapyKeeper.service.LogManageSrv import LogManageSrv
from ScrapyKeeper.model.TemplateMange import TemplateMange


class ProjectSrv(object):
    def __init__(self):
        master_url = ServerMachine.master_url()
        if master_url is None:
            abort(500, message="No master server machine")
        slave_urls = ServerMachine.slave_urls()
        self.master_agent = ScrapyAgent(master_url)
        self.slave_agents = [ScrapyAgent(url) for url in slave_urls]

    def add_project(self, args: dict):
        template = args.get('category')
        name_zh = args.get('project_alias')
        name_zh = re.findall("[\u4e00-\u9fa5]+", name_zh)
        if name_zh:
            name_zh = ''.join(name_zh)
        else:
            abort(400, message="请输入中文的项目名！")
        pinyin = Pinyin()
        name_en = pinyin.get_pinyin(name_zh)
        name_en = ''.join(name_en.split("-"))
        egg_path = TemplateGenerator.create(
            name_en=name_en,
            name_zh=name_zh,
            template=template
        )
        # if egg_path and egg_path.get("slave") and egg_path.get("master"):
        #     deploy_status = self.deploy(
        #         project={"is_msd": 1, "project_name": name_en,
        #              "project_alias": name_zh, "category": template
        #         },
        #         egg_bytes_master=open(egg_path.get("master"), "rb"),
        #         egg_bytes_slave=open(egg_path.get("slave"), "rb")
        #     )
        #     if deploy_status:
        #         self.sync_spiders(args={"project_name": deploy_status.get("project_name")})

    def edit_project(self, args: dict):
        return Project.save(dic=args)

    def get_all_projects(self, args: dict):
        self.update_all_spider_running_status()
        projects = Project.get(page_index=args.get("page_index"),
                               page_size=args.get("page_size"))
        log_error_list = LogManageSrv.log_count()
        for index, project in enumerate(projects.get("data")):
            spider = Spider.query.filter_by(project_id=project.get("id"), type="slave").first()
            status = "pending"
            for slave_agent in self.slave_agents:
                if slave_agent.server_url == spider.address:
                    status = slave_agent.job_status(
                        spider.project_name,
                        spider.job_id
                    )
                    break
            projects["data"][index]["status"] = status
            projects["data"][index]["error"] = 0
            for log_err in log_error_list:
                if project["project_name"] in log_err["key"]:
                    projects["data"][index]["error"] = log_err["doc_count"]
        return projects

    def del_projects(self, args: dict):
        # 删除srcapyd主服务器的指定工程下的所有版本
        if self.master_agent.del_project(args.get("project_name")):
            # 遍历srcapyd从服务器， 删除的指定工程下的所有版本
            for agent in self.slave_agents:
                if not agent.del_project(args.get("project_name")):
                    abort(500, message="删除节点：{} 时出现错误！".format(agent.server_url))
        # 删除系统上的数据库

        Project.delete(filters={"id": args.get("id")})
        Spider.delete(filters={"project_id": args.get("id")})
        return "已删除工程！"

    def deploy(self, project: dict, egg_bytes_master: BinaryIO, egg_bytes_slave: BinaryIO = None) -> dict:
        if egg_bytes_slave is not None and project['is_msd'] == 1:
            version = int(time.time())
            proj = self.master_agent.deploy(project['project_name'], version, egg_bytes_master)

            threads = []
            for agent in self.slave_agents:
                t = ThreadWithResult(target=agent.deploy, args=(
                    project['project_name'],
                    version,
                    egg_bytes_slave
                ))
                threads.append(t)
                t.start()
            for t in threads:
                t.join()
            slaved_res = [t.get_result() for t in threads]

            if proj and any(slaved_res):
                Project.save(project)
                return project
            else:
                abort(500, message="Deploy Failed")

    def sync_spiders(self, args: dict):
        # 获取工程id
        project_instance = Project.query.filter_by(project_name=args.get("project_name")).first()
        # 获取工程下的蜘蛛列表, 然后更新至数据库
        spider_list = self.master_agent.list_spiders(args.get("project_name"))
        master_spider_name = spider_list[0] if spider_list else None
        # 更新数据库
        Spider.save({
            "name": master_spider_name,
            "project_id": project_instance.id,
            "project_name": project_instance.project_name,
            "type": "master",
            "address": self.master_agent.server_url
        })

        # 遍历从服务器节点， 当获取到从爬虫名时，跳出循环
        for slave_agent in self.slave_agents:
            slave_spider_name_list = slave_agent.list_spiders(args.get("project_name"))
            slave_spider_name = slave_spider_name_list[0] if slave_spider_name_list else None
            # 更新数据库
            Spider.save({
                "name": slave_spider_name,
                "project_id": project_instance.id,
                "project_name": project_instance.project_name,
                "type": "slave",
                "address": slave_agent.server_url
            })

    def update_all_spider_running_status(self):
        projects = Project.query.all()
        for project in projects:
            spiders = Spider.query.filter_by(type="slave", project_id=project.id).all()
            status = []
            for spider in spiders:
                for slave_agent in self.slave_agents:
                    if slave_agent.server_url == spider.address:
                        _status = slave_agent.job_status(
                            spider.project_name,
                            spider.job_id
                        )
                        status.append(_status)
            if "running" in status:
                project.status = "running"
            else:
                project.status = "pending"
            db.session.commit()

    def statistical_running_status(self):
        total = Project.query.all()
        running = Project.query.filter_by(status="running").all()
        return {
            "waitting": len(total) - len(running),
            "running": len(running)
        }
