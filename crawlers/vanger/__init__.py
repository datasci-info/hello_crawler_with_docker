import requests
from pyquery import PyQuery
import pandas as pd
from datetime import datetime
import time


def get_product_data(product_url):
    res = requests.get(product_url)
    S = PyQuery(res.text)
    
    product_sku = res.text.split('''console.log("cloudmaker_stock(''')[-1].split(")")[0]
    product_id = S("*[type='hidden']#product_id").attr("value")
    description = "\n".join([PyQuery(p).text() for p in S('*[itemprop="offers"] *[itemprop="description"] p') if len(PyQuery(p)("a")) == 0])
    
    colors = [PyQuery(p)("a") for p in S('*[itemprop="offers"] *[itemprop="description"] p') if len(PyQuery(p)("a")) > 0][0]
    
    wh_url = "https://shop.vanger.com.tw/index.php"
    wh_res = requests.get(wh_url,params={"route":"cloudmaker/order/wareHouseOrdernew",
                                      "product_sku":product_sku})
    
    df = pd.DataFrame(wh_res.json())
    def exp_df(row):
        stores = row["cred_response"]["stock"][0]
        return [{"store":s,"qty":stores[s],"size":row["cred_response"]["size"]} for s in stores]

    if df.shape[0] > 0:
        store_inventory_df = pd.concat(list(map(pd.DataFrame,df.apply(exp_df,axis=1).tolist())))
        store_inventory_df["product_sku"] = product_sku
        store_inventory_df["product_id"] = product_id
        store_inventory_df["surveyAt"] = datetime.utcnow()
    else:
        store_inventory_df = df
    
    size_url = "https://shop.vanger.com.tw/index.php?route=product/product_options&key={prod_id}&type=prod".format(prod_id = product_id)
    size_res = requests.get(size_url)
    
    SS = PyQuery(size_res.text)
    
    colors = colors.filter(lambda i,e: len(PyQuery(e)("img")) > 0)
    
    data = {
        "product_url": product_url,
        "product_id": product_id,
        "product_sku": product_sku,
        "price": S('*[itemprop="price"]').attr("content"),
        "discount_rule":S(".discount").map(lambda i,e:PyQuery(e).outer_html()),
        "tags": S(".tags a").map(lambda i,e:{
            "tag_name": PyQuery(e).text(),
            "tag_url": PyQuery(e).attr("href"),
        }),
        "sizes": SS("option").map(lambda i,e:{
            "maybe_size_id": PyQuery(e).attr("value"),
            "size": PyQuery(e).text().replace("\xa0(暫無現貨)",""),
            "disable": PyQuery(e).text().endswith("\xa0(暫無現貨)"),
        }),
        "image_wrap": S(".img-wrap").outer_html(),
        "sizing_info": S(".product-table.europ-size").outer_html(),
        "colors": colors.map(lambda i,e:{
            "product_url":"https:" + PyQuery(e).attr("href"),
            "color": PyQuery(e)("img").attr("title"),
            "color_img_url": "https:" + PyQuery(e)("img").attr("src"),
        }),
        "store_inventory": store_inventory_df.to_dict("records"),
        "spec_no":S(".description").text().replace("規格型號 ",""),
        "description": description,
        "images":S("#image-additional li > a").map(lambda i,e: {
            "image_url":"https:" + PyQuery(e).attr("href"),
            "thumbnail_image_url":"https:" + PyQuery(e)("img").attr("src"),
        })
    }
    
    return data
    


def get_all_category_urls():
    url = "https://shop.vanger.com.tw/"
    res = requests.get(url)
    
    S = PyQuery(res.text)

    category_urls = S('li[href="https://shop.vanger.com.tw/men"] a').map(lambda i,e:{
        "url": PyQuery(e).attr("href"),
        "title": PyQuery(e).text(),
    }) + S('li[href="https://shop.vanger.com.tw/woman"] a').map(lambda i,e:{
        "url": PyQuery(e).attr("href"),
        "title": PyQuery(e).text(),
    }) + S('li[href="https://shop.vanger.com.tw/recommend"] a').map(lambda i,e:{
        "url": PyQuery(e).attr("href"),
        "title": PyQuery(e).text(),
    })

    category_urls_df = pd.DataFrame(category_urls)

    urls = category_urls_df.url.tolist()
    return urls 

def get_all_product_urls_in_category(category_page_url, sleep_time=10.):
    category_page_res = requests.get(category_page_url)
    S = PyQuery(category_page_res.text)

    try:
        max_page = max(S(".pagination a").map(lambda i,e: int(PyQuery(e).attr("href").replace(category_page_url+"?page=",""))))
    except:
        max_page = 1

    category_page_urls = [
        category_page_url + "?page={n}" .format(n=m) for m in range(1,max_page+1)
    ]
    
    category_page_reses = []
    
    def get_product_page_urls(category_page_res):
        S = PyQuery(category_page_res.text)
        proudct_urls = S(".product-listing .image > a").map(lambda i,e: PyQuery(e).attr("href"))
        return proudct_urls
    
    
    for category_page_url in category_page_urls:
        category_page_reses.append(get_product_page_urls(requests.get(category_page_url)))
        
        time.sleep(sleep_time)
        print("category_page_url = ",category_page_url)
        

    
    all_product_page_urls = []
    
    for urls in category_page_reses:
        all_product_page_urls.extend(urls)
        
    return all_product_page_urls