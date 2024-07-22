import requests
import json
import sqlite3


# Fetch data from the API and store it in the SQLite database
def fetch_and_store_data():
    # Connect to the SQLite database
    conn = sqlite3.connect("velib_data.db")
    cursor = conn.cursor()

    # Fetch station_status data
    url = "https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/station_status.json"
    response = requests.get(url)
    data = response.json()

    # Store station_status data in the SQLite database
    for station in data["data"]["stations"]:
        num_ebikes_available = 0
        num_bikes_available = 0

        for bike_type in station["num_bikes_available_types"]:
            if "ebike" in bike_type and bike_type["ebike"]:
                num_ebikes_available = bike_type["ebike"]
            elif "mechanical" in bike_type and bike_type["mechanical"]:
                num_bikes_available = bike_type["mechanical"]

        cursor.execute(
            """
            INSERT INTO station_status (
                station_id,
                num_bikes_available,
                num_ebikes_available,
                num_docks_available,
                last_reported
            ) VALUES (?, ?, ?, ?, ?)
        """,
            (
                station["station_id"],
                num_bikes_available,
                num_ebikes_available,
                station["num_docks_available"],
                station["last_reported"],
            ),
        )

    # Fetch station_information data
    url = "https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/station_information.json"
    response = requests.get(url)
    data = response.json()

    # Store station_information data in the SQLite database
    for station in data["data"]["stations"]:
        cursor.execute(
            """
            INSERT INTO station_information (
                station_id,
                name,
                capacity,
                lat,
                lon
            ) VALUES (?, ?, ?, ?, ?)
        """,
            (
                station["station_id"],
                station["name"],
                station["capacity"],
                station["lat"],
                station["lon"],
            ),
        )

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


# Call the function to fetch and store the data
fetch_and_store_data()
