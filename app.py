# Get Order from BigCommerce
import requests

url = "https://api.bigcommerce.com/stores/b5ajmj9rbq/v2/orders/111"


header = {
    "X-Auth-Token":"redptv84kmlgfed97l7jroa0mdknfgc",
    "Content-Type":"application/json",
    "Accept": "application/json"
}

response = requests.request("GET",url,headers=header)
print(response.text)