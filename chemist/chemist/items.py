# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ChemistItem(scrapy.Item):

    name = scrapy.Field()

    price = scrapy.Field()

    image_url = scrapy.Field()

    shop_url = scrapy.Field()
