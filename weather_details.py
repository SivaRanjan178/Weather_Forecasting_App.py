from datetime import datetime

def get_weather_details(mgr, place):
    """Fetch additional weather details: rain, wind speed, humidity, sunrise, sunset."""
    try:
        # Get weather data
        weather = mgr.weather_at_place(place).weather
        forecaster = mgr.forecast_at_place(place, "3h")

        # Fetch weather conditions
        rain = "Yes" if forecaster.will_have_rain() else "No"
        cloud_coverage = weather.clouds
        wind_speed = weather.wind()["speed"]
        humidity = weather.humidity

        # Convert UNIX sunrise & sunset times to readable format
        sunrise_time = datetime.utcfromtimestamp(weather.sunrise_time()).strftime('%H:%M:%S')
        sunset_time = datetime.utcfromtimestamp(weather.sunset_time()).strftime('%H:%M:%S')

        return {
            "rain": rain,
            "cloud_coverage": cloud_coverage,
            "wind_speed": wind_speed,
            "humidity": humidity,
            "sunrise_time": sunrise_time,
            "sunset_time": sunset_time
        }
    
    except Exception as e:
        return {"error": f"Error fetching weather details: {e}"}
