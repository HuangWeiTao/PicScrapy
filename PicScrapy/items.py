# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class TopicItem(scrapy.Item):
    name = scrapy.Field()
    start_url = scrapy.Field()
    name = scrapy.Field()

class PostItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    topic_id = scrapy.Field()