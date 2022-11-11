from operator import itemgetter
import requests
import json
import pandas as pd
import datetime as dt

url = "https://furballs.com/api/graphql/"
date = dt.datetime.utcnow() - dt.timedelta(weeks=2)
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
                        name
                        username
                    }
                    ... on FurPlayer {
                        name
                        username
                    }
                    ... on FurScholar {
                        name
                        username
                    }
                }
                score
                furballIds
                isTrialGame
                isComplete
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
        # print(battle['score'])
        if battle['isTrialGame'] or not battle['isComplete']:
            continue
        if battle['worldBoss']['name'] != "Trashy":
            continue
        if battle['score'] is not None:
            name = battle['player']['username']
            if name == '':
                name = battle['player']['name']
            battle_info = {
                # "playerId": battle['playerId'],
                "player_name": name,
                "boss": battle['worldBoss']['name'],
                "party_size": len(battle['furballIds']),
                # "createdAt": battle['createdAt'],
                "score": battle['score'],
                # "rank": battle['percentileRank'],
                # "fur": battle['furEarned'],
                "norm_score": battle['score'] / len(battle['furballIds']),
            }
            furball_battles.append(battle_info)

leaders = sorted(furball_battles, key=itemgetter('norm_score'), reverse=True)
df_battles = pd.DataFrame(leaders[:100])
print(df_battles)
with open("output/top_normalized_scores.txt", 'w') as f:
    f.write(df_battles.to_string())
#print(json.dumps(furball_battles, indent=4))
