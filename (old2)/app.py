from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import joblib
from api.velib_api import get_stations, get_station_status
from api.weather_api import get_weather

app = Flask(__name__)

# Load models
bike_model = joblib.load("models/bike_model.pkl")
ebike_model = joblib.load("models/ebike_model.pkl")
dock_model = joblib.load("models/dock_model.pkl")


def get_data():
    conn = sqlite3.connect("db.sqlite3")
    df = pd.read_sql_query("SELECT * FROM data", conn)
    conn.close()
    return df


def predict_availability(station_id, date, time):
    df = get_data()

    df["date"] = pd.to_datetime(df["date"])
    df["hour"] = df["date"].dt.hour
    df["day_of_week"] = df["date"].dt.dayofweek
    df["weekend"] = (df["day_of_week"] >= 5).astype(int)
    df["temp_celsius"] = df["temperature"] - 273.15

    station_df = df[df["station_id"] == station_id]

    input_data = pd.DataFrame(
        {
            "hour": [time.hour],
            "day_of_week": [time.weekday()],
            "weekend": [int(time.weekday() >= 5)],
            "temp_celsius": [station_df["temp_celsius"].mean()],
        }
    )

    bike_prediction = bike_model.predict(input_data)[0]
    ebike_prediction = ebike_model.predict(input_data)[0]
    dock_prediction = dock_model.predict(input_data)[0]

    station_status = get_station_status(station_id)
    if station_status is None:
        return None

    current_bikes = station_status["num_bikes_available"]
    current_ebikes = station_status["num_bikes_available_types"][0]["ebike"]
    current_docks = station_status["num_docks_available"]

    capacity = station_status["capacity"]
    bike_percentage = np.clip(bike_prediction / capacity, 0, 1) * 100
    ebike_percentage = np.clip(ebike_prediction / capacity, 0, 1) * 100
    dock_percentage = np.clip(dock_prediction / capacity, 0, 1) * 100

    return {
        "station_id": station_id,
        "current_bikes": current_bikes,
        "current_ebikes": current_ebikes,
        "current_docks": current_docks,
        "predicted_bikes": bike_percentage,
        "predicted_ebikes": ebike_percentage,
        "predicted_docks": dock_percentage,
    }


@app.route("/")
def index():
    stations = get_stations()
    return render_template("index.html", stations=stations)


@app.route("/predict", methods=["POST"])
def predict():
    station_id = int(request.form["station_id"])
    date = pd.to_datetime(request.form["date"])
    time = pd.to_datetime(request.form["time"]).time()
    prediction = predict_availability(station_id, date, time)
    stations = get_stations()
    return render_template("index.html", stations=stations, prediction=prediction)


if __name__ == "__main__":
    app.run(debug=True)
