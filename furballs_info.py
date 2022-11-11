import requests
import json
import pandas as pd

url = "https://furballs.com/api/graphql/"

# query = """ query {
#    searchFurballs(where: {id: { in: ["0x110a04060a000f0709091000", "0x90403060300090a0a050f00"]}} first: 100) {
#        nodes {
#            id
#            name
#            level
#            zone
#            skillRollCost
#            skillUpgradesAvailable
#        }
#    }
# }"""

int_ids = [
    "5273353426026000844176560128",
    "2486807690168527033169220352"
]


hex_ids = []
for id in int_ids:
    print(f"id: {id}")
    int_id = int(id)
    print(f"int id: {int_id}")
    hex_id = hex(int_id)
    hex_id = f"0x{int_id:024x}"
    print(f"hex id: {hex_id}")
    hex_ids.append(hex_id)


query = """ query getFurballs($ids: [String!]!) {
    searchFurballs(where: {id: {in: $ids}}) {
        nodes {
            id
            name
            level
            zone
            skillRollCost
            skillUpgradesAvailable
            owner {
                ... Owner
            }
            equipment {
                id
                name
                rarity
            }
            info {
                image
            }
        }
    }
}

fragment Owner on FurAccount {
    name
    username
}

"""

query2 = """ query getFurballs($ids: [String!]!) {
    searchFurballs(where: {id: {in: $ids}}) {
        nodes {
            id
            name
            level
            zone
            skillRollCost
            skillUpgradesAvailable
            info {
                image
            }
            owner {
                username
            }
            equipment {
                ... on EquipmentItem {
                    id
                    name
                    rarity
                }
            }
        }
    }
}"""


variables = {"ids": hex_ids}
r = requests.post(url, json={'query': query, 'variables': variables})
print(r.status_code)
# print(r.text)

json_data = json.loads(r.text)

print(json.dumps(json_data, indent=4))

#df_data = json_data['data']['bossBattles']['nodes']
#df = pd.DataFrame(df_data)
# print(df)
