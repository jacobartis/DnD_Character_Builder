import requests
import json
import copy
import random as rand

catagories = {0:"cha",1:"con",2:"dex",3:"int",4:"str",5:"wis"}

character = {
    "name":"placeholder",
    "stats": {"cha":0,"con":0,"dex":0,"int":0,"str":0,"wis":0},
    "race":"human"
}

#character["name"] = input("Please enter your characters name: ")

#Generates stat array
def gen_stats(stats=[]):
    stats = copy.deepcopy(stats)
    rand.seed(rand.random())
    numbers = []
    for x in range(4):
        numbers.append(rand.randint(1,6))
    numbers.sort(reverse=True)
    numbers.pop()
    stats.append(sum(numbers))
    if len(stats) >= 6:
        return stats
    else:
        return gen_stats(stats)

def get_desc(topic):
    r = requests.get("https://www.dnd5eapi.co/api/ability-scores/"+topic, headers={"Accept": "application/json"})
    desc = r.json()["desc"]
    for x in desc:
        print(x)


def allocate_stats(aval_stats):
    while len(aval_stats) > 0:
        
        print("\nAvalible stats:",aval_stats)
        print("Your current stats:",character["stats"],"\n")
        x = input("Please allocate "+ str(aval_stats[0])+": ")

        if x.isdigit():
            x = int(x)

        elif x.lower() == "r" or x.lower() == "reroll" :
            check = input("Are you sure you want to reroll? ")
            if check.lower() == "y" or check.lower() == "yes":
                for x in catagories:
                    character["stats"][catagories[x]] = 0
                aval_stats = gen_stats()
            continue
        
        elif x[0].isdigit() and x.endswith("?"):
            lookup = int(x[0])
            if not lookup in catagories:
                continue
            get_desc(catagories[lookup])

        elif x.lower() in list(character["stats"].keys()):
            x = list(catagories.values()).index(x.lower())
            print(x)
        
        else:
            print("\nPlease enter valid value:",catagories,"\n")
            continue

        if x in catagories:
            if character["stats"][catagories[x]] > 0:
                aval_stats.append(character["stats"][catagories[x]])
            character["stats"][catagories[x]] = aval_stats.pop(0)

allocate_stats(gen_stats())

#with open("test.json","w") as file:
#    file.write(json.dumps(character, indent=4))

r = requests.get("https://www.dnd5eapi.co/api/ability-scores/con", headers={"Accept": "application/json"})
print(r.json()["index"])