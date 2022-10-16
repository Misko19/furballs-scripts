import requests
import json
import pandas as pd

url = "https://furballs.com/api/graphql/"
furball_id = "0x010101010900070b04070e00"
furball_id = "0x0508050f060007060b051a00"

query = """ query getFurballEquipment($id:String!) {
    furball(tokenId:$id) {
        id
        name
        level
        zone
        skillRollCost
        skillUpgradesAvailable
        equipment {
            name
            rarity
            equippedBy {
                id
                socialName
            }
        }
    }
}"""

variables = {'id': furball_id}
r = requests.post(url, json={'query': query, 'variables': variables})
# print(r.status_code)
print(r.text)

json_data = json.loads(r.text)

#df_data = json_data['data']['furball']
#df = pd.DataFrame(df_data)
# print(df)

print(json.dumps(json_data["data"]["furball"]["equipment"], indent=4))
