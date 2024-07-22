import sqlite3
import pandas as pd


def create_features():
    conn = sqlite3.connect("velib_data.db")
    df = pd.read_sql_query("SELECT * FROM station_status", conn)

    # Convert timestamp to datetime
    df["last_reported"] = pd.to_datetime(df["last_reported"], unit="s")

    # Create time-based features
    df["hour"] = df["last_reported"].dt.hour
    df["day_of_week"] = df["last_reported"].dt.dayofweek

    # Save the processed DataFrame
    df.to_sql("features", conn, if_exists="replace", index=False)
    conn.close()


if __name__ == "__main__":
    create_features()
