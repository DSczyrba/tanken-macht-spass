import requests, os, json
from get_id import get_ids


data = get_ids("50.7278999", "12.9094443", "3")
data = [",".join(data[i:i+10]) for i in range(0, len(data), 10)]



for i in data:
  results = requests.get(
      "https://creativecommons.tankerkoenig.de/json/prices.php",
      params={
          "apikey": os.environ.get("TANK_API"),
          "ids": i

      }
  ).json()


  if results['ok'] is False:
    print("Daten konnten nicht geladen werden...")
    exit()



  for x in results['prices']:
    if results['prices'][x]['status'] == "closed":
      print("Tankstelle hat zu...")
    print(results['prices'][x])

