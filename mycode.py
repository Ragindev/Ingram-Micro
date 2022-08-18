import http
import json
from math import prod
from pickle import GET
from urllib3 import request
from flask import Flask, render_template,request
import requests


app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def product():
    # set header for storing auth data
    header = {
        "X-Auth-Token":"redptv84kmlgfed97l7jroa0mdknfgc",
        "Content-Type":"application/json",
        "Accept": "application/json"
        # STORE HASH : b5ajmj9rbq
    }
    #create a global var for store order data
    order_data = ''
    # Collect the order data using POST Method
    if request.method =='POST':
        order_data = request.json
        order_id = order_data['data']['id']
        print('ORDER DETAILS  :',order_data, '\n')  #Get all data 
        # print("=================")
        # print(order_data)
        
        print("ORDER ID      : ",order_data['data']['id'])
        
        # print("======= GET Full ORDER Details ==========")
        # print(order_data)
        # print("order id :", order_id)
        return 'Yeah, I got it',200

    elif request.method =='GET':    
        # print('New Request')
        newRequest = 'New REQUEST'
        return newRequest
    
    # Collect order id and store hash from the order data 
    order_id = order_data['data']['id']
    store_hash = order_data['producer']

    print("****** order_id IS  ********* \n")
    print("order_id          :",order_id, '\n')
    
    print("****** STORE HASH IS  ********* \n")
    print("store_hash        :",store_hash,'\n')
    
    # Using List Order Products API find the products in the present order 
    url = f"https://api.bigcommerce.com/{store_hash}/v2/orders/{order_id}/products"
    # url = f"https://api.bigcommerce.com/stores/b5ajmj9rbq/v2/orders/249/products"
    # 
    response = requests.request("GET",url,headers=header).json()
    # print("***********  Product Name *********** ")
    print("Product DATA :", response)
    
    # collecting multipl product from the product API using for Loop
    for i in response:
        print("******  PRODUCTS IDs ARE *******")
        print(i)
        product_id = i["product_id"]
        # Getting Each product data using product API
        url = f"https://api. bigcommerce.com/{store_hash}/v3/catalog/products/{product_id}"
        prd_data = requests.request("GET",url,headers=header).json()
        print("********PRODUCT ID and DETAILS***********")
        print('product id    :',product_id)
        product_name = prd_data['data']['name']
        product_sku = prd_data['data']['sku']
        product_price = prd_data['data']['price']
        print("product_name  :",product_name)
        print("product_sku   :",product_sku)
        print("product_price :",product_price)
        
    #  Collecting shiping Address data from order shipping_address API  
    url = f"https://api.bigcommerce.com/{store_hash}/v2/orders/{order_id}/shipping_addresses"
    shipping_address = requests.request("GET",url,headers=header).json()
    # collecting each fields using for loop
    for x in shipping_address:
        first_name = x['first_name']
        street_1 = x['street_1']
        city = x['city']
        zip = x['zip']
        print("********* SHIPPING ADDRESS ********")
        print("First Name    : ",first_name)
        print("street_1      : ",street_1)
        print("city          : ",city)
        print("zip           : ",zip)
    return render_template('/index.html', header=header, order_data=order_data)

if __name__ == ('__main__'):
    app.run(debug=True) 