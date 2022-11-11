import requests
import json
import pandas as pd
import datetime as dt

url = "https://furballs.com/api/graphql/"

furball_num = 434

query = """ query furballByNumber($num: Int!) {
    searchFurballs(filters: {number: $num}) {
        nodes {
            id
            tokenId
            name
            number
            bossBattleCount
            owner {
                username
            }
            activeRentalAgreement {
                wFurEarned
            }
            zone
            state {
                zone
            }
        }
    }
}"""

variables = {'num': furball_num}

r = requests.post(url, json={'query': query, 'variables': variables})
json_data = json.loads(r.text)
print(json.dumps(json_data, indent=4))
furball_id = json_data['data']['searchFurballs']['nodes'][0]['id']
print(json_data)
