# -*- coding: utf-8 -*-
import requests
import json
from flask_restful import abort
from ScrapyKeeper.agent.ScrapyAgent import ScrapyAgent
from ScrapyKeeper.model.ServerMachine import ServerMachine
from ScrapyKeeper.model.Spider import Spider


class OriginalLogSrv(object):
    def __init__(self):
        master_url = ServerMachine.master_url()
        if master_url is None:
            abort(500, message="No master server machine")
        slave_urls = ServerMachine.slave_urls()
        self.master_agent = ScrapyAgent(master_url)
        self.slave_agents = [ScrapyAgent(url) for url in slave_urls]

    def view_log(self, args: dict):
        filters = {"project_id": args.get("id"), "type": "slave"}
        spiders = Spider.query.filter_by(**filters).all()
        text = ""
        for spider in spiders:
            for agent in self.slave_agents:
                if spider.address == agent.server_url:
                    log_url = agent.log_url(
                        spider.project_name,
                        spider.name,
                        spider.job_id
                    )
                    res = requests.get(log_url+".log")
                    res.encoding = 'utf8'
                    text += res.text
        return text.split('\n')
