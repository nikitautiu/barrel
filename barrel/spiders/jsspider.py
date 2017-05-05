import scrapy_splash
from scrapy_splash import SplashRequest

from spiders.asbtract import AbstractSpider
from barrel.settings import DOWNLOADER_MIDDLEWARES, SPIDER_MIDDLEWARES


class JSYogaSpider(AbstractSpider):
    name = 'jsbarrelspider'
    custom_settings = {
        # modify appropriate settings
        'DOWNLOADER_MIDDLEWARES': DOWNLOADER_MIDDLEWARES.update({

            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810
        }),

        'SPIDER_MIDDLEWARES': SPIDER_MIDDLEWARES.update({
        'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
        }),

        'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter'

    }

    def build_request(self, url, start_url):
        req = SplashRequest(url, callback=self.parse)
        req.meta['start_url'] = start_url
        req.meta['splash']['slot_policy'] = scrapy_splash.SlotPolicy.SINGLE_SLOT
        return req
