import sqlite3


def create_tables():
    conn = sqlite3.connect("velib_data.db")
    c = conn.cursor()

    # Drop tables if they already exist to avoid schema issues
    c.execute("DROP TABLE IF EXISTS system_information")
    c.execute("DROP TABLE IF EXISTS station_information")
    c.execute("DROP TABLE IF EXISTS station_status")

    # Create system_information table
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS system_information (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data TEXT
        )
    """
    )

    # Create station_information table
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS station_information (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data TEXT
        )
    """
    )

    # Create station_status table with corrected schema
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS station_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            station_id INTEGER,
            is_installed INTEGER,
            is_renting INTEGER,
            is_returning INTEGER,
            last_reported INTEGER,
            numBikesAvailable INTEGER,
            numDocksAvailable INTEGER,
            num_bikes_available INTEGER,
            num_bikes_available_ebike INTEGER,
            num_bikes_available_mechanical INTEGER,
            num_docks_available INTEGER,
            UNIQUE (station_id, fetched_at)  -- Unique constraint to avoid duplicates
        )
    """
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
