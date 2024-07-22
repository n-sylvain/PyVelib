import sqlite3
import pandas as pd
from datetime import datetime
import joblib

# Load your trained model (assuming you have saved it using joblib)
# model = joblib.load("velib_model.pkl")
model = joblib.load("bike_availability_model.pkl")


def get_current_status(station_id):
    conn = sqlite3.connect("velib_data.db")
    c = conn.cursor()
    c.execute(
        "SELECT num_ebikes_available, num_bikes_available, num_docks_available FROM station_status WHERE station_id = ?",
        (station_id,),
    )
    current_status = c.fetchone()
    conn.close()
    return current_status


def get_prediction(station_id, date, time):
    conn = sqlite3.connect("velib_data.db")
    df = pd.read_sql_query("SELECT * FROM features", conn)
    conn.close()

    # Parse date and time
    dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    hour = dt.hour
    day_of_week = dt.weekday()

    # Create feature vector for prediction
    X = df[
        (df["station_id"] == int(station_id))
        & (df["hour"] == hour)
        & (df["day_of_week"] == day_of_week)
    ]
    if X.empty:
        return None

    # Make prediction
    prediction = model.predict(X)
    return prediction[0]
