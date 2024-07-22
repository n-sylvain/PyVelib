from flask import Flask, render_template, request
from predict import get_prediction, get_current_status
from model import get_station_names

app = Flask(__name__)


@app.route("/")
def index():
    stations = get_station_names()
    return render_template("index.html", stations=stations)


@app.route("/predict", methods=["POST"])
def predict():
    station_id = request.form["station_id"]
    date = request.form["date"]
    time = request.form["time"]

    current_status = get_current_status(station_id)
    prediction = get_prediction(station_id, date, time)

    return render_template(
        "index.html",
        stations=get_station_names(),
        current_status=current_status,
        prediction=prediction,
        selected_station=station_id,
    )


if __name__ == "__main__":
    app.run(debug=True)
