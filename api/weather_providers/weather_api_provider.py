from django.conf import settings
from .base_weather_provider import BaseWeatherProvider
from ..http_client import HttpClient


class WeatherAPIProvider(BaseWeatherProvider):
    BASE_URL = "https://api.weatherapi.com/v1"

    def __init__(self) -> None:
        self.api_key = getattr(settings, "WEATHER_API_KEY")
        self.client = HttpClient(timeout=10, retries=3)

    def get_current(self, zip_code: str) -> dict:
        url = f"{self.BASE_URL}/current.json"
        resp = self.client.get(
            url, params={"key": self.api_key, "q": zip_code, "aqi": "no"}
        )
        resp.raise_for_status()
        return resp.json()

    def get_forecast(self, zip_code: str, days: int) -> dict:
        url = f"{self.BASE_URL}/forecast.json"
        resp = self.client.get(
            url, params={"key": self.api_key, "q": zip_code, "days": days, "aqi": "no"}
        )
        resp.raise_for_status()
        return resp.json()
