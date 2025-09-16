from .base_weather_provider import BaseWeatherProvider


class DummyWeatherProvider(BaseWeatherProvider):

    def get_current(self, zip_code: str) -> dict:
        return {"temperature": 5.7, "humidity": 34}

    def get_forecast(self, zip_code: str, days: int) -> dict:
        return {"temperature": days, "humidity": 50}
