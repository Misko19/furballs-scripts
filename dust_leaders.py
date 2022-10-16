import requests
import json
import pandas as pd
from tqdm import tqdm

url = "https://furballs.com/api/graphql/"

query1 = """ query getFurballs($after:String) {
    searchFurballs(first:100 after:$after) {
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
        pageInfo {
            hasNextPage
            endCursor
        }
    }
}
"""

after = None
has_next_page = True
owners = {}
while(has_next_page):
    variables1 = {'after': after}
    r = requests.post(url, json={'query': query1, 'variables': variables1})
    # print(r.status_code)
    # print(r.text)

    json_data = json.loads(r.text)

    furballs = json_data['data']['searchFurballs']['nodes']
    has_next_page = json_data['data']['searchFurballs']['pageInfo']['hasNextPage']
    after = json_data['data']['searchFurballs']['pageInfo']['endCursor']
    # df = pd.DataFrame(owner)
    # print(df)

    # print(json.dumps(furballs, indent=4))

    for furball in tqdm(furballs):
        owner = furball['owner']
        owner_id = owner['id']
        query2 = '''query getDustTotal($accountId: String!)
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
        variables2 = {'accountId': owner_id}
        if not owner_id in owners:
            r = requests.post(
                url, json={'query': query2, 'variables': variables2})
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

leaders = sorted(
    owners.items(), key=lambda k_v: k_v[1]['dust'], reverse=True)

i = 1
for leader in leaders:
    # print(leader)
    print(f"{i} - {leader[1]['name']} - {leader[1]['dust']}")
    i += 1
    if i > 25:
        break
