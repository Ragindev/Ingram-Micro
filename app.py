import json
from urllib import response
from flask import Flask, render_template 
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
    url = "https://api.bigcommerce.com/stores/b5ajmj9rbq/v3/hooks"

    headers = {
        "Content-Type": "",
        "Accept": "",
        "X-Auth-Token": "redptv84kmlgfed97l7jroa0mdknfgc"
    }

    response = requests.request("GET", url, headers=headers)
    print(response.text)
    return render_template('/index.html', response=response)

if __name__ == ('__main__'):
    app.run(debug=True)