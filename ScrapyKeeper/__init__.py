#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : __init__.py.py
# @Time    : 2020-4-28 13:51
# @Software: PyCharm
# @Author  : Taoz
# @contact : xie-hong-tao@qq.com
import logging
import os
from threading import Lock

from flask import Flask, send_from_directory, render_template, jsonify
from flask_cors import CORS
from flask_restful import Api, abort
from ScrapyKeeper import config
from apscheduler.schedulers.background import BackgroundScheduler
ram_scheduler = BackgroundScheduler()
lock = Lock()

app = Flask(__name__)
restful_api = Api(app)
cors = CORS(app, resources=r'/*', supports_credentials=True)
app.config.from_object(config)
app.config['JSON_AS_ASCII'] = False

# Logging
log = logging.getLogger()
log.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
app.logger.setLevel(app.config.get('LOG_LEVEL', "INFO"))
app.logger.addHandler(handler)


@app.errorhandler(Exception)
def internal_error(error):
    print(error)
    abort(500, message=str(error))


@app.errorhandler(404)
def handle_404_error(err):
    """自定义的处理错误方法"""
    # 这个函数的返回值会是前端用户看到的最终结果
    return jsonify({
        'code': 404,
        'message': 'not found'
    })

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='favicon.icon')

# 注册路由
from .router import regist_router
regist_router()
# from ScrapyKeeper.service.SchedulerSrv import SchedulerSrv
# schedulerSrv = SchedulerSrv()
# schedulerSrv.add_existed_job_to_ram_scheduler()
ram_scheduler.start()
