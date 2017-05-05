from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider

from barrel.helpers import get_domain_from_url
from barrel.items import PageItem


class AbstractSpider(CrawlSpider):
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        # workaround to pass the settings in the initializer so we can
        # setup the spider
        spider = cls(crawler.settings, *args, **kwargs)
        spider._set_crawler(crawler)
        return spider

    def __init__(self, settings, *args, **kwargs):
        super(AbstractSpider, self).__init__(*args, **kwargs)

        # keep the first url, this ensure that we know where we
        # should have started, regardless of redirects
        self.start_urls = settings.getlist('START_URLS', None)

        # just get the domain part of the url```
        # do not enforce domains spider wide, just for this one
        # non frame links should not traverse domains
        self.allowed_domains = [get_domain_from_url(url)
                                for url in self.start_urls]
        self.link_extractor = LinkExtractor(unique=True,
                                            allow_domains=self.allowed_domains)
        # frames should be allow to traverse domains

        follow_frames = settings.getbool('FOLLOW_FRAMES', False)
        self.frame_link_extractor = None
        if follow_frames:
            self.frame_link_extractor = LinkExtractor(unique=True,
                                                      tags=('frame',),
                                                      attrs=('href', 'src'))

    def start_requests(self):
        # initiate all the requests with their start urls
        for url in self.start_urls:
            yield self.build_request(url, url)

    def parse(self, response):
        # get the first url
        # if it is not set set it to the current one.
        # otherwise, if recursing, propagate it via the meta
        start_url = response.meta.get('start_url', response.url)
        links = self.link_extractor.extract_links(response)
        if self.frame_link_extractor is not None:
            links += self.frame_link_extractor.extract_links(response)

        for link in links:
            yield self.build_request(link.url, start_url)

        yield PageItem(content=response.text, start_url=start_url,
                       url=response.url)