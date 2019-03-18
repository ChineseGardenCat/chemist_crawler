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
        new_product_ref = db.collection(u'products').document(item['name'])
        doc_ref = new_product_ref.collection(u'name').document(u'product_original_name')
        doc_ref.set({
            u'value': item['name'].strip()
        })
        doc_ref = new_product_ref.collection(u'name').document(u'chinese_interpretation')
        doc_ref.set({
            u'value': ''
        })
        doc_ref = new_product_ref.collection(u'name').document(u'key_searching_words')
        doc_ref.set({
            u'keywords_list': []
        })
        doc_ref = new_product_ref.collection(u'retailers').document(u'chemist_warehouse')
        doc_ref.set({
            u'price': item['price'].strip()
        })
        doc_ref = new_product_ref.collection(u'retailers').document(u'chemist_warehouse').collection(u'resources').document(u'urls')
        doc_ref.set({
            u'shop_url': item['shop_url'].strip(),
            u'image_url': item['image_url'].strip()
        })
        doc_ref = new_product_ref.collection(u'retailers').document(u'chemist_warehouse').collection(u'resources').document(u'description')
        doc_ref.set({
            u'value': ''
        })
        # doc_ref = db.collection(u'Products').document(u'ChemistWarehouse').collection(u'product_list').document(item['name'])
        # doc_ref.set({
        #     u'product_name': item['name'].strip(),
        #     u'product_image_url': item['image_url'].strip(),
        #     u'product_price': item['price'].strip(),
        #     u'product_shop_url': item['shop_url'].strip()
        # })

        return item
