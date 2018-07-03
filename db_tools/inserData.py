import sys
import os

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd + '../')
#在manage.py中
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "beenquickServer.settings")

import django
django.setup()

from db_tools.axf_json import JSONSTR
from products.models import Categorys

data = eval(JSONSTR)['data']
categories = data['categories']
products = data['products']

for category in categories:
    category_instance = Categorys()
    category_instance.name = category['name']
    category_instance.id = category['id']
    category_instance.icon = category['icon']
    category_instance.flag = category['flag']
    category_instance.is_open = category['is_open']
    category_instance.sort = category['sort']
    category_instance.visibility = category['visibility']
    category_instance.save()
    if category['cids']:
        for c in category['cids']:
            if c['id'] is '0':
                continue
            category_instance2 = Categorys()
            category_instance2.id = c['id']
            category_instance2.name = c['name']
            category_instance2.pcid = category_instance
            category_instance2.sort = c['sort']
            category_instance2.visibility = c.get('visibility','1')
            category_instance2.save()

