import sys
import os
import requests

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd + '../')
#在manage.py中
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "beenquickServer.settings")

import django
django.setup()

from db_tools.axf_json import JSONSTR
from products.models import Products

data = eval(JSONSTR)['data']
products = data['products']
for k,v in products.items():
    for product in v:
        p = Products()
        p.id = product['id']
        p.name = product['name']
        p.longname = product['long_name']
        p.store_nums = product['store_nums']
        p.specifics = product['specifics']
        p.attribute = product['attribute']
        p.sort = product['sort']
        p.brand_id = product['brand_id']
        p.brand_name = product['brand_name']
        p.hot_degree = product['hot_degree']
        p.safe_day = product['safe_day']
        p.safe_unit = product['safe_unit']
        p.market_price = product['market_price']
        p.partner_price = product['partner_price']
        p.pre_img = product['pre_img']
        p.pre_imgs = product['pre_imgs']
        p.keywords = product['keywords']
        url = product['img'].replace('\\', '')
        img = requests.get(url)
        p.img = img.content()
        p.pid = product['category_id']
        p.children_pid = product['child_cid']
        p.save()