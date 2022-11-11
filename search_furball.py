import requests
import json
import pandas as pd

url = "https://furballs.com/api/graphql/"
furball_num = 4853

query = """ query furballByNumber($num: Int!) {
    searchFurballs(filters: {number: $num}) {
        nodes {
            id
            name
            number
            isListedForSale
            bossBattleCount
        }
    }
}"""

variables = {'num': furball_num}

r = requests.post(url, json={'query': query, 'variables': variables})
# print(r.status_code)
# print(r.text)

json_data = json.loads(r.text)
print(json.dumps(json_data, indent=4))
