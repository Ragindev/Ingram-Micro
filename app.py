import http
import json
from pickle import GET
from urllib3 import request
from flask import Flask, render_template,request
import requests


app = Flask(__name__)

@app.route('/')
def index():
    url = "https://api.bigcommerce.com/stores/b5ajmj9rbq/v2/orders/111"
    header = {
        "X-Auth-Token":"redptv84kmlgfed97l7jroa0mdknfgc",
        "Content-Type":"application/json",
        "Accept": "application/json"
    }
    response = requests.request("GET",url,headers=header).json()
    # print(response)
    # print("Customer ID is : ",response['customer_id'])  24233840
    return render_template('/index.html',response=response)

@app.route('/product', methods=["GET", "POST"])
def product():
    if request.method =='POST':
        print('Product Updated',request.json)  #Get all data 
        return 'New Changes'

    elif request.method =='GET':    
        print('New Request')
        return 'New Request'
    return render_template('/product.html')
if __name__ == ('__main__'):
    app.run(debug=True)