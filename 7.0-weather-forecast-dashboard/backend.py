import os

import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPEN_WEATHER_API_KEY")


def get_data(place):
    try:
        response = requests.get(
            f"https://api.openweathermap.org/data/2.5/forecast?q={place}&appid={api_key}&units=metric"
        )
        response.raise_for_status()
        data = response.json()
        return {"data": data, "error": None}
    except requests.exceptions.HTTPError as err:
        return {"data": None, "error": err}
