import requests
import sqlite3
from datetime import datetime
import time

API_URLS = {
    "system_information": "https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/system_information.json",
    "station_information": "https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/station_information.json",
    "station_status": "https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/station_status.json",
}


def fetch_data():
    data = {}
    for name, url in API_URLS.items():
        response = requests.get(url)
        data[name] = response.json()
    return data


def store_data(data):
    conn = sqlite3.connect("velib_data.db")
    c = conn.cursor()

    # Refresh data for non-historical tables
    for name, json_data in data.items():
        if name != "station_status":
            c.execute(
                f"""
                DELETE FROM {name}
            """
            )
            c.execute(
                f"""
                INSERT INTO {name} (data) VALUES (?)
            """,
                (str(json_data),),
            )

    # Insert historical data for station_status
    now = datetime.now().isoformat()  # Convert datetime to ISO format string
    for station in data["station_status"]["data"]["stations"]:
        c.execute(
            """
            INSERT INTO station_status (
                fetched_at, station_id, is_installed, is_renting, is_returning,
                last_reported, numBikesAvailable, numDocksAvailable, num_bikes_available,
                num_bikes_available_ebike, num_bikes_available_mechanical, num_docks_available
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                now,
                station.get("station_id"),
                station.get("is_installed"),
                station.get("is_renting"),
                station.get("is_returning"),
                station.get("last_reported"),
                station.get("numBikesAvailable"),
                station.get("numDocksAvailable"),
                station.get("num_bikes_available"),
                station.get("num_bikes_available_types", [{}])[0].get("ebike"),
                station.get("num_bikes_available_types", [{}])[0].get("mechanical"),
                station.get("num_docks_available"),
            ),
        )

    conn.commit()
    conn.close()


def main():
    while True:
        data = fetch_data()
        store_data(data)
        print(f"Data fetched and stored at {datetime.now()}")
        time.sleep(60)  # Sleep for 1 minute


if __name__ == "__main__":
    main()
