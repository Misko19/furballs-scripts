import requests
import json

url = "https://opensea13.p.rapidapi.com/assets"

querystring = {"collection_slug": "furballs-com-official",
               "order_direction": "desc", "limit": "50", "include_orders": "true"}

headers = {
    "X-RapidAPI-Key": "be48cd5a76mshf7ae1b81a77dd26p14dbb1jsn9eef395c4111",
    "X-RapidAPI-Host": "opensea13.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

# print(response.text)

json_data = json.loads(response.text)

for asset in json_data['assets']:
    token_id = asset['token_id']
    if asset['seaport_sell_orders'] is not None:
        for order in asset['seaport_sell_orders']:
            if "current_price" in order:
                price = int(order['current_price']) / (10**18)
                print(f"Price: {price} ETH")
                print(
                    f"https://opensea.io/assets/ethereum/0x2d004b72d8b7d36f9da2e4a14516618bf53bac57/{token_id}"
                )
