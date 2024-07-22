from flask import Flask, request, jsonify
import sqlite3
import pandas as pd
import pickle

app = Flask(__name__)

# Load the model
with open("bike_availability_model.pkl", "rb") as f:
    model = pickle.load(f)


@app.route("/predict", methods=["GET"])
def predict():
    station_id = request.args.get("station_id")
    date = request.args.get("date")
    time = request.args.get("time")

    # Create a datetime object from date and time
    dt = pd.to_datetime(f"{date} {time}")

    # Extract features
    hour = dt.hour
    day_of_week = dt.dayofweek

    # Make prediction
    prediction = model.predict([[hour, day_of_week]])

    return jsonify({"prediction": int(prediction[0])})


if __name__ == "__main__":
    app.run(debug=True)
