# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PageItem(scrapy.Item):
    content = scrapy.Field()
    start_url = scrapy.Field()
    url = scrapy.Field()


class KeywordItem(scrapy.Item):
    url = scrapy.Field()
    start_url = scrapy.Field()
    emails = scrapy.Field()
    keywords = scrapy.Field()


class ReducedItem(scrapy.Item):
    url = scrapy.Field()
    emails = scrapy.Field()
    keywords = scrapy.Field()