from barrel.settings.settings import DOWNLOADER_MIDDLEWARES, SPIDER_MIDDLEWARES

DOWNLOADER_MIDDLEWARES.update({
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810
})

SPIDER_MIDDLEWARES.update({
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
})

DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'

SPLASH_URL = 'http://localhost:8050/'
