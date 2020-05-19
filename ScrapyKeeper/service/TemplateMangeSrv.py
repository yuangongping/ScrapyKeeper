#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:chenlincui
from shutil import rmtree

from ScrapyKeeper.model.TemplateMange import TemplateMange
from ScrapyKeeper.model import db
from sqlalchemy import and_
from flask_restful import abort
import os
from ScrapyKeeper.utils.uzip import uzip
from werkzeug.utils import secure_filename


class TemplateMangeSrv(object):
    @classmethod
    def add(cls, args: dict, tpl_zip, file_name):
        # TODO 后端去做压缩包的检查，并返回给前端
        try:
            """ 解压文件首先解压文件，并放置指定目录 """
            root_path = os.path.dirname(os.path.dirname(__file__))
            path = root_path + "/code_template/zip_temp/"
            # 保存模板的压缩文件
            with open(path+"/"+file_name, 'wb') as f:
                f.write(tpl_zip)
                f.close()
            """ 解压文件 """
            tar_path = root_path + "/code_template/sources/"
            uzip(path+"/"+file_name, tar_path)
            # 保存数据
            return TemplateMange.save(args)
        except Exception as e:
            print(e)
            abort(400, message='数据已经存在')

    @classmethod
    def list(cls):
        return TemplateMange.all()

    @classmethod
    def delete(cls, id: int):
        try:
            template = TemplateMange.query.filter_by(id=id).first()
            if template:
                db.session.delete(template)
                db.session.commit()


            root_path = os.path.dirname(os.path.dirname(__file__))
            path = root_path + "/code_template/sources/{}".format(template.tpl_name)
            # 删除模板文件
            if os.path.exists(path):
               rmtree(path)
            return "删除成功！"
        except Exception as e:
            print(e)
            abort(400, message='delete template failed')

    # @classmethod
    # def update(cls, args: dict):
    #     # 首先删除文件
    #     root_path = os.path.dirname(os.path.dirname(__file__))
    #     if args.get("tpl_zip"):
    #         # 首先解压文件，并放置指定目录
    #         path = root_path + "/code_template/sources/{}".format(args.get("tpl_name"))
    #         os.rmdir(path)
    #
    #         # 重新创建文件目录
    #         path = root_path + "/code_template/zip_temp/{}".format(args.get("tpl_name"))
    #         if not os.path.exists(path):
    #             os.makedirs(path)
    #         # 保存模板的压缩文件
    #         file_name = secure_filename(args["tpl_zip"].filename)
    #         tpl_zip = args["tpl_zip"].stream.read()
    #         with open(path + "/" + file_name, 'wb') as f:
    #             f.write(tpl_zip)
    #             f.close()
    #         # 解压文件
    #         tar_path = root_path + "/code_template/sources/{}".format(args.get("tpl_name"))
    #         if not os.path.exists(tar_path):
    #             os.makedirs(tar_path)
    #         uzip(path + "/" + file_name, tar_path)
    #     obj = {
    #         "id": args.get("id"),
    #         "tpl_name": args.get("tpl_name"),
    #         "tpl_zh": args.get("tpl_zh"),
    #         "tpl_type": args.get("tpl_type"),
    #         "tpl_input": args.get("tpl_input") if args.get("tpl_input") else '',
    #         "tpl_img": args.get("tpl_img")
    #     }
    #     if args.get("tpl_img"):
    #         obj["tpl_img"] = obj["tpl_img"].stream.read()
    #     else:
    #         obj.pop("tpl_img")
    #     return TemplateMange.save()

    @classmethod
    def save(cls, args: dict):
        try:
            return TemplateMange.save(args)
        except Exception as err:
            abort(500, message=str(err))

    @classmethod
    def get_candidate(cls, args: dict):
        objs = TemplateMange.query.filter_by(
            name=args.get("name")
        ).all()
        return [{"crawl_name": obj.crawl_name, "crawl_url": obj.crawl_url} for obj in objs]
