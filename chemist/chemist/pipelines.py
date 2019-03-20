# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
    'projectId': "chemist-helper",
})

db = firestore.client()

class ChemistPipeline(object):

    def process_item(self, item, spider):
        new_product_ref = db.collection(u'products').document(u'chemistwarehouse').collection(u'product_list').document(item['name'])
        new_product_ref.set({
            u'product_name': item['name'],
            u'product_price': item['price'],
            u'shop_url': item['shop_url'].strip(),
            u'image_url': item['image_url'].strip(),
            u'categories': item['product_category'],
            u'key_words': item['key_words']

        })

        return item
