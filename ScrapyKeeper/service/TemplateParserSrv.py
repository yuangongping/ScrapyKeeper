#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : TemplateParserSrv.py
# @Time    : 2020-5-12 14:32
# @Software: PyCharm
# @Author  : Taoz
# @contact : xie-hong-tao@qq.com
import json
import os
import re
import zipfile

from flask_restful import abort


class TemplateParserSrv(object):
    @classmethod
    def parse(cls, file_name: str, zip_bytes: bytes):
        path = cls.save_to_temp_dir(file_name, zip_bytes)
        try:
            return cls.parse_zip(path)
        except Exception as e:
            abort(400, message=str(e))


    @classmethod
    def save_to_temp_dir(cls, file_name: str, zip_bytes: bytes):
        """ 解压文件首先解压文件，并放置指定目录 """
        root_path = os.path.dirname(os.path.dirname(__file__))
        path = root_path + "/code_template/zip_temp/"

        # 保存模板的压缩文件
        with open(path + file_name, 'wb') as f:
            f.write(zip_bytes)
        return path + file_name

    @classmethod
    def parse_zip(cls, path):
        file = zipfile.ZipFile(path)
        name_list = file.namelist()
        # 首先检查有几个根目录，只能有一个根目录
        top_dir_exp = re.compile('\w+/$')
        top_dir_num = 0
        top_dir = None

        # 检查是否有generator.py
        generator_py = None
        generator_exp = re.compile('\w+/generator.py')

        # 检查是否有config.py
        config_py = None
        config_exp = re.compile('\w+/config.py')

        for name in name_list:
            if re.match(top_dir_exp, name):
                top_dir_num += 1
                top_dir = name

            if re.match(generator_exp, name):
                generator_py = name

            if re.match(config_exp, name):
                config_py = name

        if top_dir_num != 1:
            file.close()
            raise FileExistsError('模板存在多个根目录')
        if generator_py is None:
            file.close()
            raise FileNotFoundError('模板没有 generator.py')
        if config_py is None:
            file.close()
            raise FileNotFoundError('模板没有 config_py.py')
        else:
            byte = file.read(config_py)
            s = byte.decode(encoding='utf-8')
            m = re.search('config = ((.|\n|\r)*)', s)
            if m:
                try:
                    config = json.loads(m.group(1))
                    config['name'] = top_dir.replace('/', '')

                    assert type(config['type']) == int, 'config配置文件，没有 type模板类型'
                    assert type(config['name_zh']) == str, 'config配置文件，没有 name_zh 中文名称'

                    for key in config['tpl_input']:
                        assert config['tpl_input'][key].get('tip') is not None, '模板输入中没有 tip 字段（输入提示）'
                        assert config['tpl_input'][key].get('value') is not None, '模板输入中没有 value 字段（预输入值）'

                    return config
                except Exception as e:
                    raise ValueError('解析 tpl_input.py 失败，请检查模板, Error: %s' % str(e))
                finally:
                    file.close()
            else:
                file.close()
                raise ValueError('解析 tpl_input.py 失败，请检查模板')
