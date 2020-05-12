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
from ScrapyKeeper.code_template.ScrapyGenerator import ScrapyGenerator
from ScrapyKeeper.utils.ThreadWithResult import ThreadWithResult
from ScrapyKeeper.service.LogManageSrv import LogManageSrv
from sqlalchemy import and_


class ProjectSrv(object):
    def __init__(self):
        master_url = ServerMachine.master_url()
        if master_url is None:
            abort(500, message="No master server machine")
        slave_urls = ServerMachine.slave_urls()
        self.master_agent = ScrapyAgent(master_url)
        self.slave_agents = [ScrapyAgent(url) for url in slave_urls]

    def add_project(self, tmpl_name: str, tmpl_args: dict):
        pinyin = Pinyin()
        name_en = pinyin.get_pinyin(tmpl_args['project_name_zh'])
        tmpl_args['project_name'] = ''.join(name_en.split("-"))

        # TODO: 前端通过中文生成项目英文名并提交，存在相同英文名的时候，提醒用户自己手动修改英文名
        exist = Project.find_by_name(name_en)
        if exist:
            abort(400, message="存在相同的工程名称，请重新命名")
        egg_path = ScrapyGenerator.gen(tmpl_name, **tmpl_args)
        if egg_path.get('master') is not None:
            # 分布式
            if egg_path.get('slave') is not None:
                deploy_status = self.deploy(
                    project={"is_msd": 1, "project_name": tmpl_args['project_name'],
                             "project_name_zh": tmpl_args['project_name_zh'], "template": tmpl_name
                             },
                    egg_bytes_master=open(egg_path.get("master"), "rb"),
                    egg_bytes_slave=open(egg_path.get("slave"), "rb")
                )
            # 单机
            else:
                deploy_status = self.deploy(
                    project={"is_msd": 0, "project_name": tmpl_args['project_name'],
                             "project_name_zh": tmpl_args['project_name_zh'], "template": tmpl_name
                             },
                    egg_bytes_master=open(egg_path.get("master"), "rb"),
                    egg_bytes_slave=None
                )

            if deploy_status:
                Project.save({
                    "is_msd": 1,
                    "project_name": tmpl_args['project_name'],
                    "project_name_zh": tmpl_args['project_name_zh'],
                    "tpl_input": tmpl_args.get("tpl_input")})
                self.sync_spiders(tmpl_args['project_name'])
            else:
                abort(500, message="部署失败")
        else:
            abort(500, message="生成工程失败")

    def edit_project(self, args: dict):
        return Project.save(dic=args)

    def get_all_projects(self, args: dict):
        # self.update_all_spider_running_status()
        exp_list = []
        if args.get("project_name_zh"):
            words = args.get("project_name_zh").split(' ')
            for word in words:
                exp_list.append(Project.project_name_zh.like('%{}%'.format(word)))
        if args.get("status"):
            exp_list.append(Project.status == args.get("status"))
        if args.get("category"):
            exp_list.append(Project.category == args.get("category"))
        if args.get("project_name"):
            exp_list.append(Project.project_name == args.get("project_name"))
        order_exp = Project.date_created.desc()
        if len(exp_list) > 0:
            filter_exp = and_(*exp_list)
            pagination = Project.query.filter(filter_exp).order_by(order_exp).paginate(
                args.get("page_index"), args.get("page_szie"), error_out=False)
        else:
            pagination = Project.query.order_by(order_exp).paginate(args.get("page_index"), args.get("page_szie"), error_out=False)
        projects = [dataset.to_dict() for dataset in pagination.items]
        for index, project in enumerate(projects):
            projects[index]["time"] = "12点"
        log_error_list = LogManageSrv.log_count()
        # for index, project in enumerate(projects):
        #     spider = Spider.query.filter_by(project_id=project.get("id"), type="slave").first()
        #     status = "pending"
        #     for slave_agent in self.slave_agents:
        #         if slave_agent.server_url == spider.address:
        #             status = slave_agent.job_status(
        #                 spider.project_name,
        #                 spider.job_id
        #             )
        #             break
        #     projects[index]["status"] = status
        #     projects[index]["error"] = 0
        #     for log_err in log_error_list:
        #         if project["project_name"] in log_err["key"]:
        #             projects[index]["error"] = log_err["doc_count"]
        return {"total": pagination.total, "data": projects}

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
        # TODO dict 参数的代码优化
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

            return proj and any(slaved_res)

    def sync_spiders(self, project_name: str):
        # 获取工程id
        project = Project.find_by_name(project_name)
        # 获取工程下的蜘蛛列表, 然后更新至数据库
        spider_list = self.master_agent.list_spiders(project_name)
        master_spider_name = spider_list[0] if spider_list else None
        # 更新数据库
        Spider.save({
            "name": master_spider_name,
            "project_id": project.id,
            "project_name": project.project_name,
            "type": "master",
            "address": self.master_agent.server_url
        })

        # 遍历从服务器节点， 当获取到从爬虫名时，跳出循环
        for slave_agent in self.slave_agents:
            slave_spider_name_list = slave_agent.list_spiders(project_name)
            slave_spider_name = slave_spider_name_list[0] if slave_spider_name_list else None
            # 更新数据库
            Spider.save({
                "name": slave_spider_name,
                "project_id": project.id,
                "project_name": project.project_name,
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
