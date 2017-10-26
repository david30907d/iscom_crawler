# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TripadvisorItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    detail = scrapy.Field()
    location = scrapy.Field()
    description = scrapy.Field()
    image = scrapy.Field()
    link = scrapy.Field()