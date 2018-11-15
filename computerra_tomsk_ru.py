import logging
import re

import coloredlogs
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from w3lib.html import remove_tags, replace_tags

coloredlogs.install(level='DEBUG')

DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers': {
        'scrapy': {
            'level': 'DEBUG',
        },
    }
}

logging.config.dictConfig(DEFAULT_LOGGING)



# %%
class Spider(CrawlSpider):
    name = "computerra.tomsk.ru"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            

    custom_settings = {
        'LOGSTATS_INTERVAL': 15,
        'EXTENSIONS': {
            'scrapy.extensions.logstats.LogStats': 300
        }
    }
    
    start_urls = ['http://computerra.tomsk.ru/index.phtml?p=archive&a={}'.format(i) for i in range(1, 3000)]

    def parse_start_url(self, response):
        item = {}
        item['url'] = response.url

        item['title'] = response.css('font.atitle::text').extract_first()
        if item['title']: # there are empty pages
            date_tag = response.xpath('//*[@style="font-Size:12;color:#FFFFFF; font-family:Arial; font-weight:bold; line-height:150%; "]/text()').extract_first()  
            elems = response.css('font.content p').extract() 
            item['text'] = ' '.join((map(remove_tags, elems)))

            match = re.search('(\d+\.\d+\.\d+)\s*\[(.*)\]\s*(.*)', date_tag)
            if match:
                item['date'] = match.group(1)
                item['tag'] = match.group(2)
                item['rest'] = match.group(3) # magazine's number?

            yield item
