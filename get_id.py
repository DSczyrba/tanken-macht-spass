import requests, os, json

data = requests.get(
    "https://creativecommons.tankerkoenig.de/json/list.php",
    params={
        "apikey": os.environ.get("TANK_API"),
        "lat": "50.7278999",
        "lng": "12.9094443",
        "rad": "5",
        "type": "all"
    }
).json()

if data['status'] != "ok":
  print("Daten konnten nicht geladen werden...")
  exit()

for x in data['stations']:
  print(f"Name: {x['name']} ID: {x['id']}")
