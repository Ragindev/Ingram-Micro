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
        'producer':'stores/o257sk57z9',
        'scope':'store/cart/converted',
        'store_id':'1002102576', #store id NB
        # 'store_id':'1001802518', #Store ID Camera Stuff
        'data':{
            'orderId':'683'
        }
    }
    processWebhookPayload(orderdata)
    return 'Yeah, I got it'

def processWebhookPayload(order_data):
    header = {
        "X-Auth-Token":"r4vkpwhvq8h595ak1m9vtg4l6pee9dy",
        "Content-Type":"application/json",
        "Accept": "application/json"
        # STORE HASH : b5ajmj9rbq
        # STORE HASH : o257sk57z9
    }
    
    print(order_data)
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
    
    products_In_Order = [] #Create an empty array to store the values from the below loop
    # Using List Order Products API find the products in the present order 
    linesOut = []
    customerLineNumber = 0
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
        products_In_Order.append(product_data)
        print(product_data)
        lines_data = {
            "customerLineNumber":customerLineNumber+1,
            "vendorPartNumber" : product_data["data"]["sku"],
            "quantity": 1,
            "unitPrice": product_data["data"]["price"],
        }
        print("Lines Data in loop : ",lines_data)
        linesOut.append(lines_data)
        
        
        print('\n')
        print('\n')
        customerLineNumber = customerLineNumber + 1
        
    # linesOut = [lines_data]
    print(linesOut)
    
    print('\n')
    print('\n')
########################################################
########################################################
        
    #  Collecting shiping Address data from order shipping_address API  
    url = f"https://api.bigcommerce.com/{store_hash}/v2/orders/{order_id}/shipping_addresses"
    shipping_address = requests.request("GET",url,headers=header).json()
    
    print("****** GET THE SHIPPING DETAILS USING THE API  ******* \n")
    
    pp.pprint(shipping_address)
    createOrder(shipping_address, products_In_Order , linesOut) # Calling the Create Order Function 
    print('\n')
    print('\n')
    return "got it" , 200


########################################################
########################################################

@app.route('/createOrder')
def createOrder(shipping_address, products_In_Order, linesOut):
    # Create token for every new order 
    client_id = 'vxGA45MVwXFEWYvjzITSGTdGAgeygbct'
    client_secret = 'FyW7sATOWbGKFrOW'
    url = "https://api.ingrammicro.com:443/oauth/oauth30/token"
    payload=f'grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    tokenResponse = requests.request("POST", url, headers=headers, data=payload)
    # print(json.loads(tokenResponse.text))
    # convert the tokenResponse from string to Dictionary using (json.loads)
    accessToken =json.loads(tokenResponse.text)
    
    print("*********** token created **********")
    headers = {
    'accept': 'application/json',
    'IM-CustomerNumber': '280695',
    'IM-CountryCode': 'AU',
    'IM-SenderID': 'IngramMicro',
    'IM-CorrelationID': '2022-07-29T05:31:04+0000',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer '+ accessToken['access_token']  # Passing token to the header 
    }
    
    # print("PRODUCT 1  :",products_In_Order[0]['data']['sku'])
    # print("PRODUCT 2  :",products_In_Order[1]['data']['sku'])
    
    # API to create a order in ingrammicro 
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
        "postalCode": "4209", #4 Digit Postal Code available in AU   
        "countryCode": shipping_address[0]['country_iso2'], #must be AU  
        "phoneNumber":  shipping_address[0]['phone'], 
        "email":  shipping_address[0]['email']
    },
    #each lines contain a single product 
    #get the product sku from the bigcommerce order and crate lines based on the number of product 
    "lines": linesOut
    })  
    print("Payload Is : ",payload)
    response = requests.request("POST", url, headers=headers, data=payload)
    print("****** CREATE A ORDER USING THE ABOVE DATA  ******* \n")
    print(response.text)
    # print("Product in order is **********: ",products_In_Order)
    return "Order Created"

if __name__ == '__main__':
    app.run()










