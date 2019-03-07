# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from firebase import firebase
import json
import requests

firebase = firebase.FirebaseApplication('https://chemist-helper.firebaseio.com')

class ChemistPipeline(object):


    def process_item(self, item, spider):

        data = {'image': item['image_url'], 'product_name': item['name'], 'product_price': item['price'].strip(),
                'shop_url': item['shop_url']}
        sent = json.dumps(data)
        print(sent)
        result = requests.put("https://chemist-helper.firebaseio.com/products/" + item['name']+".json", data = sent)
        print(result)
        return item
