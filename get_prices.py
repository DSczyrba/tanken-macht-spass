import requests, os, json
from get_id import get_ids


data = requests.get(
    "https://creativecommons.tankerkoenig.de/json/prices.php",
    params={
        "apikey": os.environ.get("TANK_API"),
        "ids": ",".join(get_ids())

    }
).json()


if data['ok'] is False:
  print("Daten konnten nicht geladen werden...")
  exit()


for x in data['prices']:
  print(data['prices'][x])
