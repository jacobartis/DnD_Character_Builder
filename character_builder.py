import requests
import json
import copy
import random as rand

catagories = {1:"cha",2:"con",3:"dex",4:"int",5:"str",6:"wis"}

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

aval_stats = gen_stats()
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

    else:
        print("\nPlease enter valid value:",catagories,"\n")
        continue

    if x in catagories:
        if character["stats"][catagories[x]] > 0:
            aval_stats.append(character["stats"][catagories[x]])
        character["stats"][catagories[x]] = aval_stats.pop(0)

#with open("test.json","w") as file:
#    file.write(json.dumps(character, indent=4))

r = requests.get("https://www.dnd5eapi.co/api/ability-scores/con", headers={"Accept": "application/json"})
print(r.json()["index"])