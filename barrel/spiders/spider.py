from scrapy import Request

from barrel.spiders.abstract import AbstractSpider


class BarrelSpider(AbstractSpider):
    name = 'barrelspider'

    def _build_request(self, url, start_url):
        req = Request(url, callback=self.parse)
        req.meta['start_url'] = start_url
        return req
