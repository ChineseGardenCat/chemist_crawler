import scrapy
from bs4 import BeautifulSoup
from ..items import ChemistItem
import re

class ChemistSpider(scrapy.Spider):
    name = 'chemist_spider'

    start_urls = [
        'https://www.chemistwarehouse.com.au/categories'
    ]

    chemist_prefix = 'https://www.chemistwarehouse.com.au/'

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        # TODO: Find all category tages in the home page
        tags = soup.find_all('a', href=re.compile(r"^/shop-online/*"))
        temp = []
        for tag in tags:
            temp.append(tag.get('href'))
        temp = list(set(temp))
        if len(temp) != 0:
            for suffix in temp:
                url = self.chemist_prefix + suffix
                yield scrapy.Request(url, callback=self.parse_product)
        # banner = soup.find_all('a', href=re.compile(r"^https://www.chemistwarehouse.com.au/shop-online/*"))
        # for category in banner:
        #     url = category.get('href')
        #     yield scrapy.Request(url, callback=self.parse_product)

    def parse_product(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        products = soup.find_all('a', class_="product-container")
        for product in products:
            shop_url = self.chemist_prefix + product.get('href')
            yield scrapy.Request(shop_url, callback=self.parse_product_page)
        next_tags = set(soup.find_all('a', string='Next'))
        next_arr = []
        for ele in next_tags:
            next_arr.append(ele.get('href'))
        if next_arr:
            for suffix in next_arr:
                url = self.chemist_prefix + suffix
                yield scrapy.Request(url, callback=self.parse_product)

    def parse_product_page(self, response):
        new_item = ChemistItem()
        soup = BeautifulSoup(response.body, 'html.parser')
        product_categories = soup.find('div', class_="breadcrumbs").find_all('a')
        product_categories_list = []
        for category in product_categories:
            url = category.get('href')
            spliter = re.compile(r'/')
            splited_list = spliter.split(url)
            if len(splited_list) > 2:
                product_categories_list.append(splited_list[3])
        product_details = soup.find('div', class_="productDetail")
        new_item['shop_url'] = response.request.url
        new_item['name'] = product_details.find('div', class_="product-name").find('h1').text.strip()
        new_item['price'] = product_details.find('div', class_="Price").find('span').text.strip()
        new_item['image_url'] = product_details.find('div', class_="pi_slide").find('a').get('href')
        new_item['product_category'] = product_categories_list
        new_item['key_words'] = product_details.find('div', class_="product-name").find('h1').text.strip().split()
        yield new_item
