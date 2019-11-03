# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import heartsong.settings
import csv


class HeartsongPipeline(object):
    # def process_item(self, item, spider):
    #     file = open("items.txt", "ab+")  # 以追加的方式打开文件，不存在则创建
    #     # 因为item中的数据是unicode编码的，为了在控制台中查看数据的有效性和保存，
    #     # 将其编码改为utf-8
    #     item_string = str(item).encode('utf-8')
    #     file.write(item_string)
    #     file.write('\n'.encode())
    #     file.close()
    #     # print (item_string)  #在控制台输出
    #     return item  # 会在控制台输出原item数据，可以选择不写

    def process_item(self, item, spider):
        f = open('item_spdb.csv', 'a+', newline="", encoding='utf-8')
        writer = csv.writer(f)
        # item = str(item).encode('utf-8')
        if item['author']:
            writer.writerow([item['author'],
                             item['content'],
                             item['post_time'],
                             item['title'],
                             item['url']])
        return item

