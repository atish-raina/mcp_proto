#!/usr/bin/env python3
"""
Test the weather function directly without MCP
"""

import requests

# Import the weather function from serve.py
from config import OPENWEATHERMAP_API_KEY, WEATHER_API_BASE_URL, WEATHER_UNITS

def get_weather(location: str) -> dict:
    if not OPENWEATHERMAP_API_KEY:
        return {"error": "OPENWEATHERMAP_API_KEY is not set"}

    params = {
        "q": location,
        "appid": OPENWEATHERMAP_API_KEY,
        "units": WEATHER_UNITS
    }

    try:
        response = requests.get(WEATHER_API_BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        return {
            "location": data["name"],
            "weather": weather_description,
            "temperature_celsius": f"{temperature}°C",
            "feels_like_celsius": f"{feels_like}°C",
            "humidity": f"{humidity}%",
            "wind_speed_mps": f"{wind_speed} m/s"
        }

    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            return {"error": f"Could not find weather data for '{location}'. Please check the location name."}
        elif response.status_code == 401:
            return {"error": "Authentication failed. The API key is likely invalid or inactive."}
        else:
            return {"error": f"An HTTP error occurred: {http_err}"}
    except requests.exceptions.RequestException as req_err:
        return {"error": f"A network error occurred: {req_err}"}
    except KeyError:
        return {"error": "Received unexpected data format from the weather API."}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}

# Test the function
if __name__ == "__main__":
    print("Testing Weather Function Directly")
    print("=" * 50)
    
    # Test valid cities
    test_cities = ["London", "New York", "Tokyo", "Paris"]
    
    for city in test_cities:
        print(f"\nTesting: {city}")
        result = get_weather(city)
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
        else:
            print(f"✅ Success!")
            print(f"   Location: {result['location']}")
            print(f"   Weather: {result['weather']}")
            print(f"   Temperature: {result['temperature_celsius']}")
            print(f"   Feels like: {result['feels_like_celsius']}")
            print(f"   Humidity: {result['humidity']}")
            print(f"   Wind Speed: {result['wind_speed_mps']}")
    
    # Test invalid city
    print(f"\nTesting invalid city: 'InvalidCity123'")
    result = get_weather("InvalidCity123")
    if "error" in result:
        print(f"✅ Correctly handled error: {result['error']}")
    else:
        print(f"❌ Unexpected success for invalid city")
    
    print("\n" + "=" * 50)
    print("Testing complete!") 