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
    header = {
        "X-Auth-Token":"redptv84kmlgfed97l7jroa0mdknfgc",
        "Content-Type":"application/json",
        "Accept": "application/json"
        # STORE HASH : b5ajmj9rbq
    }
    order_data = ''
    if request.method =='POST':
        order_data = request.json
        order_id = order_data['data']['id']
        # print('ORDER DETAILS  :',request.json)  #Get all data 
        print("=================")
        print("ORDER ID : ",order_data['data']['id'])
        
        print("======= GET Full ORDER Details ==========")
        print(order_data)

    elif request.method =='GET':    
        print('New Request')
        newRequest = 'New REQUEST'
        return newRequest
        
    order_id = order_data['data']['id']
    store_hash = order_data['producer']

    print("****** Product ID IS  *********")
    print(order_id)
    
    print("****** STORE HAS IS  *********")
    print(store_hash)
    
    # url = f"https://api.bigcommerce.com/{store_hash}/v3/catalog/products/{product_id}"
    # url = f"https://api.bigcommerce.com/{store_hash}/v2/orders/{order_id}"
    url = f"https://api.bigcommerce.com/{store_hash}/v2/orders/{order_id}/products"
    
    response = requests.request("GET",url,headers=header).json()
    # print("***********  Product Name *********** ")
    print("**** FIND THE INDEX LENGTH *****")
    print("NUMBER OF LENGTH  :",  len(response))
    
    print("**** FIND THE PRODUCT *****")
    print(response[0])
    
    print("**** FIND THE PRODUCT *****")
    print("product_id  :  ",response[0]['product_id'])
    
    for i in response:
        print("****** ALL PRODUCTS ID ARE *******")
        print("product_id",i["product_id"])
    
    return render_template('/index.html', header=header, order_data=order_data, response=response)

if __name__ == ('__main__'):
    app.run(debug=True) 