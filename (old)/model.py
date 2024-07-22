import sqlite3


def get_station_names():
    conn = sqlite3.connect("velib_data.db")
    cursor = conn.cursor()

    cursor.execute("SELECT station_id, name FROM station_information")
    stations = cursor.fetchall()

    conn.close()
    return stations
