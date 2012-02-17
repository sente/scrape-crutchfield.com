import glob
import logging
import lxml
import lxml.html
import os
import pprint
import random
import requests
import sys
import urllib
import urlparse
import tablib
import get_fields


fields_string = """
type
category_ids
sku
name
image
small_image
thumbnail
_media_image
url_key
url_path
price
weight
status
visibility
tax_class_id
description
short_description
qty
product_name
"""
headers = fields_string.strip().split('\n')

ds = tablib.Dataset(headers=headers)

def add_record(url="http://www.crutchfield.com/p_113HR300/Kenwood-KTC-HR300.html?tp=993"):
    res = get_fields.test(url)
    fields = {}
    fields['type'] = 'simple'
    fields['status'] = 'Enabled'
    fields['visibility'] = 'Catalog, Search'
    fields['tax_class_id'] = 'None'
    fields['qty'] = 4
    fields['category_ids'] = '2,4'
    fields['sku'] = res['canonical']
    fields['name'] = res['productname']
    fields['image'] = res['list_images'][0]
    fields['small_image'] = res['list_images'][0]
    fields['thumbnail'] = res['list_images'][0]
    fields['_media_image'] = ', '.join(res['list_images'])
#    fields['url_key'] = res['url_key']
#    fields['url_path'] = res['url_path']
    fields['price'] = res['price']
    fields['weight'] = 2
    fields['description'] = res['overview_cleanest']
    fields['short_description'] = res['shortdescription']
    fields['product_name'] = res['productname']

    ds.append([fields[h] for h in headers])
    return fields




def load_from_file():
    items = [x.strip().split('\t') for x in open('categories.dat','r').read().strip().split('\n') if x.strip()]
    headers = ['category','sku','model','quantity','manufacturer','name','image_1','image_2','image_3','price','seo','tags','description']
    ds = tablib.Dataset(headers=headers)
    for count,tup in enumerate(items):

        cats,file = tup
        print count, cats, file

        res = get_fields.test(file)
        fields = {}

        fields['category'] = cats.replace(':',',')
        fields['sku'] = res['canonical'].replace('p_','')
        fields['model'] = fields['sku']
        fields['quantity'] = 10
        fields['manufacturer'] = res['productname'].split(' ')[0]
        fields['name'] = res['productname']
        imgs = [os.path.basename(x) for x in glob.glob(os.path.dirname(file) + '/*.jpeg')]
        imgs = imgs + ["","",""]
#        fields['imgs'] = ', '.join(imgs)
        fields['image_1'] = imgs[0]
        fields['image_2'] = imgs[1]
        fields['image_3'] = imgs[2]
        fields['price'] = res['price']
        fields['description'] = res['overview_cleanest']
        fields['seo'] = res['shortdescription']
        fields['tags'] = res['shortdescription']

        ds.append([fields[h] for h in headers])
    return ds
#        print fields



def save_ds(ds):
    open('ds.csv','w').write(ds.csv)
    open('ds.xls','w').write(ds.xls)
    open('ds.xlsx','w').write(ds.xlsx)
    open('ds.json','w').write(ds.json)


if __name__ == '__main__':
    ds = load_from_file()

#open('ds.csv','w').write(ds.csv)
#open('ds.xls','w').write(ds.xls)
#open('ds.xlsx','w').write(ds.xlsx)
#open('ds.json','w').write(ds.json)
#

