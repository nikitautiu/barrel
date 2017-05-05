from scrapy import Request

from spiders.asbtract import AbstractSpider


class YogaSpider(AbstractSpider):
    name = 'barrelspider'

    def build_request(self, url, start_url):
        req = Request(url, callback=self.parse)
        req.meta['start_url'] = start_url
        return req

