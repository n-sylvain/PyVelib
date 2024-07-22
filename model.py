import sqlite3


def get_station_names():
    conn = sqlite3.connect("velib_data.db")
    c = conn.cursor()
    c.execute("SELECT station_id, name FROM station_information")
    stations = c.fetchall()
    conn.close()
    return stations
