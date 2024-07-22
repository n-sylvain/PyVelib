import requests
import json
import time


def fetch_station_status():
    url = "https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/station_status.json"
    response = requests.get(url)
    return response.json()


def save_data(data):
    timestamp = int(time.time())
    filename = f"data/station_status_{timestamp}.json"
    with open(filename, "w") as file:
        json.dump(data, file)


if __name__ == "__main__":
    data = fetch_station_status()
    save_data(data)
