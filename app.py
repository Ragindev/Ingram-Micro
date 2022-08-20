from email import header
import http
import json
from math import prod
from pickle import GET
from wsgiref import headers
from flask import Flask, render_template,request
import requests
import time
import threading
import asyncio
import pprint
import http.client

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
            'orderId':'697'
            # 'orderId':'500'
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
########################################################################################

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
########################################################################################
# Chanaging the order status to Awaiting Shipment in Bigcommerce 
    url = f"https://api.bigcommerce.com/{store_hash}/v2/orders/{order_id}"
    payload = {
        "status_id": 9, #Status id : 9 is Awaiting Shipment
    }
    update_order_status = requests.request("PUT", url, json=payload, headers=header).json()
    print('\n')
    print("Order Status Changed to  : ", update_order_status['status'])
    
########################################################################################
    
    products_In_Order = [] #Create an empty array to store the values from the below loop
    # Using List Order Products API find the products in the present order 
    linesOut = []
    customerLineNumber = 0
    url = f"https://api.bigcommerce.com/{store_hash}/v2/orders/{order_id}/products"
    response = requests.request("GET",url,headers=header).json()
    print("Product DATA :", response)
    # collecting multipl product from the product API using for Loop
    for i in response:
        print("****** GET THE PRODUCTS DETAILS USING THE API  ******* \n")
        product_id = i["product_id"]
        
        # Getting Each product data using product API
        url = f"https://api.bigcommerce.com/{store_hash}/v3/catalog/products/{product_id}"
        product_data = requests.request("GET",url,headers=header).json()
        
        # Asign the SKU to the bcSKU Variable     
        bcSKU= product_data["data"]["sku"]
        print("The Selected product BC SKU Is : ",bcSKU)
        # Assign the selected BigCommerce SKUs to a variable 
        BC_prd = {"NBDVR622GW":"camera",
                  "NBDVR522GW":"camera",
                  "NBDVR422GW":"camera",
                  "NBDVR322GW":"camera",
                  "NBDVR122":"camera",
                  "NBDVR222":"camera",
                  "NBDVR622GW-1-1":"camera",
                  "NBDVRS2RFCZ":"accessories",
                  "NBDVRS2RFCW":"accessories",
                  "NBDVRS2RWC":"accessories",
                  "NBDVRS2HK": "accessories",
                  "NBDVRS2PM":"accessories",
                  "NBDVRS2GP32U3":"accessories",
                  "NBDVRS2SD64GBU3":"accessories",
                  "NBDVRS2PMGPS":"accessories",
                  "NBDVRS2PF":"accessories",
                  "NBDVRS2SD32GBU3":"accessories",
                  "NBDVRS2SD128GBU3":"accessories",
                  "NBDVRS2CLC":"accessories",
                  "NBDVRS2CC":"accessories",
                  "NBDVR380BAT":"accessories",
                  "NBDVRS2SD256GBU3":"accessories",
                  "NBSFITFRONTREARG":"accessories",
                  "NBDVR380GWXRCB":"accessories",
                  }

        IM_SKU =""  # Create an empty variable to store the IM SKU
        # Checking each SKUs available in the BC 
        for SKU_key in BC_prd: 
            if bcSKU == SKU_key:
                # Check the SKU values camera or Accessories
                # if the product is a camera then it will assign a new sku values matching in IM
                # else Assign the product to the second IM Sku
                if BC_prd[SKU_key] == 'camera':
                    print("The selected product is ::: CAMERA ")
                    IM_SKU = 2985452
                else:
                    print("The selected product is ::: CAMERA ACCESSORIES ")
                    IM_SKU = 3278984
                    
        products_In_Order.append(product_data)
        # print(product_data)
        lines_data = {
            "customerLineNumber":customerLineNumber+1,
            "ingramPartNumber" : IM_SKU, #collecting the sku from the top
            "quantity": response[0]['quantity'],
            "unitPrice": product_data["data"]["price"], 
        }
        print("Lines Data in loop : ",lines_data)
        linesOut.append(lines_data)
        print('\n')
        print('\n')
        customerLineNumber = customerLineNumber + 1 
    print(linesOut)
    print('\n')
    print('\n')
########################################################################################
        
    #  Collecting shiping Address data from order shipping_address API  
    url = f"https://api.bigcommerce.com/{store_hash}/v2/orders/{order_id}/shipping_addresses"
    shipping_address = requests.request("GET",url,headers=header).json()
    
    print("****** GET THE SHIPPING DETAILS USING THE API  ******* \n")
    
    print(shipping_address)
    
########################################################################################
    # Check the Country || if the selected country is Austalia then do the next step 
    # else simply print  Selected Country is not Australia
    selected_country = shipping_address[0]['country']
    if selected_country != 'Australia':
        print("Selected Country is not Australia")
    else:
        print("The Selected Country is : ",selected_country)
        createOrder(shipping_address, products_In_Order, linesOut) # Calling the Create Order Function 
        print('\n')
        print('\n')
        return "got it" , 200


########################################################################################

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
    
    # API to create a order in ingrammicro 
    url = "https://api.ingrammicro.com:443/sandbox/resellers/v6/orders"
    payload = json.dumps({
    "customerOrderNumber": shipping_address[0]['order_id'],
    "endCustomerOrderNumber": shipping_address[0]['order_id'],
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
        # "state": "SA",  #Should be the state of AU
        # "postalCode": "4209", #4 Digit Postal Code available in AU  
        "countryCode": shipping_address[0]['country_iso2'], #must be AU  
        "phoneNumber":  shipping_address[0]['phone'], 
        "email":  shipping_address[0]['email']
    },
    #each lines contain a single product 
    #get the product sku from the bigcommerce order and crate lines based on the number of product 
    "lines": linesOut
    })  
    # print("Payload Is : ",payload)
    response = requests.request("POST", url, headers=headers, data=payload)
    print("****** CREATE A ORDER USING THE ABOVE DATA  ******* \n")
    print(response.text)
    return "Order Created "


