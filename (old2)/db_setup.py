import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor


def train_and_save_model(data_file, target_column, model_filename):
    # Load the dataset
    df = pd.read_csv(data_file)

    # Assume that the target column is the one to predict and the rest are features
    X = df.drop(columns=[target_column])
    y = df[target_column]

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train the model
    model = RandomForestRegressor()
    model.fit(X_train, y_train)

    # Save the model
    joblib.dump(model, model_filename)
    print(f"Model saved to {model_filename}")


if __name__ == "__main__":
    # Training and saving models for bikes, e-bikes, and docks
    train_and_save_model("data/bike_data.csv", "bike_target", "models/bike_model.pkl")
    train_and_save_model(
        "data/ebike_data.csv", "ebike_target", "models/ebike_model.pkl"
    )
    train_and_save_model("data/dock_data.csv", "dock_target", "models/dock_model.pkl")
