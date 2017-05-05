# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import re

import csv

from items import KeywordItem
from scrapy import signals
from scrapy.exporters import JsonLinesItemExporter

from helpers import get_urls


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


class JsonExportPipeline(object):
    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open('interm_results.json', 'w+b')
        self.files[spider] = file
        self.exporter = JsonLinesItemExporter(file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class ReducePipeline(object):
    def __init__(self):
        self._items = {}
        self._urls = get_urls('urls.txt')

        # populate collected fields
        self._collected = {}
        for url in self._urls:
            # the empty dict
            item_dict = {'emails': set()}
            item_dict.update({kw: False for kw in self.kerywords.keys().keys()})

            self._collected[url] = item_dict

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_closed(self, spider):
        with open('results.csv', 'w+b') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',',
                                   quotechar="'", quoting=csv.QUOTE_MINIMAL)

            # build each row and output it to csv
            csvwriter.writerow(['Domain', 'Email'] + self.kerywords.keys())
            for row in self.build_rows():
                csvwriter.writerow(row)

    def build_rows(self):
        """Build rows from the collected data"""
        for url in self._urls:
            item_dict = self._collected[url]

            # build the kw columns
            kw_checks = [item_dict[kw_name] for kw_name in self.kerywords.keys()]
            email_list = ' '.join(
                item_dict['emails'])  # join the unique emails with spaces
            row_list = [url, email_list] + kw_checks

            logging.info('Procesing Pipeline: wrote: %s', url)
            # write it line by line to the file
            yield row_list

    def process_item(self, item, spider):
        for kw in self.kerywords.keys():
            if item['keywords'][kw]:
                # toggle all available keywords
                self._collected[item['start_url']][kw] = True
        self._collected[item['start_url']]['emails'] |= set(item['emails'])
        return item
