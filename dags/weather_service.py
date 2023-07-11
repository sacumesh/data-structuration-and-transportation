from typing import Union, Dict, Tuple, List

import requests
import json


def read_form_api(latitude, longitude, date) -> Union[Dict, None]:
    url = "https://api.open-meteo.com/v1/forecast"
    headers = {
        'accept': 'application/vnd.github+json',
    }

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m",
        "start_date": date,
        "end_date": date
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        forecast_data = response.json()
        return forecast_data
    else:
        print("Failed to retrieve the forecast. Status code:", response.status_code)
        return None


def process_weather_data(data: dict) -> dict:
    latitude = data["latitude"]
    longitude = data["longitude"]
    units = data["hourly_units"]["temperature_2m"]
    hourly_data = data["hourly"]
    hourly_temperature = hourly_data["temperature_2m"]
    average_temperature = sum(hourly_temperature) / len(hourly_temperature)

    res = {
        "latitude": latitude,
        "longitude": longitude,
        "average_temperature": average_temperature,
        "units": units
    }

    return res


def prepare_rows_and_fields(data: dict, timestamp: str) -> Tuple[List[list], List[str]]:
    data['timestamp'] = timestamp
    rows = [list(data.values())]
    target_fields = list(data.keys())
    return rows, target_fields


def write_to_json_file(data: dict) -> None:
    with open("dags/data/weather_data.json", 'w') as file:
        json.dump(data, file, indent=2)
