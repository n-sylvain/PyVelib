import requests


def get_stations():
    url = "https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/station_information.json"
    response = requests.get(url)
    data = response.json()
    return data["data"]["stations"]


def get_station_status(station_id):
    url = "https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/station_status.json"
    response = requests.get(url)
    data = response.json()
    for station in data["data"]["stations"]:
        if station["station_id"] == station_id:
            return station
    return None
