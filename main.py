import random
import os
import json
import requests
from prometheus_client import Gauge, make_wsgi_app
from prometheus_client.core import GaugeMetricFamily, REGISTRY

if not (API_KEY := os.environ.get("TANK_API")):
  print("Please provide an API key via environment variable...")
  exit()

if not (IDS := os.environ.get("IDS")):
  print("Please specify IDS per environment variable comma separated...")
  exit()


def get_ids(lat, lng, rad):
  data = requests.get(
      "https://creativecommons.tankerkoenig.de/json/list.php",
      params={"apikey": API_KEY, "lat": lat, "lng": lng, "rad": rad, "type": "all"}).json()
  if data['status'] != "ok":
    print("Daten konnten nicht geladen werden...")
    exit()
  return [x["id"] for x in data["stations"]]

def get_details(id):
  result = requests.get(
        "https://creativecommons.tankerkoenig.de/json/detail.php",
        params={
            "apikey": API_KEY,
            "id": id
        }
    ).json()

  if result['status'] == 'error':
    print("Please check the provided id:", id)
    exit()

  adress = f"{result['station']['street']}{result['station']['houseNumber']}, {result['station']['postCode']:05} {result['station']['place']}"
  return [result['station']['id'], result['station']['name'], adress]

def get_price(id):
  result = requests.get(
        "https://creativecommons.tankerkoenig.de/json/prices.php",
        params={
            "apikey": API_KEY,
            "id": id
        }
    ).json()
  if result['ok'] is False:
    print("Data could not be loaded...")
    exit()
  if result['prices'][id]['status'] == "closed":
    return None
  return result['prices'][id]

class MyCollector:
    def __init__(self):
      self.fuel_stations = [get_details(id) for id in IDS.split(",")]
    def collect(self):
        print("custom collector called")
        g = GaugeMetricFamily("price", "fuel price", labels=["id", "name", "address", "fuel_type"])

        for station in self.fuel_stations:
          if not (price := get_price(station[0])):
            continue
          for e in ["e5", "e10", "diesel"]:
            g.add_metric([station[0], station[1], station[2], e], price[e])


        #g.add_metric(["123", "musterstraße 1", "e5"], random.randint(140, 180) / 100)
        yield g


REGISTRY.register(MyCollector())
print("export server ready")
app = make_wsgi_app()