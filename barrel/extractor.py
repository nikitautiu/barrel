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
from scrapy.http import HtmlResponse

from barrel.helpers import get_urls_from_file
from barrel.items import KeywordItem


class HtmlMatcher(object):
    """Class for matching text via xpath, css or regex"""
    def __init__(self, regex=r".+", css=None, xpath=None, collect=False):
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
            extracted = text.css(self.css).extract()
        elif self.xpath is not None:
            extracted = text.xpath(self.xpath).extract()
        else:
            if type(text) is Selector:
                extracted = [text.extract()]
            else:
                extracted = [text.text]


        result = []
        for extracted_str in extracted:
            for match in self.regex.finditer(extracted_str):
                result.append(match.group(0))

        if self.collect:
            return result
        return bool(result)


class HtmlExtractor(object):
    """Class for extracting/collecting from an html text"""
    def __init__(self, collect, keywords):
        """Initiliazes the extractor
        
        Receives two dictionaries with the following form:
        ``{name: matcher}`` where  matcher can be either a string representing
        a regex to match or a dictionary of keyword arguments to pass to a 
        matcher.
        Ex: ``{"name": ".Ana.", "addr": {"css": ".class1", "regex": r".*"}}``
        
        The first dict is for collected items, the second one for keywords.
        """
        self.matchers = {}
        # add collectors
        for name, args in collect.items():
            if type(args) is not dict:
                args = {'regex': args}
            self.matchers[name] = HtmlMatcher(collect=True, **args)

        # add bool extractors
        for name, args in keywords.items():
            if type(args) is not dict:
                args = {'regex': args}
            self.matchers[name] = HtmlMatcher(collect=False, **args)

    def extract(self, text):
        if not hasattr(text, 'xpath'):
            # this means it is not already a selector
            text = Selector(text=text)
        return {name: matcher.parse(text)
                for name, matcher in self.matchers.items()}
