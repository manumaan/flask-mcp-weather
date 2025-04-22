from mcp.server.fastmcp import FastMCP
import requests
import time
from functools import lru_cache

# create server 
mcp = FastMCP("Weather Server")

@mcp.tool()
@lru_cache(maxsize=100)
def get_weather(city: str) -> str:
    start_time = time.time()
    endpoint = "https://wttr.in"
    response = requests.get(f"{endpoint}/{city}?format=j1", timeout=5)
    elapsed_time = time.time() - start_time
    print(f"get_weather execution time: {elapsed_time:.2f} seconds")

    # Parse the JSON response
    weather_data = response.json()

    # Extract current weather details
    current_condition = weather_data['current_condition'][0]
    condition = current_condition['weatherDesc'][0]['value']
    temperature = current_condition['temp_C']
    feels_like = current_condition['FeelsLikeC']
    wind_speed = current_condition['windspeedKmph']
    precipitation = current_condition['precipMM']

    # Extract forecast details
    forecast = weather_data['weather'][0]['hourly']
    morning = forecast[2]  # Assuming morning is around 6 AM
    noon = forecast[5]     # Assuming noon is around 12 PM
    evening = forecast[8]  # Assuming evening is around 6 PM
    night = forecast[11]   # Assuming night is around 9 PM

    # Format the weather report
    report = f"""
Here's the weather report for {city}:
Current Weather

    Condition: {condition}
    Temperature: {temperature}°C (Feels like {feels_like}°C)
    Wind Speed: {wind_speed} km/h
    Precipitation: {precipitation} mm

Forecast

    Morning: {morning['weatherDesc'][0]['value']} near +{morning['tempC']}°C (Feels like +{morning['FeelsLikeC']}°C)
    Noon: {noon['weatherDesc'][0]['value']} near +{noon['tempC']}°C (Feels like +{noon['FeelsLikeC']}°C)
    Evening: {evening['weatherDesc'][0]['value']} near +{evening['tempC']}°C (Feels like +{evening['FeelsLikeC']}°C)
    Night: {night['weatherDesc'][0]['value']} near +{night['tempC']}°C (Feels like +{night['FeelsLikeC']}°C)

Summary

    Expect {morning['weatherDesc'][0]['value']} in the morning and {noon['weatherDesc'][0]['value']} at noon, with {evening['weatherDesc'][0]['value']} in the evening. The night may see some {night['weatherDesc'][0]['value']} as well.
    """

    return report

@mcp.tool()
def add_numbers(a : int, b : int) -> int:
    return a + b

# run the server
if __name__ == "__main__":
    mcp.run()