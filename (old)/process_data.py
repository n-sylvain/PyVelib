import sqlite3
import pandas as pd
import glob
import json


def process_and_insert_data():
    conn = sqlite3.connect("velib_data.db")

    # Process and insert station_status data
    for file in glob.glob("data/station_status_*.json"):
        with open(file) as f:
            data = json.load(f)

        df = pd.DataFrame(data["data"]["stations"])

        df = df.explode("num_bikes_available_types")
        df[["num_bikes_available", "num_ebikes_available"]] = pd.DataFrame(
            df["num_bikes_available_types"].tolist()
        )
        df = df.drop(
            columns=[
                "num_bikes_available_types",
                "numBikesAvailable",
                "numDocksAvailable",
                "is_installed",
                "is_returning",
                "is_renting",
                "stationCode",
            ]
        )

        df.to_sql("station_status", conn, if_exists="append", index=False)

    # Process and insert station_information data
    file = "data/station_information.json"
    with open(file) as f:
        data = json.load(f)

    df = pd.DataFrame(data["data"]["stations"])
    df.to_sql("station_information", conn, if_exists="append", index=False)

    conn.close()


if __name__ == "__main__":
    process_and_insert_data()
