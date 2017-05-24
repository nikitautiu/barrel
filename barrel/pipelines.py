import logging

from barrel.extractor import HtmlExtractor


class KeywordsFilter(object):
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(settings.get('COLLECT_ITEMS'), settings.getdict('KEYWORD_ITEMS'))

    def __init__(self, collect_items, keyword_items):
        # initialize keyword extractor
        self.item_extractor = HtmlExtractor(collect=collect_items,
                                            keywords=keyword_items)

    def process_item(self, item, spider):
        logging.info('Keyword pipeline: parsed item for \'%s\'',
                     item['url'])

        item['content'] = self.item_extractor.extract(item['content'])
        return item