import scrapy
from bs4 import BeautifulSoup
from ..items import ChemistItem
import re
import csv


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

    def parse_product(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        next_tags = set(soup.find_all('a', string='Next'))
        next_arr = []
        for ele in next_tags:
            next_arr.append(ele.get('href'))
        if next_arr:
            for suffix in next_arr:
                url = self.chemist_prefix + suffix
                yield scrapy.Request(url, callback=self.parse_product)
        products = soup.find_all('a', class_="product-container")
        new_item = ChemistItem()
        for product in products:
            shop_url = self.chemist_prefix + product.get('href')
            yield scrapy.Request(shop_url, callback=self.parse_product_detail)


    def parse_product_detail(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')


    #
    # def parse_details(self, response):
    #     chemist_prefix = 'https://www.chemistwarehouse.com.au/'
    #     soup = BeautifulSoup(response.body, 'html.parser')
    #     next = set(soup.find_all('a', string='Next'))
    #     next_arr = []
    #     for ele in next:
    #         next_arr.append(ele.get('href'))
    #     if next_arr:
    #         for suffix in next_arr:
    #             url = chemist_prefix + suffix
    #             yield scrapy.Request(url, callback=self.parse_details)
    #     products = soup.find_all("div", class_="Product")
    #     with open("output.csv", 'a') as resultFile:
    #         for product in products:
    #             result = []
    #             name = product.find('div', class_="product-name").text
    #             price = product.find('span', class_='Price').text
    #             image = product.find('img').get('src')
    #             result.append(name)
    #             result.append(price)
    #             result.append(image)
    #             print(result)
    #             wr = csv.writer(resultFile, dialect='excel')
    #             wr.writerow(result)
