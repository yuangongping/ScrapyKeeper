#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:chenlincui
from ..items import *
import re
import json
import requests
import scrapy
from ..utils.tools import *
from ..mysql_db.operate import session
from ..mysql_db.tables import Content


class __ProjectNamecapitalize__Spider(scrapy.Spider):
    name = "{{project_name}}_master_spider"
    session = session
    start_url = ''
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'CXID=A7DD9933B0064489336BA48EB827A2CF; SUID=5998556F4B238B0A5DF9BBFE0005D9B0; wuid=AAHbPABVLAAAAAqLFBt+XAQAGwY=; SMYUV=1585031329308125; IPLOC=CN5201; SUV=00268B006F5598595E7C77B1BB0E2017; ssuid=7659773268; sw_uuid=3944064983; ABTEST=3|1586942614|v1; weixinIndexVisited=1; ld=Wkllllllll2WK4WZlllllVfW$UclllllbCQYQyllll9lllllVylll5@@@@@@@@@@; pgv_pvi=974937088; LSTMV=360%2C22; LCLKINT=1735; ad=cTjkyZllll2WqG5elllllVfuk39lllllbCQYQyllllylllllph7ll5@@@@@@@@@@; SNUID=2CED23197573D07DBC00241D76BE34F6; JSESSIONID=aaahwi-nfijofaq81TRgx; sct=11',
        'Host': 'weixin.sogou.com',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
    }

    def start_requests(self):
        "在mysql中查询"
        for url_index in self.start_url:
            url = "https://weixin.sogou.com/weixin?query=%s" % url_index
            exist = self.session.query(Content).filter_by(url=url).first()
            if not exist:
                yield scrapy.Request(
                    url=url,
                    headers=self.header,
                    callback=self.parse_list,
                    dont_filter=True
                )

    def parse_list(self, response):
        """***********提取公众号最新一篇文章的url********"""
        url_index = response.xpath("//a[@uigs='account_article_0']/@href").extract_first()
        pub_time = re.findall("document.write\(timeConvert\('(\d+)'\)", response.text)
        title = response.xpath("//a[@uigs='account_article_0']/text()").extract_first()
        if url_index:
            yield scrapy.Request(
                url=response.urljoin(url_index),
                callback=self.parse_url,
                headers=self.header,
                meta={'create_time': pub_time[0] if pub_time else '',
                      'title': title}
            )

    def parse_url(self, response):
        url_list = re.findall("url \+= '(.*)';", response.text)
        if url_list:
            url = ''.join(url_list)
            yield scrapy.Request(
                url=url,
                callback=self.paser_detail,
                meta={'create_time': response.meta['create_time'],
                      'title': response.meta['title']}
            )

    def paser_detail(self, response):
        author_index = response.xpath('//strong[contains(text(),"作者")]/following-sibling::strong/text() | '
                                      '//span[contains(text(),"编辑")]/text()').extract_first()
        if '：' in author_index:
            author = author_index.split('：')[-1]
        elif '| ' in author_index:
            author = author_index.split('| ')[-1]
        else:
            author = author_index

        body = response.xpath('//div[@id="js_content"]').xpath('string(.)').extract_first()
        create_time = stamp_to_date(response.meta['create_time'])
        source = response.xpath('//a[@id="js_name"]/text()').extract_first()

        # 内容通用字段提取
        contentItem = __ProjectNamecapitalize__DetailItem()
        contentItem['title'] = response.meta['title']
        contentItem['author'] = author.strip() if author else ''
        contentItem['source'] = source.strip() if source else ''
        contentItem['body'] = body.strip() if body else ''
        contentItem['type'] = '文稿'
        contentItem['create_time'] = create_time
        contentItem['url'] = response.url
        file_group = []

        # 附件提取
        attachment = response.xpath('//div[@id="js_content"]//img/@data-src').extract()

        if not attachment:
            return

        for att in attachment[:-1]:
            att_url = response.urljoin(att)
            img_body = requests.get(url=att_url).content  # 请求附件url
            uuid = upload(img_body)
            if not uuid:
                logging.info("文件上传失败！")
                continue
            file_group.append(uuid)
            # attItem = AttItem()
            # attItem["id"] = uuid
            # attItem["name"] = uuid
            # attItem["type"] = "图片"
            # attItem["create_time"] = create_time
            # attItem["size"] = str(int(len(img_body) / 1024))
            # attItem["path"] = uuid
            # yield attItem

        # 附件下载完毕, 保存正文
        contentItem['file_group'] = json.dumps(file_group)
        yield contentItem
