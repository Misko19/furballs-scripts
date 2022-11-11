import requests
import json
import pandas as pd

url = "https://furballs.com/api/graphql/"

query = """ query {
    skillDefinitions() {
        name
        description
        maxLevel
        maxUses 
        maxUsesBoost
        effectBonuses {
            stat
            uses
            value
            valuePerLevel
        }
    }
}"""


r = requests.post(url, json={'query': query})
print(r.status_code)
print(r.text)

json_data = json.loads(r.text)

print(json.dumps(json_data, indent=4))

#df_data = json_data['data']['skillDefinitions']
#df = pd.DataFrame(df_data)
# print(df)
