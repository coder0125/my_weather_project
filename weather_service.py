import requests
from config import API_KEY, CITIES
from db import store_weather_data

def kelvin_to_celsius(kelvin_temp):
    """Convert temperature from Kelvin to Celsius."""
    return kelvin_temp - 273.15

def get_weather_data():
    """Fetch weather data for each city and store it in the database."""
    for city in CITIES:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
            data = response.json()

            # Validate required fields in the response
            if 'main' in data and 'weather' in data and 'dt' in data and 'name' in data:
                process_weather_data(data)
            else:
                print(f"Unexpected data structure for city: {city}")

        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data for city '{city}': {e}")

def process_weather_data(data):
    """Extract and store weather data from the API response."""
    try:
        temp = kelvin_to_celsius(data['main']['temp'])
        feels_like = kelvin_to_celsius(data['main']['feels_like'])
        condition = data['weather'][0]['main']
        timestamp = data['dt']
        city = data['name']

        # Store data in the database
        store_weather_data(city, temp, feels_like, condition, timestamp)
        
    except KeyError as e:
        print(f"Error processing weather data: Missing key {e} in response.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def get_daily_summary():
    """Retrieve and print daily weather summaries from the database."""
    # Placeholder for summary implementation
    print("Daily summary functionality not yet implemented.")
