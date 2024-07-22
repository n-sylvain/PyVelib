import sqlite3


def print_sample_data(table_name, num_rows):
    conn = sqlite3.connect("velib_data.db")
    cursor = conn.cursor()

    # Get the header (column names) of the specified table
    cursor.execute(f"PRAGMA table_info({table_name})")
    header = [column[1] for column in cursor.fetchall()]

    # Fetch the specified number of rows from the table
    cursor.execute(f"SELECT * FROM {table_name} LIMIT {num_rows}")
    rows = cursor.fetchall()

    conn.close()

    # Print the header and rows
    print(f"Sample data from the '{table_name}' table:")
    print(header)
    for row in rows:
        print(row)


# Replace the following values with the desired table name and number of rows to display
table_name = "station_status"
num_rows = 5

print_sample_data(table_name, num_rows)
