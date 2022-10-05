import requests
import json
import pandas as pd

url = "https://furballs.com/api/graphql/"

query = """ query {
    account(id: "0x0277BcdE037e0B17e153A96a08C8DA79d93B708D") {
        furballs {
            id
            name
            level
            zone
            skillRollCost
            skillUpgradesAvailable
            equipment {
                definition {
                    name
                }
            }
            inventory {
                items {
                    id
                }
            }
        }
    }
}"""


r = requests.post(url, json={'query': query})
print(r.status_code)
print(r.text)

json_data = json.loads(r.text)

df_data = json_data['data']['account']['furballs']
df = pd.DataFrame(df_data)

print(df)
