import requests
import json
import pandas as pd

url = "https://furballs.com/api/graphql/"

query = """ query {
    bossBattle(id: "430c45de-4837-4374-ab6b-7c50e2c13573") {
        player {
            ... on FurAccount {
                username
            }
        }
        score
        worldBoss {
            name
        }
        leaderboardGroup
        moves(last:100) {
            nodes {
                ranAt
                moveKind
                skill {
                    definition {
                        name
                    }
                } 
                outcomes {
                    stat
                    value
                }
            }
            pageInfo {
                hasNextPage
                endCursor
            }
            totalCount
        }
    }
}"""

r = requests.post(url, json={'query': query})
# print(r.status_code)
# print(r.text)

json_data = json.loads(r.text)


#print(json.dumps(json_data, indent=4))
with open(f"output/battle_info.json", 'w') as f:
    f.write(json.dumps(json_data, indent=1))
