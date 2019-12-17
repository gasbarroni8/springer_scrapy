#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pymongo
import pandas as pd
from springer_scrapy.settings import date_count, MONGO
import json

#本地数据库操作，连接，插入，关闭
class mongo_make(object):
    def __init__(self):
        # client = pymongo.MongoClient('mongodb://{}:{}@{}:{}'.format(MONGO['USER'], MONGO['PSWD'], MONGO['HOST'], MONGO['PORT']))
        self.client = pymongo.MongoClient('127.0.0.1', 27017)
        db = self.client['springer']
        self.collection = db['springer']

    def insert(self, data):
        self.collection.insert(data)

    def close(self):
        self.client.close()

#读取本地json文件到数组
def readJson(path):
    data_list = []
    with open(path, 'r', encoding='utf-8') as f:
        for data in f.readlines():
            d = json.loads(data)
            print(d)
            data_list.append(d)
    print(len(data_list))
    return data_list

#json数组保存到本地数据库
def saveJson_toMongo(data_list):
    mongo_obj = mongo_make()
    for data in data_list:
        if '_id' in data.keys():
            data.pop('_id')
        mongo_obj.insert(data)
    mongo_obj.close()

#云服务器最新数据保存到本地excel，追加到backup.json文件
def mongo_to_xlsx():
    client = pymongo.MongoClient(
        'mongodb://{}:{}@{}:{}'.format(MONGO['USER'], MONGO['PSWD'], '47.52.38.70', MONGO['PORT']))
    db = client['springer']
    collection = db['springer']
    r = collection.find({'date_count': date_count})
    df = pd.DataFrame(r)
    # 将DataFrame存储为xlsx,index表示是否显示行名，default=True
    df.to_excel('springer' + date_count, columns=['name', 'mail', 'journal', 'source', 'url', 'address'],
                index=False)

    #追加本期结果到backup.json
    r = collection.find({'date_count': date_count})
    Append_backup_toJson(r)

#把json数组追加到backup.json文件
def Append_backup_toJson(json_list):
    with open('backup.json', 'a') as f:
        for i in json_list:
            i.pop('_id')
            print(i)
            f.writelines(json.dumps(i)+'\n')

if __name__ == '__main__':

    mongo_to_xlsx()

    # path = 'backup.json'
    # data_list = readJson(path)
    # saveJson_toMongo(data_list)

    # r = collection.find({'mail': None}).count()
    # collection.delete_many({'mail': None})
    # print(r)

    #改excel
    #page
    #填日期
    #search?
    #search/page/{}?
    #settings 改变量名