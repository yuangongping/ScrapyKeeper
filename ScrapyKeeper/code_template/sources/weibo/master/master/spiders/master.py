# -*- coding: utf-8 -*-
from ..items import *
import time
import json
import scrapy
import logging
from ..utils.tools import *


class __ProjectNamecapitalize__Spider(scrapy.Spider):
    # 爬虫名
    name = "{{project_name}}_master_spider"
    url = "{{start_url}}"
    handle_httpstatus_list = [301, 302]
    login_headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "passport.weibo.cn",
        "Origin": "https://passport.weibo.cn",
        "Referer": "https://passport.weibo.cn/signin/login?entry=mweibo&r=https%3A%2F%2Fweibo.cn&u=5iyouth&_T_WM=ab1c331c1c20b484cd16a6f3b0c1dc64",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
    }
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "max-age=0",
        "referer": "https://weibo.cn/",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
    }
    currentDate = int(time.time())
    url_login = "https://passport.weibo.cn/sso/login"
    firstCrawl = True

    def start_requests(self):
        """
        登录完成后，访问首页地址
        :param response:
        :return:
        """
        data_dict = {
            "username": "1030617785@qq.com",
            "password": "YGPCHQ19920612",
            'savestate': '1',
            'r': 'https: //weibo.cn/',
            'ec': '0',
            'pagerefer': "",
            'entry': 'mweibo',
            'wentry': '',
            'loginfrom': '',
            'client_id': '',
            'code': '',
            'qq': '',
            'mainpageflag': '1',
            'hff': '',
            'hfp': ''
        }
        yield scrapy.FormRequest(
            url=self.url_login,
            headers=self.login_headers,
            formdata=data_dict,
            callback=self.login
        )

    def login(self, response):
        # 对响应体判断是否登录成功
        json_res = json.loads(response.text)
        if json_res["retcode"] == 20000000:
            source = "project_alias"
            yield scrapy.Request(
                url=self.url,
                headers=self.headers,
                callback=self.parse_page,
                dont_filter=True
            )
        else:
            logging.error("登录失败！")

    def parse_page(self, response):
        """*********** 帖子的列表页翻页 ********"""
        totalPageList = response.xpath("//div[@id='pagelist']//text()").extract()
        totalPage = extract_total_page(totalPageList)
        if totalPage:
            for page in range(1, totalPage):
                yield scrapy.Request(
                    url=response.url + "?page={}".format(page),
                    headers=self.headers,
                    callback=self.paser_post_list,
                    dont_filter=True,
                    meta=response.meta
                )

    def paser_post_list(self, response):
        # 获取所有帖子的列表，剔除第一个，第一个为首页|消息|话题|搜索|刷新等的菜单栏
        post_dom = response.xpath("//div[@class='c'][@id]")
        for post in post_dom:
            # 详情页的地址
            detail_url = post.xpath("div/a[contains(text(),'评论[')]/@href").extract_first()
            # 帖子的发布时间
            date = post.xpath("div/span[@class='ct']/text()").extract_first()
            date = date.split("来自")[0].strip()
            # 时间转成字符串
            date = time_fix(date)
            # 转成时间戳
            date = dateStr2DateStamp(date)
            # 如果首次采集， 则进行全量采集， 否则只是采集当天数据
            if firstCrawl:
                item = {{project_name_capitalize}}
                item['url'] = detail_url
                yield item
            else:
                if self.currentDate - date < 24*3700:
                    item = {{project_name_capitalize}}
                    item['url'] = detail_url
                    yield item
                else:
                    return


