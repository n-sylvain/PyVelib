import sqlite3
import json
import glob


def process_and_insert_data():
    conn = sqlite3.connect("velib_data.db")
    c = conn.cursor()

    for file in glob.glob("data/station_status_*.json"):
        with open(file) as f:
            data = json.load(f)
            for station in data["data"]["stations"]:
                # Safely get values with defaults
                num_ebikes = next(
                    (
                        bike["ebike"]
                        for bike in station["num_bikes_available_types"]
                        if "ebike" in bike
                    ),
                    0,
                )
                num_mechanical_bikes = next(
                    (
                        bike["mechanical"]
                        for bike in station["num_bikes_available_types"]
                        if "mechanical" in bike
                    ),
                    0,
                )

                c.execute(
                    """
                    INSERT INTO station_status (
                        station_id, num_bikes_available, num_ebikes_available,
                        num_docks_available, last_reported
                    ) VALUES (?, ?, ?, ?, ?)
                """,
                    (
                        station["station_id"],
                        station["num_bikes_available"],
                        num_ebikes,
                        station["num_docks_available"],
                        station["last_reported"],
                    ),
                )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    process_and_insert_data()
