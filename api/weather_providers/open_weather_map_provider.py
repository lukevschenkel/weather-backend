from django.conf import settings
from .base_weather_provider import BaseWeatherProvider
from ..http_client import HttpClient


class OpenWeatherMapProvider(BaseWeatherProvider):
    BASE_URL = "https://api.openweathermap.org/data/2.5"

    def __init__(self) -> None:
        self.api_key = getattr(settings, "OPEN_WEATHER_MAP_API_KEY")
        self.client = HttpClient(timeout=10, retries=3)

    def get_current(self, zip_code: str) -> dict:
        url = f"{self.BASE_URL}/weather"
        resp = self.client.get(
            url,
            params={
                "zip": zip_code,
                "appid": self.api_key,
                "units": "metric",
            },
        )
        resp.raise_for_status()
        data = resp.json()
        return self._normalize_current(data)

    def get_forecast(self, zip_code: str, days: int) -> dict:
        # OpenWeatherMap provides 5-day/3-hour forecast via /forecast
        url = f"{self.BASE_URL}/forecast"
        resp = self.client.get(
            url,
            params={
                "zip": zip_code,
                "appid": self.api_key,
                "units": "metric",
            },
        )
        resp.raise_for_status()
        data = resp.json()
        return self._normalize_forecast(data, days)

    def _normalize_current(self, data: dict) -> dict:
        # Normalize to a structure similar to WeatherAPIProvider for reuse
        location_name = data.get("name")
        main = data.get("main", {})
        weather_list = data.get("weather", [])
        wind = data.get("wind", {})
        condition_text = weather_list[0]["description"] if weather_list else None

        return {
            "location": {
                "name": location_name,
            },
            "current": {
                "temp_c": main.get("temp"),
                "temp_f": (main.get("temp") * 9 / 5 + 32) if main.get("temp") is not None else None,
                "condition": {"text": condition_text},
                "humidity": main.get("humidity"),
                "wind_kph": (wind.get("speed") * 3.6) if wind.get("speed") is not None else None,
            },
        }

    def _normalize_forecast(self, data: dict, days: int) -> dict:
        # Basic normalization: group entries by date and sample daily noon entries
        from datetime import datetime
        from collections import defaultdict

        grouped: dict[str, list[dict]] = defaultdict(list)
        for entry in data.get("list", []):
            dt_txt = entry.get("dt_txt")
            if not dt_txt:
                continue
            date_key = dt_txt.split(" ")[0]
            grouped[date_key].append(entry)

        daily = []
        for date_key, entries in grouped.items():
            # pick the entry closest to 12:00:00
            def score(e: dict) -> int:
                t = e.get("dt_txt", "").split(" ")[1]
                return abs(int(t.split(":")[0]) - 12)

            best = sorted(entries, key=score)[0]
            main = best.get("main", {})
            weather_list = best.get("weather", [])
            condition_text = weather_list[0]["description"] if weather_list else None
            daily.append({
                "date": date_key,
                "day": {
                    "avgtemp_c": main.get("temp"),
                    "condition": {"text": condition_text},
                },
            })

        daily = sorted(daily, key=lambda d: d["date"])[:days]

        city = data.get("city", {})
        return {
            "location": {"name": city.get("name")},
            "forecast": {"forecastday": daily},
        }