# get order status from ingrammicro
@app.route('/bcStatus',methods=["GET","POST"])
def getOrderStatus():
    print("Get Order Status")
    # Create token for every new order 
    client_id = 'vxGA45MVwXFEWYvjzITSGTdGAgeygbct'
    client_secret = 'FyW7sATOWbGKFrOW'
    store_hash="b5ajmj9rbq"
    # STORE HASH : b5ajmj9rbq
    # STORE HASH : o257sk57z9
    bc_header = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            # 'X-Auth-Token': 'r4vkpwhvq8h595ak1m9vtg4l6pee9dy'
            'X-Auth-Token': 'redptv84kmlgfed97l7jroa0mdknfgc'
            }
    url = "https://api.ingrammicro.com:443/oauth/oauth30/token"
    payload=f'grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    tokenResponse = requests.request("POST", url, headers=headers, data=payload)
    # print(json.loads(tokenResponse.text))
    # convert the tokenResponse from string to Dictionary using (json.loads)
    accessToken =json.loads(tokenResponse.text)
    print(accessToken['access_token'])

    url = "https://api.ingrammicro.com/sandbox/resellers/v6/orders/search?pageNumber=1&pageSize=100"

    payload={}
    headers = {
    'Accept': 'application/json',
    'IM-CorrelationID': '2022-07-20',
    'IM-CountryCode': 'AU',
    'IM-CustomerNumber': '280695',
    'IM-SenderID': 'GHDGH',
    'Authorization': 'Bearer '+accessToken['access_token']
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    pd_details=json.loads(response.text)

    for cs in pd_details['orders']:
        print("customer num",cs['customerOrderNumber'],"status",cs['orderStatus'])
        if cs['orderStatus'] == "CANCELED":
           
            url = f"https://api.bigcommerce.com/stores/{store_hash}/v2/orders/{cs['customerOrderNumber']}"

            payload = json.dumps({
            "status_id": 5
            })
            headers = bc_header

            response = requests.request("PUT", url, headers=headers, data=payload)

            # print(response.text)

        elif cs['orderStatus'] == "PROCESSING":
            url = f"https://api.bigcommerce.com/stores/{store_hash}/v2/orders/{cs['customerOrderNumber']}"

            payload = json.dumps({
            "status_id": 9
            })
            headers = bc_header

            response = requests.request("PUT", url, headers=headers, data=payload)

            # print(response.text)
        
        elif cs['orderStatus'] == "SHIPPED":
            url = f"https://api.bigcommerce.com/stores/{store_hash}/v2/orders/{cs['customerOrderNumber']}"

            payload = json.dumps({
            "status_id": 2
            })
            headers = bc_header
            response = requests.request("PUT", url, headers=headers, data=payload)

            # print(response.text)

        elif cs['orderStatus'] == "CLOSED":
            url = f"https://api.bigcommerce.com/stores/{store_hash}/v2/orders/{cs['customerOrderNumber']}"

            payload = json.dumps({
            "status_id": 10
            })
            headers =bc_header

            response = requests.request("PUT", url, headers=headers, data=payload)

            # print(response.text)
        
        elif cs['orderStatus'] == "OPEN":
            url = f"https://api.bigcommerce.com/stores/{store_hash}/v2/orders/{cs['customerOrderNumber']}"

            payload = json.dumps({
            "status_id": 8
            })
            headers =bc_header

            response = requests.request("PUT", url, headers=headers, data=payload)

            print(response.text)
        
        else:
            print("UNKONOW STATUS",cs['orderStatus'])

    return "pd_details['orders']"
    
# get order status from ingrammicro
@app.route('/productUpdation',methods=["GET","POST","PUT"])
def bcProductUpdate():
    print("Get Order Status")
    # Create token for every new order 
    client_id = 'vxGA45MVwXFEWYvjzITSGTdGAgeygbct'
    client_secret = 'FyW7sATOWbGKFrOW'
    store_hash="b5ajmj9rbq"
    # STORE HASH : b5ajmj9rbq
    # STORE HASH : o257sk57z9
    bc_header = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            # 'X-Auth-Token': 'r4vkpwhvq8h595ak1m9vtg4l6pee9dy'
            'X-Auth-Token': 'redptv84kmlgfed97l7jroa0mdknfgc'
            }
    url = "https://api.ingrammicro.com:443/oauth/oauth30/token"
    payload=f'grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    tokenResponse = requests.request("POST", url, headers=headers, data=payload)
    # print(json.loads(tokenResponse.text))
    # convert the tokenResponse from string to Dictionary using (json.loads)
    accessToken =json.loads(tokenResponse.text)
    print(accessToken['access_token'])

    url = "https://api.ingrammicro.com:443/sandbox/resellers/v6/catalog/priceandavailability?includeAvailability=true&includePricing=true"
    payload = json.dumps({
    "products": [
        {
        "ingramPartNumber": "3278984"
        },
        {
        "ingramPartNumber": "2985452"
        }
    ]
    })
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': 'Bearer '+accessToken['access_token'],
    'IM-CustomerNumber': '280695',
    'IM-CorrelationID': '2022-07-29T05:31:04+0000',
    'IM-SenderID': 'SampleUser-Best-Buys',
    'IM-CountryCode': 'AU'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return response.text



if __name__ == '__main__':
    app.run()

