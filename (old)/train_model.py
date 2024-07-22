import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle


def train_model():
    conn = sqlite3.connect("velib_data.db")
    df = pd.read_sql_query("SELECT * FROM features", conn)

    # Features and target
    X = df[["hour", "day_of_week"]]
    y = df["num_bikes_available"]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Save the model
    with open("bike_availability_model.pkl", "wb") as f:
        pickle.dump(model, f)

    conn.close()


if __name__ == "__main__":
    train_model()
