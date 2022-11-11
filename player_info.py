import requests
import json
import pandas as pd

url = "https://furballs.com/api/graphql/"
address = "0x0277BcdE037e0B17e153A96a08C8DA79d93B708D"

query = """ query getAccountInfo($address:String!) {
    player(query: $address) {
        ... on FurAccount {
            id
            name
            furballsOwned
            balanceFur
            wFur
            bossBattleCount
            furballs {
                id
                tokenId
                name
                number
                level
                zone
                skillUpgradesAvailable
                info {
                    image
                }
                battleStats {
                    skills {
                        definition {
                            name
                            icon
                        }            
                        slotIndex
                        level
                        maxUses
                    }
                    currentStats {
                        attackPower
                        critAttackPower
                        critRate
                        defencePower
                        maxHealth
                        buff
                        deBuff
                        heal
                        speed
                    }
                }
                rentalAgreements {
                    id
                    isActive
                    duration
                    autoRenew
                    player {
                        id
                        name
                    }
                }
            }
            inventory {
                totalDustCount
                items {
                    ... on MaterialItem {
                        name
                        stack
                    }
                }
            }
            transactions {
                amount
                from
                to
                token {
                    name
                    symbol
                    schema
                }
            }
        }
        ... on FurPlayer {
            id
            name 
            furballsOwned
            wFur
            bossBattleCount
            inventory {
                totalDustCount
                items {
                    ... on MaterialItem {
                        name
                        stack
                    }
                }
            }
        }
        ... on FurScholar {
            id
            name
            furballsOwned
            wFur
            bossBattleCount
            inventory {
                totalDustCount
                items {
                    ... on MaterialItem {
                        name
                        stack
                    }
                }
            }
        }
    }
}"""

variables = {"address": address}
r = requests.post(url, json={'query': query, 'variables': variables})
# print(r.status_code)
# print(r.text)

json_data = json.loads(r.text)


#print(json.dumps(json_data, indent=4))
with open(f"output/player_info.json", 'w') as f:
    f.write(json.dumps(json_data, indent=1))
