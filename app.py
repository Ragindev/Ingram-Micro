import http
import json
from math import prod
from pickle import GET
from flask import Flask, render_template,request
import requests
import time
import threading
import asyncio

app = Flask(__name__)


@app.route('/',methods=["GET", "POST"])
def listern():
    order_data = request.json
    backgroundThread = threading.Thread(target = processWebhookPayload, args = (order_data,))
    backgroundThread.start()
    return 'Yeah, I got it',200

def processWebhookPayload(order_data):
    header = {
        "X-Auth-Token":"redptv84kmlgfed97l7jroa0mdknfgc",
        "Content-Type":"application/json",
        "Accept": "application/json"
        # STORE HASH : b5ajmj9rbq
    }
    print("1. Funnction is working  \n ")
    
    # print(order_data)
########################################################
########################################################
    
    print("********** GET ORDER DATA FROM WEBHOOK *********** \n")
    store_hash = order_data['producer']
    scope = order_data['scope']
    store_id = order_data['store_id']
    order_id = order_data['data']['orderId']


    print("store_hash                   :",store_hash)
    print("scope                        :",scope)
    print("store_id                     :",store_id)
    print("order_id                     :",order_id )
    
    print('\n')
    print('\n')
    
########################################################
########################################################
    
    # Using List Order Products API find the products in the present order 
    url = f"https://api.bigcommerce.com/{store_hash}/v2/orders/{order_id}/products"
    response = requests.request("GET",url,headers=header).json()
    # print("9. Product DATA :", response)
    
    # collecting multipl product from the product API using for Loop
    for i in response:
        print("****** GET THE PRODUCTS DETAILS USING THE API  ******* \n")
        product_id = i["product_id"]
        
        # Getting Each product data using product API
        url = f"https://api.bigcommerce.com/{store_hash}/v3/catalog/products/{product_id}"
        product_data = requests.request("GET",url,headers=header).json()
        # print('12. Product data is   : ',product_data)
        
        id = int(product_data['data']['id'])
        name = product_data['data']['name']
        type = product_data['data']['type']
        sku = product_data['data']['sku']
        calculated_price = int(product_data['data']['calculated_price'])
        brand_id = int(product_data['data']['brand_id'])
        option_set_id = product_data['data']['option_set_id']
        option_set_display = product_data['data']['option_set_display']
        inventory_level = int(product_data['data']['inventory_level'])
        inventory_warning_level = int(product_data['data']['inventory_warning_level'])
        inventory_tracking = product_data['data']['inventory_tracking']
        reviews_rating_sum = int(product_data['data']['reviews_rating_sum'])
        reviews_count = int(product_data['data']['reviews_count'])
        total_sold = int(product_data['data']['total_sold'])
        fixed_cost_shipping_price = int(product_data['data']['fixed_cost_shipping_price'])
        is_free_shipping = product_data['data']['is_free_shipping']
        is_visible = product_data['data']['is_visible']
        is_featured = product_data['data']['is_featured']
        warranty = product_data['data']['warranty']
        bin_picking_number = product_data['data']['bin_picking_number']
        layout_file = product_data['data']['layout_file']
        upc = product_data['data']['upc']
        mpn = product_data['data']['mpn']
        gtin = product_data['data']['gtin']
        search_keywords = product_data['data']['search_keywords']
        availability = product_data['data']['availability']
        availability_description = product_data['data']['availability_description']
        gift_wrapping_options_type = product_data['data']['gift_wrapping_options_type']
        sort_order = int(product_data['data']['sort_order'])
        condition = product_data['data']['condition']
        is_condition_shown = product_data['data']['is_condition_shown']
        order_quantity_minimum = int(product_data['data']['order_quantity_minimum'])
        order_quantity_maximum = int(product_data['data']['order_quantity_maximum'])
        page_title = product_data['data']['page_title']
        meta_description = product_data['data']['meta_description']
        date_created = product_data['data']['date_created']
        date_modified = product_data['data']['date_modified']
        view_count = int(product_data['data']['view_count'])
        preorder_release_date = product_data['data']['preorder_release_date']
        preorder_message = product_data['data']['preorder_message']
        is_preorder_only = product_data['data']['is_preorder_only']
        is_price_hidden = product_data['data']['is_price_hidden']
        price_hidden_label = product_data['data']['price_hidden_label']
        base_variant_id = product_data['data']['base_variant_id']
        open_graph_type = product_data['data']['open_graph_type']
        open_graph_title = product_data['data']['open_graph_title']
        open_graph_description = product_data['data']['open_graph_description']
        open_graph_use_meta_description = product_data['data']['open_graph_use_meta_description']
        open_graph_use_product_name = product_data['data']['open_graph_use_product_name']
        open_graph_use_image = product_data['data']['open_graph_use_image']
        
        
        
        print("id                             :", id)
        print("name                           :", name)
        print("type                           :", type)
        print("sku                            :", sku)
        print("calculated_price               :", calculated_price)
        print("brand_id                       :", brand_id)
        print("option_set_id                  :", option_set_id)
        print("option_set_display             :", option_set_display)
        print("inventory_level                :", inventory_level)
        print("inventory_warning_level        :", inventory_warning_level)
        print("inventory_tracking             :", inventory_tracking)
        print("reviews_rating_sum             :", reviews_rating_sum)
        print("reviews_count                  :", reviews_count)
        print("total_sold                     :", total_sold)
        print("fixed_cost_shipping_price      :", fixed_cost_shipping_price)
        print("is_free_shipping               :", is_free_shipping)
        print("is_visible                     :", is_visible)
        print("is_featured                    :", is_featured)
        print("warranty                       :", warranty)
        print("bin_picking_number             :", bin_picking_number)
        print("layout_file                    :", layout_file)
        print("upc                            :", upc)
        print("mpn                            :", mpn)
        print("gtin                           :", gtin)
        print("search_keywords                :", search_keywords)
        print("availability                   :", availability)
        print("availability_description       :", availability_description)
        print("gift_wrapping_options_type     :", gift_wrapping_options_type)
        print("sort_order                     :", sort_order)
        print("condition                      :", condition)
        print("is_condition_shown             :", is_condition_shown)
        print("order_quantity_minimum         :", order_quantity_minimum)
        print("order_quantity_maximum         :", order_quantity_maximum)
        print("page_title                     :", page_title)
        print("meta_description               :", meta_description)
        print("date_created                   :", date_created)
        print("date_modified                  :", date_modified)
        print("view_count                     :", view_count)
        print("preorder_release_date          :", preorder_release_date)
        print("preorder_message               :", preorder_message)
        print("is_preorder_only               :", is_preorder_only)
        print("is_price_hidden                :", is_price_hidden)
        print("price_hidden_label             :", price_hidden_label)
        print("base_variant_id                :", base_variant_id)
        print("open_graph_type                :", open_graph_type)
        print("open_graph_title               :", open_graph_title)
        print("open_graph_description         :", open_graph_description)
        print("open_graph_use_meta_description:", open_graph_use_meta_description)
        print("open_graph_use_product_name    :", open_graph_use_product_name)
        print("open_graph_use_image           :", open_graph_use_image)
        
        print('\n')
        print('\n')
