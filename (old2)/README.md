# Vélib Bike Availability Predictor

## Overview
This project predicts the availability of bikes, e-bikes, and docks at Vélib stations in Paris based on historical data and current weather conditions. It uses a Flask web application to interact with users and display predictions.

## File Structure
- `api/`: Contains scripts for fetching data from Vélib and weather APIs.
- `data/`: Contains raw and processed data.
- `models/`: Contains trained models and scripts for training them.
- `templates/`: Contains HTML templates for the web application.
- `app.py`: Main Flask application script.
- `db.sqlite3`: SQLite database for storing data.
- `README.md`: This file.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/velib-predictor.git
    cd velib-predictor
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up your environment variables (e.g., for the weather API key):
    ```bash
    export WEATHER_API_KEY="your_weather_api_key"
    ```

5. Initialize the database and train models:
    ```bash
    python models/train.py
    ```

6. Run the Flask application:
    ```bash
    python app.py
    ```

## Usage
1. Navigate to `http://127.0.0.1:5000/` in your web browser.
2. Select a Vélib station, date, and time.
3. Click "Predict" to see the availability predictions.

## API Keys
- Obtain an API key for OpenWeatherMap from [OpenWeatherMap](https://openweathermap.org/api).

## Contributing
Feel free to open issues or submit pull requests.

## License
This project is licensed under the MIT License.