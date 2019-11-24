#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pymongo
import pandas as pd
from springer_scrapy.settings import date_count

client = pymongo.MongoClient('47.52.38.70', 27017)
db = client['springer']
collection = db['springer']

r = collection.find({'date_count': date_count})

dataframe = pd.DataFrame(r)
# 将DataFrame存储为csv,index表示是否显示行名，default=True
dataframe.to_excel('springer' + date_count, columns=['name', 'mail', 'journal', 'source', 'url', 'address'],
                   index=False)
