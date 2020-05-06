# -*- coding: utf-8 -*-
from ..items import *
from scrapy_redis.utils import bytes_to_str
from scrapy_redis.spiders import RedisSpider
from ..mysql_db.operate import session
from ..mysql_db.tables import Content
from ..utils.tools import *
import scrapy
from lxml import etree


class __ProjectNamecapitalize__SlaveSpider(RedisSpider):
    name = "{{project_name}}_slave_spider"
    redis_key = "{{project_name}}"
    session = session
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

    def make_request_from_data(self, data):
        """
        重写RedisCrawlSpider中的该算法, 以实现更多参数的传递
        :param data: redis数据库中获取的数据
        :return:
        """
        # 从redis数据库中获取详情页的url
        redis_data = json.loads(bytes_to_str(data, self.redis_encoding))
        url = redis_data.get('url')
        "在mysql中查询"
        exist = self.session.query(Content).filter_by(url=url).first()
        if not exist:
            return scrapy.Request(
                url=str(url),
                callback=self.parse_detail
            )

    def parse_detail(self, response):
        try:
            # 发帖子日期
            post_date = response.xpath("//div[@id='M_']//span[@class='ct']/text()").extract_first()
            post_date = time_fix(post_date) if post_date else getDateNow()

            # 由于多线程异步的原因，部分请求改由requests
            """    *************提取帖子的图片模块****************     """
            img = response.xpath("//div[@id='M_']//a[contains(text(),'组图共')]/@href").extract_first()
            # 如果帖子中存在多张图片
            if img:
                img = unify_url(response, img)
                res = requests.get(
                    url=img,
                    headers=self.headers
                )
                requests_response = etree.HTML(res.content)
                imgs = requests_response.xpath("//div[@class='c']/a[contains(text(),'原图')]/@href")
                file_group_uuids = []
                for img in imgs:
                    url = unify_url(response, img)
                    # 请求图片的地址， 获取图片文件
                    img_body = requests.get(url, headers=self.headers).content
                    uuid = upload(img_body)
                    if not uuid:
                        logging.info("文件上传失败！")
                        continue
                    file_group_uuids.append(uuid)
            else:
                file_group_uuids = []
                imgUrl = response.xpath("//div[@id='M_']//a[contains(text(),'原图')]/@href").extract_first()
                imgUrl = unify_url(response, imgUrl)
                img_body = requests.get(
                    url=imgUrl,
                    headers=self.headers,
                ).content
                uuid = upload(img_body)
                if uuid:
                    file_group_uuids.append(uuid)
            """    *************提取帖子的信息模块****************     """
            contentItem = __ProjectNamecapitalize__DetailItem()
            contentItem["publish_time"] = post_date

            # 转发数
            repost_count = response.xpath("//span/a[contains(text(),'转发[')]/text()").extract_first()
            if repost_count:
                repost_count = repost_count.replace("转发[", '').replace("]", '')
            else:
                repost_count = 0
            contentItem["repost_count"] = repost_count

            # 点赞数
            like_count = response.xpath("//span/a[contains(text(),'赞[')]/text()").extract_first()
            if like_count:
                like_count = like_count.replace("赞[", '').replace("]", '')
            else:
                like_count = 0
            contentItem["like_count"] = like_count

            # 评论数
            comment_count = response.xpath("//span/a[contains(text(),'评论')]/text()").extract_first()
            if comment_count:
                comment_count = comment_count.replace("评论[", '').replace("]", '')
            else:
                comment_count = 0
            contentItem["comment_count"] = comment_count

            # 帖子地址
            contentItem["url"] = response.url

            # 微博发送人用户名
            publisher = response.xpath("//div[@id='M_']/div[1]/a[1]/text()").extract_first()
            contentItem["publisher"] = publisher

            # 信息来源
            contentItem["source"] = response.meta.get("source")

            # 用户url
            publisher_url = response.xpath("//div[@id='M_']/div[1]/a[1]/href").extract_first()
            publisher_url = unify_url(response, publisher_url)
            contentItem["publisher_url"] = publisher_url

            # 微博内容
            content = ''.join(response.xpath("//div[1]/span[@class='ctt']//text()").extract())
            contentItem["content"] = content

            # 文件列表
            contentItem["file_group"] = json.dumps(file_group_uuids)
            yield contentItem

            """    *************提取帖子的评论模块****************     """
            url = response.url.replace("#cmtfrm", '&page=1')
            if not '&page=' in url:
                url += "&page=1"
            yield scrapy.Request(
                url=url,
                headers=self.headers,
                callback=self.parse_comment,
                dont_filter=True,
                meta={
                    "post_url": response.url
                }
            )
        except Exception as e:
            logging.info("******************")

    def parse_comment(self, response):
        comments = response.xpath("//div[@class='c'][starts-with(@id,'C_')]")
        for cmt in comments:
            commentItem = CommentItem()
            commentItem["content_uuid"] = cmt.xpath("@id").extract_first()
            commentItem["post_url"] = response.meta.get("post_url")
            name = cmt.xpath("a[1]/text()").extract_first()
            commentItem["name"] = name

            name_url = cmt.xpath("a[1]/@href").extract_first()
            commentItem["name_url"] = unify_url(response, name_url)

            content = ''.join(cmt.xpath("span[@class='ctt']//text()").extract())
            commentItem["content"] = content

            comment_object = cmt.xpath("span[@class='ctt']/a[1]/text()").extract_first() if "回复" in content else ''
            commentItem["comment_object"] = comment_object

            comment_object_url = cmt.xpath("span[@class='ctt']/a[1]/@href").extract_first() if "回复" in content else ''
            commentItem["comment_object_url"] = unify_url(response, comment_object_url)

            like_num = cmt.xpath("span/a[contains(text(),'赞[')]/text()").extract_first()
            if like_num:
                like_num = like_num.replace("赞[", '').replace("]", '')
            else:
                like_num = 0
            commentItem["like_num"] = like_num
            date = cmt.xpath("span[@class='ct']//text()").extract_first()
            date = date.split("来自")[0].strip()
            commentItem["date"] = time_fix(date) if date else getDateNow()
            yield commentItem
        page = response.xpath("//div[@id='pagelist']//a[contains(text(),'下页')]/@href").extract_first()
        if page:
            yield Request(
                url=unify_url(response, page),
                headers=self.headers,
                callback=self.parse_comment,
                meta={
                    "post_url": response.url
                }
            )
