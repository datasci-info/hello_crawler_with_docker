import os
import time
# Variables about mongodb
MONGODB_HOST = os.environ.get("MONGODB_HOST", "localhost")
MONGODB_PORT = int(os.environ.get("MONGODB_PORT", 27017))
MONGODB_USER = os.environ.get("MONGODB_USER", "")
MONGODB_PWD = os.environ.get("MONGODB_PWD", "")
DB = os.environ.get("DB", "crawler")
SLEEP_TIME = float(os.environ.get("SLEEP_TIME", 2.))

try:
    from local_settings import *
except:
    pass

from pymongo import MongoClient

mcli = MongoClient(host=MONGODB_HOST, port=MONGODB_PORT)
db = mcli[DB]

if MONGODB_USER!="":
    db.authenticate(MONGODB_USER,MONGODB_PWD)


from crawlers.vanger import get_all_category_urls, get_all_product_urls_in_category, get_product_data

all_category_urls = get_all_category_urls()

for category_url in all_category_urls:
    p_urls = get_all_product_urls_in_category(category_url,2)

    for p_url in p_urls:
        print("p_url = ",p_url)
        if db.vanger.find({"product_url":p_url}).count() == 0:
            time.sleep(SLEEP_TIME)
            try:
                db.vanger.insert(get_product_data(p_url))
            except Exception as e:
                print("error = ",e)
