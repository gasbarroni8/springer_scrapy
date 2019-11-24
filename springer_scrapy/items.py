# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpringerScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    name = scrapy.Field()
    mail = scrapy.Field()
    address = scrapy.Field()
    journal = scrapy.Field()
    source = scrapy.Field()
    url = scrapy.Field()
    date_count = scrapy.Field()
    pass
