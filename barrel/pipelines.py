# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv
import logging
import re

from scrapy import signals, Selector
from scrapy.exporters import JsonLinesItemExporter

from barrel.helpers import get_urls_from_file
from barrel.items import KeywordItem


class HtmlMatcher(object):
    """Class for matching text via xpath, css or regex"""
    def __init__(self, regex=r".*", css=None, xpath=None, collect=False):
        """Initializez the matcher
        
        Receives a regex patter for the text to search for. If unspecified, 
        matches everything. The css and xpath arguments are optional and mutually
        exclusive. If any is specified, the context is restricted to the matching 
        context
        """
        if xpath is not None and css is not None:
            raise ValueError('css and xpath are mutually exclusive')

        self.regex = re.compile(regex)
        self.css = css
        self.xpath = xpath
        self.collect = collect

    def parse(self, text):
        if not hasattr(text, 'xpath'):
            # this means it is not already a selector
            text = Selector(text=text)

        if self.css is not None:
            result = text.css(self.css).re(self.regex)
        elif self.xpath is not None:
            result = text.xpath(self.xpath).re(self.regex)
        else:
            result = text.re(self.regex)
        # either boolean or list
        if self.collect:
            return result
        return bool(result)


class HtmlExtractor(object):
    """Class """

class KeywordsFilter(object):
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(settings.get('EMAIL_PATTERN'), settings.getdict('KEYWORDS'))

    def __init__(self, email_pattern, keywords):
        self._items = {}
        self.keywords = keywords
        self.email_pattern = email_pattern

        kw_dict = self.keywords
        self.kw_patterns = {}  # dictionary of kw-pattern
        for kw, pattern in kw_dict.items():
            self.kw_patterns[kw] = re.compile(pattern)

    def process_item(self, item, spider):
        logging.info('Keyword pipeline: parsed item for \'%s\'',
                     item['url'])
        emails = list(
            re.findall(self.email_pattern, item['content']))  # get all emails

        return KeywordItem(url=item['url'],
                           start_url=item['start_url'],
                           keywords=self._extract_keywords(item['content']),
                           emails=emails)

    def _extract_keywords(self, text):
        # return a dict of keyword-(True/False) for all keywords
        matches = {kw: pattrn.search(text) is not None
                   for (kw, pattrn) in self.kw_patterns.items()}
        return matches
