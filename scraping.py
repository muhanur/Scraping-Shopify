import requests
import pandas as pd
from time import sleep

pages = 2
limit = 12

df = pd.DataFrame(columns=['Product name','SKU','Size','Price','Price Disc'])

for page in range(1, pages):
    url = "https://filter-v1.globo.io/filter?filter_id=32958&shop=shermaine-washington.myshopify.com&collection=279791140962&sort_by=price-descending&country=CA&filter%5B329327%5D%5B%5D=Adidas&filter%5B329327%5D%5B%5D=Nike&filter%5B329327%5D%5B%5D=Jordan&filter%5B329327%5D%5B%5D=New%20Balance&filter%5B329328%5D%5B%5D=Footwear&event=products&limit={}&page={}&page_type=collection".format(limit, page)

    headers = {'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'}
    response = requests.get(url, headers=headers).json()

    products = response['products']
    for product in products:
        PT = product['title']
        PI = product['id']
        variants = product['variants']
        bot = 1
        for variant in variants:
            if variant['available'] == True:
                VI = variant['id']
                
                bot =+ bot
                headers_bot = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Cafari/537.36'}
                add_url = 'https://www.theclosetinc.com/cart/add.js'
                add_param = {
                    'form_type': 'product',
                    'utf8': '%E2%9C%93',
                    'id': VI,
                    'quantity': 1,
                    'product-id': PI,
                    'section-id': 'template--15213973274722__main',
                    'sections': 'cart-drawer'
                }

                session = requests.Session()
                disc_response = session.post(add_url, headers=headers_bot, data=add_param)

                if disc_response.status_code == 200:
                    disc_price = disc_response.json()['discounted_price'] / 100
                else:
                    print("Too many requests")
                    disc_price = None

                new_row = {"Product name": PT, "SKU": variant['sku'], "Size": variant['title'], "Price": variant['price'], "Price Disc": disc_price}
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

                session.cookies.clear()
                sleep(5)

df.to_excel('Shoes.xlsx')
df
