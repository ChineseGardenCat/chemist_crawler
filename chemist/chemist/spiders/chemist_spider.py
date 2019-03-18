import scrapy
from bs4 import BeautifulSoup
from ..items import ChemistItem
import re

class ChemistSpider(scrapy.Spider):
    name = 'chemist_spider'

    start_urls = [
        'https://www.chemistwarehouse.com.au/'
    ]

    chemist_prefix = 'https://www.chemistwarehouse.com.au/'

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        # new_item = ChemistItem()

        # TODO: Find all category tages in the home page
        tags = soup.find_all('a', href=re.compile(r"^/shop-online/*"))
        temp = []
        for tag in tags:
            temp.append(tag.get('href'))
        temp = list(set(temp))
        for suffix in temp:
            url = self.chemist_prefix + suffix
            yield scrapy.Request(url, callback=self.parse_product)
        banner = soup.find_all('a', href=re.compile(r"^https://www.chemistwarehouse.com.au/shop-online/*"))
        for category in banner:
            url = category.get('href')
            yield scrapy.Request(url, callback=self.parse_product)

    def parse_product(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        products = soup.find_all('a', class_="product-container")
        new_item = ChemistItem()
        for product in products:
            shop_url = self.chemist_prefix + product.get('href')
            new_item['shop_url'] = shop_url
            new_item['name'] = product.get('title')
            new_item['price'] = product.find('span', class_='Price').text
            new_item['image_url'] = product.find('img').get('src')
            yield new_item
        next_tags = set(soup.find_all('a', string='Next'))
        next_arr = []
        for ele in next_tags:
            next_arr.append(ele.get('href'))
        if next_arr:
            for suffix in next_arr:
                url = self.chemist_prefix + suffix
                yield scrapy.Request(url, callback=self.parse_product)

