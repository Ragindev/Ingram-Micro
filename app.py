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

# @app.route('/try-your-self',methods=["GET"])
# def tryYourSelf():
#     orderdata = {
#         'producer':'stores/b5ajmj9rbq',
#         'scope':'store/cart/converted',
#         'store_id':'1001802518',
#         'data':{
#             'orderId':'317'
#         }
#     }
#     processWebhookPayload(orderdata)
#     return 'Yeah, I got it'

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
    createOrder(shipping_address)
    print('\n')
    print('\n')
    return "got it" , 200


########################################################
########################################################

@app.route('/createOrder')
def createOrder(shipping_address):
    # create token
    url = "https://api.ingrammicro.com:443/oauth/oauth30/token"
    payload='grant_type=client_credentials&client_id=vxGA45MVwXFEWYvjzITSGTdGAgeygbct&client_secret=FyW7sATOWbGKFrOW'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    print("*********** token created **********")
    
    
    #Header Used to access ingrammicro
    headers = {
    'accept': 'application/json',
    'IM-CustomerNumber': '280695',
    'IM-CountryCode': 'AU',
    'IM-SenderID': 'IngramMicro',
    'IM-CorrelationID': '2022-07-29T05:31:04+0000',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer tRDEIaefR4BLsAGKbHqZJLxbAz71' 
    }
    #API to create a order in ingrammicro 
    url = "https://api.ingrammicro.com:443/sandbox/resellers/v6/orders"
    payload = json.dumps({
    "customerOrderNumber": shipping_address[0]['order_id'],
    "endCustomerOrderNumber": "ENDUSERPO1",
    "additionalAttributes": [
        {
        "attributeName": "allowPartialOrder",
        "attributeValue": "false"
        }
    ],
    "shipToInfo": {
        "contact": shipping_address[0]['first_name'],
        "companyName": shipping_address[0]['company'],
        "addressLine1": shipping_address[0]['street_1'],
        "addressLine2": shipping_address[0]['street_2'],
        "city":  shipping_address[0]['city'],   
        "state": "SA",  #Should be the state of AU
        "postalCode": "4209", #4 Digit Postal Code in AU   
        "countryCode": shipping_address[0]['country_iso2'],  
        "phoneNumber":  shipping_address[0]['phone'],
        "email":  shipping_address[0]['email']
    },
    "lines": [
        {
        "customerLineNumber": "001",
        "ingramPartNumber": "2985452",
        "quantity": 1,
        "unitPrice": 58.41
        },
        {
        "customerLineNumber": "002",
        "ingramPartNumber": "2985452",
        "vendorPartNumber": "",
        "quantity": 1,
        "unitPrice": 220.51
        }
    ]
    })
    response = requests.request("POST", url, headers=headers, data=payload)
    print("****** CREATE A ORDER USING THE ABOVE DATA  ******* \n")
    print(response.text)
    # return "Test Function "

if __name__ == '__main__':
    app.run()










