# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.selector import Selector
from heartsong.items import HeartsongItem  # 此处如果报错是pyCharm的原因
from scrapy.conf import settings
from scrapy import Request


class HeartsongSpider(Spider):
    name = "heartsong"
    allowed_domains = ["51credit.com"]  # 允许爬取的域名，非此域名的网页不会爬取
    start_urls = []
    for line in open("data_spdb.txt", "r"):  # 设置文件对象并读取每一行文件
        # if len(start_urls) > 50:
        #     break
        start_urls.append(line.replace("\n", ""))  # 将每一行文件加入到list中

    # start_urls = [ "https://bbs.51credit.com/thread-5550455-2-1.html",
    #                "https://bbs.51credit.com/thread-5412263-1-1.html",
    #                "https://bbs.51credit.com/thread-4276521-1-1.html"]

    # start_urls = [
    #     "https://bbs.51credit.com/thread-5603226-1-1.html"
    #     # 起始url，此例只爬这一个页面
    # ]
    cookie = settings['COOKIE']  # 带着Cookie向网页发请求
    print(cookie)
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
            yield Request(self.start_urls[i], callback=self.parse, cookies=self.cookie,
                      headers=self.headers, meta=self.meta)

    #     # Request请求的默认回调函数
    # def parse(self, response):
    #     with open("check.html", "wb") as f:
    #         f.write(response.body)  # 把下载的网页存入文件


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
            # content_quote = each.xpath('.//')
            content_list = each.xpath('.//td[@class="t_f"]/text()').extract()
            print(len(content_list))
            content = "".join(content_list)  # 将list转化为string
            item['url'] = response.url  # 用这种方式获取网页的url
            # 把内容中的换行符，空格等去掉
            item['content'] = content.replace('\r\n', '').replace(' ', '').replace('\n', '')

            yield item  # 将创建并赋值好的Item对象传递到PipeLine当中进行处理

        pages = selector.xpath('//*[@id="pgt"]/div/div/label/span')
        if pages:  # 如果pages不是空列表，说明该主题帖分页
            pages = pages[0].re(r'[0-9]+')[0]  # 正则匹配出总页数
            print("This post has", pages, "pages")
            # response.url格式： https://bbs.51credit.com/thread-5603226-1-1.html
            # 子utl格式： https://bbs.51credit.com/thread-5603226-2-1.html
            tmp = response.url.split('-')  # 以=分割url
            # 循环生成所有子页面的请求
            for page_num in range(2, int(pages) + 1):
                # 构造新的url
                sub_url = tmp[0] + '-' + tmp[1] + '-' + str(page_num) + '-' + tmp[3]
                # 注意此处的回调函数是self.sub_parse,就是说这个请求的response会传到
                # self.sub_parse里去处理
                yield Request(sub_url, callback=self.sub_parse, headers=self.headers,
                              cookies=self.cookie, meta=self.meta)


    def sub_parse(self, response):
        """
        用以爬取主题贴除首页外的其他子页
        :param response:
        :return:
        """
        selector = Selector(response)
        table = selector.xpath('//*[starts-with(@id, "pid")]')  # 取出所有的楼层
        for each in table:
            item = HeartsongItem()  # 实例化一个item
            # 通过XPath匹配信息，注意extract（）方法返回的是一个list
            item['title'] = selector.xpath('//*[@id="thread_subject"]/text()').extract()[0]
            item['author'] = each.xpath(
                'tr[1]/td[@class="pls"]/div[@class="pls favatar"]/div[@class="pi"]/div[@class="authi"]/a/text()').extract()[
                0]
            item['post_time'] = \
            each.xpath('tr[1]/td[@class="plc"]/div[@class="pi"]').re(r'[0-9]+-[0-9]+-[0-9]+ [0-9]+:[0-9]+:[0-9]+')[0]
            content_list = each.xpath('.//td[@class="t_f"]/text()').extract()
            print(len(content_list))
            content = "".join(content_list)  # 将list转化为string
            item['url'] = response.url  # 用这种方式获取网页的url
            # 把内容中的换行符，空格等去掉
            item['content'] = content.replace('\r\n', '').replace(' ', '').replace('\n', '')

            yield item  # 将创建并赋值好的Item对象传递到PipeLine当中进行处理
