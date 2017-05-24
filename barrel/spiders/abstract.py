from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider

from barrel.extractor import HtmlExtractor
from barrel.helpers import get_domain_from_url, get_urls_from_file
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
        """Initializes the spider.
        Receives the first argument, the crawler settings, passed from
        the ``from_crawler`` method."""
        super(AbstractSpider, self).__init__(*args, **kwargs)

        # keep the first url, this ensure that we know where we
        # should have started, regardless of redirects
        self.start_urls = self._get_url_list(settings)

        # just get the domain part of the url```
        # do not enforce domains spider wide, just for this one
        # non frame links should not traverse domains
        allowed_domains = [get_domain_from_url(url)
                           for url in self.start_urls]
        self.link_extractor = LinkExtractor(unique=True,
                                            allow_domains=allowed_domains)
        # frames should be allow to traverse domains

        follow_frames = settings.getbool('FOLLOW_FRAMES', False)
        self.frame_link_extractor = None
        if follow_frames:
            self.frame_link_extractor = LinkExtractor(unique=True,
                                                      tags=('frame',),
                                                      attrs=('href', 'src'))

        # initialize keyword extractor
        self.item_extractor = HtmlExtractor(collect=settings.getdict('COLLECT_ITEMS'),
                                            keywords=settings.getdict('KEYWORD_ITEMS'))

    def _get_url_list(self, settings):
        """Gets a list of urls to crawl from the setting parameters"""
        # START_URLS has priority
        start_url_list = settings.getlist('START_URLS', None)
        if start_url_list:
            return start_url_list

        # then the file
        start_url_file = settings.get('START_URLS_FILE', None)
        if start_url_file is not None:
            return get_urls_from_file(start_url_file)

        # no start urls if neither are specified
        return []

    def start_requests(self):
        # initiate all the requests with their start urls
        for url in self.start_urls:
            yield self._build_request(url, url)

    def parse(self, response):

        # get the first url
        # if it is not set set it to the current one.
        # otherwise, if recursing, propagate it via the meta
        start_url = response.meta.get('start_url', response.url)
        links = self.link_extractor.extract_links(response)

        if self.frame_link_extractor is not None:
            links += self.frame_link_extractor.extract_links(response)

        for link in links:
            yield self._build_request(link.url, start_url)

        yield PageItem(content=self.item_extractor.extract(response),
                       start_url=start_url,
                       url=response.url)

    def _build_request(self, url, start_url):
        """Builds a request to crawl ``url`` passing ``start_url`` as a
        meta argument"""
        raise NotImplementedError
