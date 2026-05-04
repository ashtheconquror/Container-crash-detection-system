import requests
from datetime import datetime
from typing import List, Dict

class WeatherService:
    """
    Fetches real-world marine weather data from Open-Meteo.
    """
    BASE_URL = "https://marine-api.open-meteo.com/v1/marine"

    def fetch_marine_weather(self, lat: float, lng: float) -> Dict:
        """
        Fetch max wave height and wind speed for a specific coordinate.
        """
        params = {
            "latitude": lat,
            "longitude": lng,
            "hourly": "wave_height,wind_speed_10m",
            "forecast_days": 7
        }
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Simplified: Return max values from forecast
            max_wave = max(data.get("hourly", {}).get("wave_height", [0]))
            max_wind = max(data.get("hourly", {}).get("wind_speed_10m", [0]))
            
            return {
                "max_wave_height": float(max_wave),
                "max_wind_speed": float(max_wind)
            }
        except Exception as e:
            print(f"Error fetching weather: {e}")
            # Fallback to safe defaults if API fails
            return {"max_wave_height": 1.5, "max_wind_speed": 15.0}

weather_service = WeatherService()
