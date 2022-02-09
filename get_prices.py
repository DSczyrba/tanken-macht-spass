import requests, os, json

data = requests.get(
    "https://creativecommons.tankerkoenig.de/json/prices.php",
    params={
        "apikey": os.environ.get("TANK_API"),
        "ids": "0e4638dc-c2e5-41b8-b6dd-e5f38df5ea95,a5141b3c-9d0d-443b-9d14-feb78ba8c4a9"

    }
).json()


if data['ok'] is False:
  print("Daten konnten nicht geladen werden...")
  exit()


print(data)