########################################################
########################################################
        
        
    #  Collecting shiping Address data from order shipping_address API  
    url = f"https://api.bigcommerce.com/{store_hash}/v2/orders/{order_id}/shipping_addresses"
    shipping_address = requests.request("GET",url,headers=header).json()
    print('\n', shipping_address, '\n')
    print("****** GET THE SHIPPING DETAILS USING THE API  ******* \n")
    address_id = int(shipping_address[0]['id'])
    order_id = int(shipping_address[0]['order_id'])
    first_name = shipping_address[0]['first_name']
    last_name = shipping_address[0]['last_name']
    company = shipping_address[0]['company']
    street_1 = shipping_address[0]['street_1']
    street_2 = shipping_address[0]['street_2']
    city = shipping_address[0]['city']
    zip = shipping_address[0]['zip']
    country = shipping_address[0]['country']
    country_iso2 = shipping_address[0]['country_iso2']
    state = shipping_address[0]['state']
    email = shipping_address[0]['email']
    phone = shipping_address[0]['phone']
    items_total = int(shipping_address[0]['items_total'])
    items_shipped = int(shipping_address[0]['items_shipped'])
    shipping_method = shipping_address[0]['shipping_method']
    base_cost = shipping_address[0]['base_cost']
    cost_ex_tax = shipping_address[0]['cost_ex_tax']
    cost_inc_tax = shipping_address[0]['cost_inc_tax']
    cost_tax = shipping_address[0]['cost_tax']
    cost_tax_class_id = int(shipping_address[0]['cost_tax_class_id'])
    base_handling_cost = shipping_address[0]['base_handling_cost']
    handling_cost_ex_tax = shipping_address[0]['handling_cost_ex_tax']
    handling_cost_inc_tax = shipping_address[0]['handling_cost_inc_tax']
    handling_cost_tax = shipping_address[0]['handling_cost_tax']
    handling_cost_tax_class_id = int(shipping_address[0]['handling_cost_tax_class_id'])
    shipping_zone_id = int(shipping_address[0]['shipping_zone_id'])
    shipping_zone_name = shipping_address[0]['shipping_zone_name']
    
    
    print("address_id                  : ",address_id)
    print("order_id                    : ",order_id)
    print("first_name                  : ",first_name)
    print("last_name                   : ",last_name)
    print("company                     : ",company)
    print("street_1                    : ",street_1)
    print("street_2                    : ",street_2)
    print("city                        : ",city)
    print("zip                         : ",zip)
    print("country                     : ",country)
    print("country_iso2                : ",country_iso2)
    print("state                       : ",state)
    print("email                       : ",email)
    print("phone                       : ",phone)
    print("items_total                 : ",items_total)
    print("items_shipped               : ",items_shipped)
    print("shipping_method             : ",shipping_method)
    print("base_cost                   : ",base_cost)
    print("cost_ex_tax                 : ",cost_ex_tax)
    print("cost_inc_tax                : ",cost_inc_tax)
    print("cost_tax                    : ",cost_tax)
    print("cost_tax_class_id           : ",cost_tax_class_id)
    print("base_handling_cost          : ",base_handling_cost)
    print("handling_cost_ex_tax        : ",handling_cost_ex_tax)
    print("handling_cost_inc_tax       : ",handling_cost_inc_tax)
    print("handling_cost_tax           : ",handling_cost_tax)
    print("handling_cost_tax_class_id  : ",handling_cost_tax_class_id)
    print("shipping_zone_id            : ",shipping_zone_id)
    print("shipping_zone_name          : ",shipping_zone_name)     
    
    print('\n')
    print('\n')
    return "got it" , 200
    
if __name__ == '__main__':
    app.run()










