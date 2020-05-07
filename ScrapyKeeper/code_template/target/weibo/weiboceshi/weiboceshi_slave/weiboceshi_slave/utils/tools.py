import os
import re
import logging
from scrapy.utils.response import get_base_url
from urllib.parse import urljoin
from scrapy.http import Response
import requests
import json
import datetime


def time_fix(time_string):
    now_time = datetime.datetime.now()
    if '分钟前' in time_string:
        minutes = re.search(r'^(\d+)分钟', time_string).group(1)
        created_at = now_time - datetime.timedelta(minutes=int(minutes))
        return created_at.strftime('%Y-%m-%d %H:%M:%S')

    if '小时前' in time_string:
        minutes = re.search(r'^(\d+)小时', time_string).group(1)
        created_at = now_time - datetime.timedelta(hours=int(minutes))
        return created_at.strftime('%Y-%m-%d %H:%M:%S')

    if '今天' in time_string:
        time_string = time_string + ":00"
        return time_string.replace('今天', now_time.strftime('%Y-%m-%d'))

    if '月' in time_string:
        time_string = time_string + ":00"
        time_string = time_string.replace('月', '-').replace('日', '')
        time_string = str(now_time.year) + '-' + time_string
        return time_string
    return time_string



def mrkdir(path):
    if not os.path.isdir(path):
        mrkdir(os.path.split(path)[0])
    else:
        return
    os.mkdir(path)


def unify_date(date_str):
    '''
    功能:处理时间为统一格式
    :param data: str 时间字符串
    :return:
    '''
    if not date_str:
        return None
    date = re.search(r'(\d+(\-|年|/)\d+(\-|月|/)\d+)', date_str)
    if date:
        date = date.group()
        return re.sub('年|月|/', '-', date)


def draftdate_from_textlines(textlines):
    """
    在正文里面去提取成文日期
    :param textlines: 正文的每一行
    :return: 提取结果
    """
    if textlines:
        textlines.reverse()
        for line in textlines:
            line = line.strip()
            is_date = re.search(r'^\d+年\d+月\d+日$', line)
            if is_date:
                return unify_date(is_date.group())


def del_quote(s):
    """
    删除字符串中的中英文冒号
    :param s: str
    :return: str
    """
    return re.sub(':|：', '', s)


def unify_url(response, url):
    """
    标准化url路径 （绝对路径和相对路径都会转换成绝对路径）
    :param response: scrapy.Response
    :param url: url
    :return:
    """
    if not isinstance(response, Response):
        logging.error("[** ERROR **] function unify_path(response, url) "
                      "papram response is not instance of scrapy.Response")
    return urljoin(get_base_url(response), url)



def upload(files):
    res = requests.post(
        url="http://172.16.119.13/dcy-file/fdfs/upload",
        files={'file': files}
    )
    res = json.loads(str(res.content, encoding="utf-8"))
    return res["result"]["fileUuid"] if res["msg"] == "成功" else ''


def getDateNow():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

