import http.client

conn = http.client.HTTPSConnection("api.bigcommerce.com")

headers = {
    'Content-Type': "application/json",
    'Accept': "application/json",
    'X-Auth-Token': "redptv84kmlgfed97l7jroa0mdknfgc"
    }

conn.request("GET", "/stores/b5ajmj9rbq/v3/catalog/products/112", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))


