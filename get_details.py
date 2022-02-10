import requests, json, os
id = "0e4638dc-c2e5-41b8-b6dd-e5f38df5ea95"

def get_details(id):
  result = requests.get(
        "https://creativecommons.tankerkoenig.de/json/detail.php",
        params={
            "apikey": os.environ.get("TANK_API"),
            "id": id
        }
    ).json()

  if result['status'] == 'error':
    print("Please check the provided id:", id)
    exit()

  adress = f"{result['station']['street']}{result['station']['houseNumber']}, {result['station']['postCode']:05} {result['station']['place']}"
  return [result['station']['id'], result['station']['name'], adress]
