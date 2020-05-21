# -*- coding: utf-8 -*-
import requests
import json
from flask_restful import abort
from ScrapyKeeper.agent.ScrapyAgent import ScrapyAgent
from ScrapyKeeper.model.ServerMachine import ServerMachine
from ScrapyKeeper.model.JobExecution import JobExecution
from ScrapyKeeper.model.Spider import Spider


class ScrapydLogSrv(object):
    def __init__(self):
        master_url = ServerMachine.master_url()
        if master_url is None:
            abort(500, message="No master server machine")
        slave_urls = ServerMachine.slave_urls()
        self.master_agent = ScrapyAgent(master_url)
        self.slave_agents = [ScrapyAgent(url) for url in slave_urls]

    def view_master_log(self, scheduler_id: int):
        filters = {"scheduler_id": scheduler_id, "node_type": "master"}
        jobExe = JobExecution.query.filter_by(**filters).first()
        spider = Spider.query.filter_by(project_id=jobExe.project_id, type=jobExe.node_type).first()
        log_url = self.master_agent.log_url(
            spider.project_name,
            spider.name,
            jobExe.scrapyd_job_id
        )
        res = requests.get(log_url + ".log")
        res.encoding = 'utf8'
        text = res.text
        return text.split('\n')

    def view_slave_log(self, scheduler_id: int):
        filters = {"scheduler_id": scheduler_id, "node_type": "slave"}
        jobExe = JobExecution.query.filter_by(**filters).first()
        text = ""
        for agent in self.slave_agents:
            if agent.server_url == jobExe.scrapyd_url:
                spider = Spider.query.filter_by(project_id=jobExe.project_id, type=jobExe.node_type).first()
                log_url = agent.log_url(
                    spider.project_name,
                    spider.name,
                    jobExe.scrapyd_job_id
                )
                res = requests.get(log_url + ".log")
                res.encoding = 'utf8'
                text = res.text
                break
        return text.split('\n')
