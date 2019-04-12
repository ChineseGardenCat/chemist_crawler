import scrapy
from bs4 import BeautifulSoup
from ..items import ChemistItem
import re

class priceline_spider(scrapy.Spider):

    name = 'priceline_spider'

    start_urls = [
        'https://www.priceline.com.au/brand/'
    ]

    def parse(self, response):
