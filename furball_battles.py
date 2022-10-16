import requests
import json
import pandas as pd
import datetime as dt

url = "https://furballs.com/api/graphql/"

furball_num = 702

query = """ query furballByNumber($num: Int!) {
    searchFurballs(filters: {number: $num}) {
        nodes {
            id
            name
            number
            bossBattleCount
        }
    }
}"""

variables = {'num': furball_num}

r = requests.post(url, json={'query': query, 'variables': variables})
json_data = json.loads(r.text)
furball_id = json_data['data']['searchFurballs']['nodes'][0]['id']
print(furball_id)

date = dt.datetime.utcnow() - dt.timedelta(weeks=1)
date_iso = date.isoformat()

furball_battles = []
has_next_page = True
after_cursor = None
while(has_next_page):
    query = """ query latestBossBattles($date:DateTime! $after_cursor:String)
    {
        bossBattles(where:{createdAt: {gte: $date}} order:{createdAt: DESC} after:$after_cursor first:100) {
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
                percentileRank
                furEarned
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

    print(after_cursor)
    #variables = {'after': cursor, 'date': date_iso}
    variables = {'date': date_iso, 'after_cursor': after_cursor}

    r = requests.post(
        url, json={'query': query, 'variables': variables})
    # print(r.status_code)
    # print(r.text)
    json_data = json.loads(r.text)

    has_next_page = json_data['data']['bossBattles']['pageInfo']['hasNextPage']
    after_cursor = json_data['data']['bossBattles']['pageInfo']['endCursor']

    print(json_data['data']['bossBattles']['pageInfo'])
    print(json_data['data']['bossBattles']['totalCount'])

    battles = json_data['data']['bossBattles']['nodes']
    #df = pd.DataFrame(battles)
    # print(df)

    for battle in battles:
        if battle['isTrialGame']:
            continue
        if furball_id in battle['furballIds']:
            battle_info = {
                "playerId": battle['playerId'],
                "playerName": battle['player']['username'],
                "boss": battle['worldBoss']['name'],
                "partySize": len(battle['furballIds']),
                # "createdAt": battle['createdAt'],
                "score": battle['score'],
                "rank": battle['percentileRank'],
                "fur": battle['furEarned']
            }
            furball_battles.append(battle_info)

df_battles = pd.DataFrame(furball_battles)
print(df_battles)
#print(json.dumps(furball_battles, indent=4))
