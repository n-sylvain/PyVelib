from flask import Flask, render_template, request
from model import get_station_names

app = Flask(__name__)


@app.route("/")
def index():
    stations = get_station_names()
    return render_template("index.html", stations=stations)


if __name__ == "__main__":
    app.run(debug=True)
