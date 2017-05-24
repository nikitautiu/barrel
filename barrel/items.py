import scrapy


class PageItem(scrapy.Item):
    content = scrapy.Field()
    start_url = scrapy.Field()
    url = scrapy.Field()
