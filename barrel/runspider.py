#!/bin/env python2.7
import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from helpers import get_urls_from_file
from spiders import BarrelSpider
from barrel.helpers import get_domain_from_url
from barrel.spiders.jsspider import JSBarrelSpider


def crawl(start_urls):
    # Crawl MySpider
    settings = get_project_settings()
    settings.set('FEED_URI', sys.argv[2], priority='cmdline')
    settings.set('FEED_FORMAT', 'jsonlines', priority='cmdline')
    settings.set('LOG_FILE', 'crawlall.log', priority='cmdline')
    settings.set('JOBDIR', './cache', priority='cmdline')
    settings.set('LOG_LEVEL', 'INFO', priority='cmdline')
    crawler = CrawlerProcess(settings=settings)

    crawler.crawl(JSBarrelSpider, start_urls=start_urls)
    crawler.start()

def main():
    crawl(get_urls_from_file(sys.argv[1]))

if __name__ == '__main__':
    main()