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
    }
    productdata = ''
    if request.method =='POST':
        productdata = request.json
        productID = productdata['data']['id']
        print('Product Updated  :',request.json)  #Get all data 
        print ("=================")
        print ("Product DATA : ",productdata['data']['id'])
        print ("=================")
        print (productID)

    elif request.method =='GET':    
        print('New Request')
        # newRequest = 'New REQUEST'
        # return newRequest
    print("****** product data *********")
    print(productdata)
    print("****** product ID IS  *********")
    print(productdata['data']['id'])
    print("****** product ID IS  *********")
    product_id = productdata['data']['id']
    print("****** product ID new var is  *********")
    print (product_id)
    url = f"https://api.bigcommerce.com/stores/b5ajmj9rbq/v3/catalog/products/{product_id}"
    
    response = requests.request("GET",url,headers=header).json()
    # print("Customer ID is : ",response['customer_id'])
    print("RESPONSE is : ",response)
    return render_template('/index.html', header=header, response=response,productdata=productdata)

if __name__ == ('__main__'):
    app.run(debug=True)