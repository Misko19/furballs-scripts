import requests
import json
import pandas as pd
import time
from string import Template

fb_api_url = "https://furballs.com/api/graphql/"
rapid_api_os_url = "https://opensea13.p.rapidapi.com/assets"

querystring = {"collection_slug": "furballs-com-official",
               "order_direction": "desc", "limit": "50", "include_orders": "true"}

headers = {
    "X-RapidAPI-Key": "be48cd5a76mshf7ae1b81a77dd26p14dbb1jsn9eef395c4111",
    "X-RapidAPI-Host": "opensea13.p.rapidapi.com"
}
#
#r = requests.get(os_api_url)
# print(r.json)


################################################################################
#
################################################################################
def main():
    with open("output/le_loot.txt", "w") as f:
        count = 0
        while True:
            ra_os_r = requests.request("GET", rapid_api_os_url,
                                       headers=headers, params=querystring)
            #os_r = requests.get(os_api_url.substitute(token_id=furball_int_id))
            # print(rapi_os_r.text)
            # print(rapi_os_r.status_code)
            ra_os_json = json.loads(ra_os_r.text)

            for_sale = False
            price = 0
            for asset in ra_os_json['assets']:
                token_id = asset['token_id']
                if asset['seaport_sell_orders'] is not None:
                    for order in asset['seaport_sell_orders']:
                        if "current_price" in order:
                            if has_le_loot(hex(int(token_id)), f):
                                price = int(order['current_price']) / (10**18)
                                print(f"Price: {price} ETH")
                                url = f"https://opensea.io/assets/ethereum/0x2d004b72d8b7d36f9da2e4a14516618bf53bac57/{token_id}"
                                print(url)
                                f.write(f"Price: {price} ETH")
                                f.write(url)
            next_cursor = ra_os_json['next']
            print(f"{count} - {next_cursor}")
            count += 1
            if next_cursor is None:
                break
            querystring['cursor'] = next_cursor
            time.sleep(5)


################################################################################
#
################################################################################
def has_le_loot(furball_id, f):
    query = """ query getFurballsEquipment($id:String!) {
        furball(tokenId:$id) {
            id
            name
            level
            zone
            skillRollCost
            skillUpgradesAvailable
            owner {
                name
                username
            }
            equipment {
                name
                rarity
                equippedBy {
                    id
                    name
                    username
                    socialName
                }
            }
            inventory {
                items {
                    ... on EquipmentItem {
                        name
                        rarity
                    }
                }
            }
        }
    }"""

    variables = {'id': furball_id}
    r = requests.post(
        fb_api_url, json={'query': query, 'variables': variables})
    # print(r.status_code)
    # print(r.text)

    json_data = json.loads(r.text)
    #print(json.dumps(furball, indent=4))
    # if furball['isListedForSale']:
    #    print(json.dumps(furball, indent=4))
    furball = json_data['data']['furball']

    equipment = furball['equipment']
    items = furball['inventory']['items']
    # if len(equipment) > 0:
    #    print(equipment)
    #    exit()
    # for item in equipment:
    #    if item['name'] == "Flowers":
    #        print(item)
    #        exit()
    le_item = False
    owner = furball['owner']['username']
    if owner == "":
        owner = furball['owner']['name']
    for item in items:
        if "name" in item:
            if ((item['rarity'] == "LEGENDARY") and
                    ((item['name'] == "Flowers") or (item['name'] == "Trash Net") or (item['name'] == "Ghost Potion"))):
                le_item = True
                print(item)
                f.write(item)
    for item in equipment:
        if "name" in item:
            if ((item['rarity'] == "LEGENDARY") and
                    ((item['name'] == "Flowers") or (item['name'] == "Trash Net") or (item['name'] == "Ghost Potion"))):
                le_item = True
                print(item)
                f.write(item)

    if le_item:
        print(f"{furball['name']} - {owner}")
        f.write(f"{furball['name']} - {owner}")
    return le_item


################################################################################
#
################################################################################
if __name__ == '__main__':
    main()
