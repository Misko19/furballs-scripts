import requests
import json
import pandas as pd

url = "https://furballs.com/api/graphql/"

query = """ query {
    bossBattles {
        nodes {
            id
            playerId
        }
        pageInfo {
            hasNextPage
        }
        totalCount
    }
}"""


r = requests.post(url, json={'query': query})
print(r.status_code)
print(r.text)

json_data = json.loads(r.text)

df_data = json_data['data']['bossBattles']['nodes']
df = pd.DataFrame(df_data)

print(df)
