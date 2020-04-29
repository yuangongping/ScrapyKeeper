#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : __init__.py.py
# @Time    : 2020-4-28 13:51
# @Software: PyCharm
# @Author  : Taoz
# @contact : xie-hong-tao@qq.com
import logging
import os
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager
from flask_restful import Api
from ScrapyKeeper import config

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


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='favicon.icon')

# 注册路由
from .router import regist_router
regist_router()
