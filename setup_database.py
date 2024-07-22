import sqlite3


def setup_database():
    conn = sqlite3.connect("velib_data.db")
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS station_status (
            station_id INTEGER,
            num_bikes_available INTEGER,
            num_ebikes_available INTEGER,
            num_docks_available INTEGER,
            last_reported TIMESTAMP
        )
    """
    )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    setup_database()
