import requests
import json
import pandas as pd

url = "https://furballs.com/api/graphql/"
furball_num = 3918

query = """ query furballByNumber($num: Int!) {
    searchFurballs(filters: {number: $num}) {
        nodes {
            id
            tokenId
            name
            number
        }
    }
}"""


variables = {'num': furball_num}

r = requests.post(url, json={'query': query, 'variables': variables})

json_data = json.loads(r.text)
furball_token_id = json_data['data']['searchFurballs']['nodes'][0]['tokenId']

query = """ query getFurballSkills($id:String!) {
    furball(tokenId:$id) {
        id
        name
        level
        zone
        skillRollCost
        skillUpgradesAvailable
        owner {
            username
        }
        rentalAgreements {
            id
            isActive
            autoRenew
            duration
            player {
                id
                name
            }
        }
    }
}"""

variables = {'id': furball_token_id}
r = requests.post(url, json={'query': query, 'variables': variables})
# print(r.status_code)
print(r.text)

json_data = json.loads(r.text)

#df_data = json_data['data']['furball']
#df = pd.DataFrame(df_data)
# print(df)

#print(json.dumps(json_data["data"]["furball"]["equipment"], indent=4))
print(json.dumps(json_data["data"]["furball"], indent=4))
