import requests
import json
import pandas as pd

url = "https://furballs.com/api/graphql/"
token_id = "3405553534359963827058116864"
hex_id = "0x0b010203060009050b020900"

#query = """ query {
#   findFurball(query: "Furball #991") {
#       id
#       name
#       bossBattleCount
#       number
#   }
#}"""
#
#r = requests.post(url, json={'query': query})
#print(r.status_code)
#print(r.text)
#exit()

# activeHost {
#    name
# }
# lastAt
# isComplete
# score

query = """ query latestBossBattles($last: Int!)
{
    bossBattles(last:$last order:{createdAt: ASC}) {
        nodes {
            playerId
            player {
                ... on FurAccount {
                    username
                }
            }
            score
            furballIds
            isTrialGame
            createdAt
            worldBoss {
                name
            }
        }
        totalCount
        pageInfo {
            startCursor
            hasNextPage
            endCursor
        }
    }
}"""

variables = {'last': 100}
after = ""

r = requests.post(
    url, json={'query': query, 'variables': variables})
print(r.status_code)
#print(r.text)

json_data = json.loads(r.text)

print(json_data['data']['bossBattles']['pageInfo'])

df_data = json_data['data']['bossBattles']['nodes']
#df_data = json_data['data']['furball']
df = pd.DataFrame(df_data)

#print(df)

furball_battles = []
for battle in json_data['data']['bossBattles']['nodes']:
    if battle['isTrialGame']:
        continue
    for furball_id in battle['furballIds']:
        if furball_id == hex_id:
            battle_info = {
                "playerId": battle['playerId'],
                "playerName": battle['player']['username'],
                "boss" : battle['worldBoss']['name'],
                "partySize": len(battle['furballIds']),
                "createdAt": battle['createdAt'],
                "score": battle['score'],
            }
            furball_battles.append(battle_info) 

print(json.dumps(furball_battles, indent=4))