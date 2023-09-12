import requests
import json
import copy
import random as rand

catagories = {0:"cha",1:"con",2:"dex",3:"int",4:"str",5:"wis"}

character = {
    "name":"placeholder",
    "stats": {"cha":0,"con":0,"dex":0,"int":0,"str":0,"wis":0},
    "alignment": "neutral",
    "languages": "common",
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

def set_alignment():
    print("\nPlease select an alignment")
    alignments = requests.get("https://www.dnd5eapi.co/api/alignments", headers={"Accept": "application/json"})
    names = []
    abbr = []
    indexes = []
    for x in range(len(alignments.json()["results"])):
        result = alignments.json()["results"][x]
        names.append(result["name"].lower())
        abbr.append(requests.get("https://www.dnd5eapi.co"+result["url"], headers={"Accept": "application/json"}).json()["abbreviation"].lower())
        indexes.append(result["index"])
    
    while True: 
        for x in names:
            print(x,":",names[x])
        
        choice = input()
        
        if choice.lower() in names:
            character["alignment"] = indexes[names.index(choice.lower())]
        elif choice.isdigit() and int(choice) in range(len(names)):
            character["alignment"] = indexes[int(choice)]
        elif choice.lower() in abbr:
            character["alignment"] = indexes[abbr.index(choice.lower())]
        else:
            continue
        break

#allocate_stats(gen_stats())
set_alignment()

with open("test.json","w") as file:
    file.write(json.dumps(character, indent=4))

#r = requests.get("https://www.dnd5eapi.co/api/ability-scores/con", headers={"Accept": "application/json"})
#print(r.json()["index"])