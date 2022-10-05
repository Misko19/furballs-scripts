import requests
import json
import pandas as pd

url = "https://furballs.com/api/graphql/"

# query = """ query {
#    furball(tokenId: "0x050809060900090408080700") {
#        id
#        name
#        bossBattleCount
#        battles {
#            id
#        }
#    }
# }"""

# activeHost {
#    name
# }
# lastAt
# isComplete
# score

query = """ query latestBossBattles($last: Int!)
{
    bossBattles(last:$last) {
        nodes {
            playerId
            score
            furballIds
        }
        totalCount
        pageInfo {
            startCursor
            hasNextPage
            endCursor
        }
    }
}"""

variables = {'last': 50}
after = ""

r = requests.post(
    url, json={'query': query, 'variables': variables})
print(r.status_code)
print(r.text)

json_data = json.loads(r.text)

print(json_data['data']['bossBattles']['pageInfo'])

df_data = json_data['data']['bossBattles']['nodes']
#df_data = json_data['data']['furball']
df = pd.DataFrame(df_data)

print(df)
