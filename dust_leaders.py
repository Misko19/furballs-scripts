import requests
import json
import pandas as pd
from tqdm import tqdm

url = "https://furballs.com/api/graphql/"

query = """ query {
    searchFurballs(first:100) {
        nodes {
            id
            owner {
                ... on FurAccount {
                    id
                    username
                    displayName
                    furballsOwned
                    bossBattleCount
                    wFur
                    balance
                    balanceFur
                    balanceFurballs
                }
            }
        }
    }
}
"""

r = requests.post(url, json={'query': query})
print(r.status_code)
print(r.text)

json_data = json.loads(r.text)

furballs = json_data['data']['searchFurballs']['nodes']
#df = pd.DataFrame(owner)
#print(df)

print(json.dumps(furballs, indent=4))

owners = {}
for furball in tqdm(furballs):
    owner = furball['owner']
    owner_id = owner['id']
    query = '''query getDustTotal($accountId: String!) 
    {
        player(query: $accountId) {
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
        
    }
    '''
    variables = {'accountId': owner_id}
    if not owner_id in owners:
        r = requests.post(url, json={'query': query, 'variables': variables})
        json_data = json.loads(r.text)
        dust_total = json_data['data']['player']['inventory']['totalDustCount']

        owners[owner_id] = {
            'name': owner['displayName'],
            'furballsOwned': owner['furballsOwned'],
            'bossBattleCount': owner['bossBattleCount'],
            'fur': owner['balanceFur'],
            'wFur': owner['wFur'],
            'totalFur': owner['balanceFur'] + owner['wFur'],
            'dust': dust_total,
        }

leaders = sorted(owners.items(), key=lambda k_v: k_v[1]['dust'], reverse=True) 

i = 1
for leader in leaders:
    #print(leader)
    print(f"{i} - {leader[1]['name']} - {leader[1]['dust']}")
    i += 1
    if i >= 25:
        break

