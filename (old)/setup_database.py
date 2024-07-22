import sqlite3


def setup_database():
    conn = sqlite3.connect("velib_data.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS station_status (
            station_id INTEGER PRIMARY KEY,
            num_bikes_available INTEGER,
            num_ebikes_available INTEGER,
            num_docks_available INTEGER,
            last_reported INTEGER
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS station_information (
            station_id INTEGER PRIMARY KEY,
            name TEXT,
            capacity INTEGER,
            lat REAL,
            lon REAL
        )
    """
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    setup_database()
