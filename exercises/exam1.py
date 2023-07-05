import requests
import json


def task1():
    base_url = "https://api.openweathermap.org/data/2.5/forecast"

    headers = {
        "Accept": "application/json"
    }

    # Replace with your own values
    params = {
        "q": "Paris,FR",  # City name and country code
        "appid": "6b302a0dcd0b8cec144fee14eb3468b2"  # Your API key
    }

    response = requests.get(base_url, params=params, headers=headers)
    data = response.json()

    # Process the data as needed
    return json.dumps(data)


def write_json_to_file(json_data, filename):
    with open(filename, 'w') as file:
        json.dump(json_data, file, indent=2)


def task2(data):
    json_data = json.loads(data)
    with open("test.json", 'w') as file:
        json.dump(json_data, file, indent=2)

task2(task1())
