import requests
import json
import pandas as pd

url = "https://furballs.com/api/graphql/"
furball_id = "0x010101010900070b04070e00"
furball_id = "0x0508050f060007060b051a00"
furball_id = "0x080503100700030b06000a00"
furball_id = "0x8090a030300010507021300"

query = """ query {
    furball(tokenId: "0x050809060900090408080700") {
        id
        name
        level
        zone
        skillRollCost
        skillUpgradesAvailable
        owner {
            username
        }
        equipment {
            definition {
                name
            }
            equippedBy {
                id
                socialName
            }
        }
    }
}"""

r = requests.post(url, json={'query': query})
# print(r.status_code)
# print(r.text)

json_data = json.loads(r.text)

#df_data = json_data['data']['furball']
#df = pd.DataFrame(df_data)
# print(df)

#print(json.dumps(json_data["data"]["furball"]["equipment"], indent=4))
print(json.dumps(json_data["data"]["furball"], indent=4))
