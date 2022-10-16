import requests
import json
import pandas as pd

url = "https://furballs.com/api/graphql/"
furball_num = 991

query = """ query furballByNumber($num: Int!) {
    searchFurballs(filters: {number: $num}) {
        nodes {
            id
            name
            number
            bossBattleCount
        }
    }
}"""

variables = {'num': furball_num}

r = requests.post(url, json={'query': query, 'variables': variables})
print(r.status_code)
print(r.text)
