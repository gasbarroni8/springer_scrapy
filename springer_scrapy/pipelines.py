# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging

from springer_scrapy.settings import MONGO
import pymongo


class SpringerScrapyPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
    logger = logging.getLogger(__name__)
    def open_spider(self, spider):
        self.client = pymongo.MongoClient('mongodb://{}:{}@{}:{}'.format(MONGO['USER'], MONGO['PSWD'], MONGO['HOST'], MONGO['PORT']))
        self.db = self.client[MONGO['DB']]
        self.collection = self.db[MONGO['COLLECTION']]

    def process_item(self, item, spider):
        postItem = dict(item)  # 把item转化成字典形式
        # 查询数据，条件mail中的数量
        result = self.collection.find({'mail': {'$regex': item['mail'], '$options': 'i'}}).count()
        # 返回结果是0数据库中没有此数据
        if result == 0:
            self.collection.insert(postItem)  # 向数据库插入一条记录
            print('保存：' + item['name'] + ' ' + item['mail'])
            self.logger.info('保存：' + item['name'] + ' ' + item['mail'])
            return item
        else:
            print('已存在：' + item['name'] + ' ' + item['mail'])
            self.logger.info('已存在：' + item['name'] + ' ' + item['mail'])

    def close_spider(self, spider):
        self.client.close()
