from typing import Optional
from django.conf import settings
from .dummy_weather_provider import DummyWeatherProvider
from .weather_api_provider import WeatherAPIProvider
from .open_weather_map_provider import OpenWeatherMapProvider
from .base_weather_provider import BaseWeatherProvider
from ..weather_setting_managers.factory import WeatherSettingManagerFactory


class WeatherProviderNotConfigured(Exception):
    """Raised when weather provider is missing or misconfigured."""


class UnsupportedWeatherProvider(Exception):
    """Raised when weather provider is unsupported."""


class WeatherProviderFactory:
    _instance: Optional[BaseWeatherProvider] = None

    @classmethod
    def get_provider(cls) -> BaseWeatherProvider:
        if cls._instance is None:
            weather_setting_manager = WeatherSettingManagerFactory.get_manager()
            weather_api = weather_setting_manager.get_settings().weather_api
            if weather_api is None or weather_api == "":
                raise WeatherProviderNotConfigured("Weather API is not configured")

            match weather_api:
                case "dummy":
                    cls._instance = DummyWeatherProvider()
                case "weatherapi":
                    cls._instance = WeatherAPIProvider()
                case "openweathermap":
                    cls._instance = OpenWeatherMapProvider()
                case _:
                    raise UnsupportedWeatherProvider(
                        f"Unsupported weather API: {weather_api}"
                    )

        return cls._instance
