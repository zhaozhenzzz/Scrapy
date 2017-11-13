# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WuyouItem(scrapy.Item):
    jobname = scrapy.Field()
    salary = scrapy.Field()
    link = scrapy.Field()
    experience = scrapy.Field()
    address = scrapy.Field()
    comany_name = scrapy.Field()
    head_count = scrapy.Field()
    education_require = scrapy.Field()
    comany_size = scrapy.Field()
    job_require =scrapy.Field()
    release_date = scrapy.Field()
    # 增加一个反馈率字段
