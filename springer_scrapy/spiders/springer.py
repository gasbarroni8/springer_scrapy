# -*- coding: utf-8 -*-
import scrapy
import re
from springer_scrapy.items import SpringerScrapyItem
import random
from scrapy_redis.spiders import RedisSpider
import openpyxl
from springer_scrapy.settings import date_count


# scrapy crawl springer

class SpringerSpider(RedisSpider):
    name = 'springer'
    allowed_domains = ['link.springer.com']
    start_urls = ['http://link.springer.com/']

    redis_key = 'springer:start_urls'

    def start_requests(self):
        '''
        指定哪年的哪种期刊
        :return:
        '''
        wb = openpyxl.load_workbook(date_count)
        ws = wb["Sheet1"]
        for row in ws.rows:
            for i in range(1, int(row[3].value)):
                random.uniform(1, 3)
                self.logger.info(row[0].value.format(i))
                self.logger.info('现在是第' + str(i) + '页。')
                print(row[0].value.format(i))
                print('现在是第' + str(i) + '页。')
                yield scrapy.Request(url=row[0].value.format(i),
                                     meta={'download_timeout': 5, 'journal': row[1].value}, callback=self.parse,
                                     dont_filter=True)

    def parse(self, response):
        chapter_urls = response.xpath('//a[@class="title"]/@href').getall()
        for url in chapter_urls:
            self.logger.info(response.urljoin(url))
            print(response.urljoin(url))
            yield scrapy.Request(url=response.urljoin(url),
                                 meta={'download_timeout': 5, 'journal': response.meta['journal']},
                                 callback=self.parse_data,
                                 dont_filter=True)

    def parse_data(self, response):
        list = response.xpath('//li[@itemscope]').getall()
        email_set = set()
        for li in list:
            search_email = re.search('title="(.*?)" itemprop="email"', li, re.S)
            if search_email:
                email_set.add(search_email[1])
        for email in email_set:
            item = SpringerScrapyItem()
            for li in list:
                search_aff = re.search('data-affiliation.*?' + email, li, re.S)
                if search_aff:
                    search_name = re.search('class="authors-affiliations__name">(.*?)</span>', li, re.S)
                    search_address = re.search('data-affiliation="(.*?)"', li, re.S)
                    item['name'] = search_name[1]
                    item['mail'] = email
                    item['journal'] = response.meta['journal']
                    item['source'] = 'springer link'
                    item['url'] = response.url
                    for li in list:
                        if 'data-affiliation-highlight="' + search_address[1] + '"' in li:
                            search_add = []
                            if 'department' in li:
                                search_add.append(re.search('department">(.*?)</span>', li, re.S)[1])
                            if 'affiliation__name' in li:
                                search_add.append(re.search('affiliation__name">(.*?)</span>', li, re.S)[1])
                            if 'affiliation__city' in li:
                                search_add.append(re.search('affiliation__city">(.*?)</span>', li, re.S)[1])
                            if 'affiliation__country' in li:
                                search_add.append(re.search('affiliation__country">(.*?)</span>', li, re.S)[1])
                            item['address'] = ','.join(search_add)
                    item['date_count'] = date_count
            yield item
