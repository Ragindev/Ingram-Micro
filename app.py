import http
import json
from math import prod
from pickle import GET
from flask import Flask, render_template,request
import requests
import time
import threading
import asyncio
import pprint

pp = pprint.PrettyPrinter(indent=4)

app = Flask(__name__)


@app.route('/',methods=["GET", "POST"])
def listern():
    order_data = request.json
    backgroundThread = threading.Thread(target = processWebhookPayload, args = (order_data,))
    backgroundThread.start()
    return 'Yeah, I got it',200

@app.route('/try-your-self',methods=["GET"])
def tryYourSelf():
    orderdata = {
        'producer':'stores/b5ajmj9rbq',
        'scope':'store/cart/converted',
        'store_id':'1001802518',
        'data':{
            'orderId':'288'
        }
    }
    processWebhookPayload(orderdata)
    return 'Yeah, I got it'

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
        
        pp.pprint(product_data)
        
        
        print('\n')
        print('\n')
########################################################
########################################################
        
        
    #  Collecting shiping Address data from order shipping_address API  
    url = f"https://api.bigcommerce.com/{store_hash}/v2/orders/{order_id}/shipping_addresses"
    shipping_address = requests.request("GET",url,headers=header).json()
    # print('\n', shipping_address, '\n')
    print("****** GET THE SHIPPING DETAILS USING THE API  ******* \n")
    pp.pprint(shipping_address)
    
    print('\n')
    print('\n')
    return "got it" , 200
    
if __name__ == '__main__':
    app.run()










