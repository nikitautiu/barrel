import scrapy_splash
from scrapy_splash import SplashRequest

from barrel.settings import jssettings
from barrel.spiders.abstract import AbstractSpider


class JSBarrelSpider(AbstractSpider):
    name = 'jsbarrelspider'
    custom_settings = vars(jssettings)  # dict from module

    def _build_request(self, url, start_url):
        req = SplashRequest(url, callback=self.parse)
        req.meta['start_url'] = start_url
        req.meta['splash']['slot_policy'] = scrapy_splash.SlotPolicy.PER_DOMAIN
        return req
