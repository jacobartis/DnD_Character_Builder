import requests
import json

r = requests.get("https://www.dnd5eapi.co/api/ability-scores/con", headers={"Accept": "application/json"})
print(r.json()["index"])