# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HeartsongItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()  # 帖子的标题
    url = scrapy.Field()  # 帖子的网页链接
    author = scrapy.Field()  # 帖子的作者
    post_time = scrapy.Field()  # 发表时间
    content = scrapy.Field()  # 帖子的内容
    user_level = scrapy.Field()  # 用户等级
    user_exp = scrapy.Field()  # 用户经验值
    user_thread = scrapy.Field()  # 用户发布的主题帖数目
    user_comment = scrapy.Field()  # 用户回复的帖子数目
    user_currency = scrapy.Field()  # 用户信用币数目
    user_register_time = scrapy.Field()  # 用户注册时间
