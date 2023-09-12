import requests
import json
import copy
import random as rand

catagories = {0:"cha",1:"con",2:"dex",3:"int",4:"str",5:"wis"}

character = {
    "name":"placeholder",
    "stats": {"cha":0,"con":0,"dex":0,"int":0,"str":0,"wis":0},
    "race":"human",
    "alignment": "neutral",
    "background": "none",
    "speed": 0,
    "features": [],
    "proficiencies": [],
    "traits": [],
    "languages": [],
    "skills": [],
    "personality_traits": [],
    "ideals": [],
    "bonds": [],
    "flaws": []
}


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

def print_desc(topic):
    r = requests.get("https://www.dnd5eapi.co"+topic, headers={"Accept": "application/json"})
    desc = r.json()["desc"]
    if type(desc) == list:
        for x in desc:
            print(x+"\n")
    else:
        print(desc)

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
            print_desc("/api/ability-scores/"+catagories[lookup])

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
        for x in range(len(names)):
            print(x,":",names[x])
        
        choice = input()

        if choice.endswith("?"):
            choice = choice[:-1]
            if choice.lower() in names:
                print_desc("/api/alignments/"+indexes[names.index(choice.lower())])
            elif choice.isdigit() and int(choice) in range(len(names)):
                print_desc("/api/alignments/"+indexes[int(choice)])
            elif choice.lower() in abbr:
                print_desc("/api/alignments/"+indexes[abbr.index(choice.lower())])
            continue
        else:
            if choice.lower() in names:
                character["alignment"] = indexes[names.index(choice.lower())]
            elif choice.isdigit() and int(choice) in range(len(names)):
                character["alignment"] = indexes[int(choice)]
            elif choice.lower() in abbr:
                character["alignment"] = indexes[abbr.index(choice.lower())]
            else:
                continue
        break

def set_race():
    races = requests.get("https://www.dnd5eapi.co/api/races", headers={"Accept": "application/json"})
    race_names = []
    race_urls = []
    
    for r in races.json()["results"]:
        
        result = requests.get("https://www.dnd5eapi.co"+r["url"], headers={"Accept": "application/json"}).json()
        race_names.append(result["name"].lower())
        race_urls.append(result["url"])
        if len(result["subraces"]):
            for sr in result["subraces"]:
                race_names.append(sr["name"].lower())
                race_urls.append(sr["url"])

    while True: 
        print(race_urls)
        choice = input("Please select a race: ").lower()
        if choice in race_names:
            character["race"] = race_urls[race_names.index(choice)]
            break
    
    if "subraces" in character["race"]:
        selected_subrace = requests.get("https://www.dnd5eapi.co"+character["race"], headers={"Accept": "application/json"}).json()
        selected_race = requests.get("https://www.dnd5eapi.co"+selected_subrace["race"]["url"], headers={"Accept": "application/json"}).json()
    else:
        selected_race = requests.get("https://www.dnd5eapi.co"+character["race"], headers={"Accept": "application/json"}).json()
    print(selected_race)
    
    character["speed"] = selected_race["speed"]
    
    if selected_subrace:
        for ab in selected_subrace["ability_bonuses"]:
            character["stats"][ab["ability_score"]["index"]] += ab["bonus"]
        character["proficiencies"].extend(selected_subrace["starting_proficiencies"])
    else:
        for ab in selected_race["ability_bonuses"]:
            character["stats"][ab["ability_score"]["index"]] += ab["bonus"]
        character["proficiencies"].extend(selected_race["starting_proficiencies"])
    character["traits"].extend(selected_race["traits"])
    character["languages"].extend(selected_race["languages"])
    #Need starting profs
    #Need to finish sub races
    

#character["name"] = input("Please enter your characters name: ")
#allocate_stats(gen_stats())
#set_alignment()
set_race()

with open("test.json","w") as file:
    file.write(json.dumps(character, indent=4))

#r = requests.get("https://www.dnd5eapi.co/api/ability-scores/con", headers={"Accept": "application/json"})
#print(r.json()["index"])