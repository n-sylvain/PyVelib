import requests


def get_weather(lat, lon):
    api_key = "a00792162c209e694256484f6a0f8570"
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    weather = data["weather"][0]["description"]
    temperature = data["main"]["temp"]
    return weather, temperature
