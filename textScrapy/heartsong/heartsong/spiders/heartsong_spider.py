# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.selector import Selector
from heartsong.items import HeartsongItem  # 此处如果报错是pyCharm的原因
from scrapy.utils.project import get_project_settings
from scrapy import Request
import numpy as np


class HeartsongSpider(Spider):
    name = "heartsong"
    allowed_domains = ["51credit.com"]  # 允许爬取的域名，非此域名的网页不会爬取
    start_urls = []

    for line in open("data_spdb.txt", "r"):  # 设置文件对象并读取每一行文件
        start_urls.append(line.replace("\n", ""))  # 将每一行文件加入到list中

    settings = get_project_settings()

    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Host': 'bbs.51credit.com'
    }

    # 对请求的返回进行处理的配置
    meta = {
        'dont_redirect': True,  # 禁止网页重定向
        'handle_httpstatus_list': [301, 302]  # 对哪些异常返回进行处理
    }

    # 爬虫的起点
    def start_requests(self):
        # 带着cookie向网站服务器发请求，表明我们是一个已登录的用户
        for i in range(len(self.start_urls)):
            yield Request(self.start_urls[i], callback=self.parse,
                      headers=self.headers, meta=self.meta)


    def parse(self, response):
        selector = Selector(response)  # 创建选择器
        table = selector.xpath('//*[starts-with(@id, "pid")]')  # 取出所有的楼层
        for each in table:  # 对于每一个楼层执行下列操作
            item = HeartsongItem()  # 实例化一个Item对象
            item['title'] = selector.xpath('//*[@id="thread_subject"]/text()').extract()[0]
            item['author'] = \
                each.xpath(
                    'tr[1]/td[@class="pls"]/div[@class="pls favatar"]/div[@class="pi"]/div[@class="authi"]/a/text()').extract()[
                    0]
            item['post_time'] = \
                each.xpath('tr[1]/td[@class="plc"]/div[@class="pi"]').re(r'[0-9]+-[0-9]+-[0-9]+ [0-9]+:[0-9]+:[0-9]+')[
                    0]
            user_level = each.xpath('tr[1]/td[@class="pls"]/div[@class="pls favatar"]/p[1]/em/a/text()').extract()
            item['user_level'] = user_level[0] if user_level else np.nan
            item['user_exp'] = each.xpath('tr[1]/td[@class="pls"]/div[@class="pls favatar"]/dl[@class="pil cl"]/dd[1]/a/text()').extract()[0]
            item['user_thread'] = each.xpath('tr[1]/td[@class="pls"]/div[@class="pls favatar"]/dl[@class="pil cl"]/dd[2]/a/text()').extract()[0]
            item['user_comment'] = each.xpath('tr[1]/td[@class="pls"]/div[@class="pls favatar"]/dl[@class="pil cl"]/dd[3]/a/text()').extract()[0]
            item['user_currency'] = each.xpath('tr[1]/td[@class="pls"]/div[@class="pls favatar"]/dl[@class="pil cl"]/dd[4]/text()').extract()[0]
            item['user_register_time'] = each.xpath('tr[1]/td[@class="pls"]/div[@class="pls favatar"]/dl[@class="pil cl"]/dd[5]/text()').extract()[0]
            # content_quote = each.xpath('.//')
            content_list = each.xpath('.//td[@class="t_f"]/text()').extract()
            print(len(content_list))
            content = "".join(content_list)  # 将list转化为string
            item['url'] = response.url  # 用这种方式获取网页的url
            # 把内容中的换行符，空格等去掉
            item['content'] = content.replace('\r\n', '').replace(' ', '').replace('\n', '')

            yield item  # 将创建并赋值好的Item对象传递到PipeLine当中进行处理

        next_url = self.get_next_url(response.url)  # response.url就是原请求的url
        if next_url != None:  # 如果返回了新的url
            yield Request(next_url, callback=self.parse, headers=self.headers,
                                    meta=self.meta)
