import requests
import json
import pandas as pd

url = "https://furballs.com/api/graphql/"

query = """ query {
    player(query: "0x0277BcdE037e0B17e153A96a08C8DA79d93B708D") {
        ... on FurAccount {
            inventory {
                totalDustCount
            }
        }
        ... on FurPlayer {
            inventory {
                totalDustCount
            }
        }
    }
}"""


r = requests.post(url, json={'query': query})
print(r.status_code)
print(r.text)

json_data = json.loads(r.text)

print(json.dumps(json_data, indent=4))

#df_data = json_data['data']['bossBattles']['nodes']
#df = pd.DataFrame(df_data)
# print(df)
