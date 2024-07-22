import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import sqlite3
import joblib


def train_models():
    conn = sqlite3.connect("db.sqlite3")
    df = pd.read_sql_query("SELECT * FROM data", conn)
    conn.close()

    df["date"] = pd.to_datetime(df["date"])
    df["hour"] = df["date"].dt.hour
    df["day_of_week"] = df["date"].dt.dayofweek
    df["weekend"] = (df["day_of_week"] >= 5).astype(int)
    df["temp_celsius"] = df["temperature"] - 273.15

    X = df.drop(
        columns=["available_bikes", "available_ebikes", "available_docks", "date"]
    )
    y_bike = df["available_bikes"]
    y_ebike = df["available_ebikes"]
    y_dock = df["available_docks"]

    X_train, X_test, y_bike_train, y_bike_test = train_test_split(
        X, y_bike, test_size=0.2
    )
    X_train, X_test, y_ebike_train, y_ebike_test = train_test_split(
        X, y_ebike, test_size=0.2
    )
    X_train, X_test, y_dock_train, y_dock_test = train_test_split(
        X, y_dock, test_size=0.2
    )

    bike_model = LinearRegression()
    bike_model.fit(X_train, y_bike_train)

    ebike_model = LinearRegression()
    ebike_model.fit(X_train, y_ebike_train)

    dock_model = LinearRegression()
    dock_model.fit(X_train, y_dock_train)

    bike_predictions = bike_model.predict(X_test)
    ebike_predictions = ebike_model.predict(X_test)
    dock_predictions = dock_model.predict(X_test)

    bike_mse = mean_squared_error(y_bike_test, bike_predictions)
    ebike_mse = mean_squared_error(y_ebike_test, ebike_predictions)
    dock_mse = mean_squared_error(y_dock_test, dock_predictions)

    print(f"Bike MSE: {bike_mse:.2f}")
    print(f"Ebike MSE: {ebike_mse:.2f}")
    print(f"Dock MSE: {dock_mse:.2f}")

    joblib.dump(bike_model, "models/bike_model.pkl")
    joblib.dump(ebike_model, "models/ebike_model.pkl")
    joblib.dump(dock_model, "models/dock_model.pkl")
