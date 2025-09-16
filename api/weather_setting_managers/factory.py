from django.conf import settings
from .base_weather_setting_manager import BaseWeatherSettingManager
from .redis_weather_setting_manager import RedisWeatherSettingManager


class WeatherSettingManagerFactory:
    """
    Factory class to return a singleton weather setting manager.
    """

    _instance: BaseWeatherSettingManager | None = None

    @classmethod
    def get_manager(cls) -> BaseWeatherSettingManager:
        if cls._instance is not None:
            return cls._instance

        backend_type = getattr(settings, "WEATHER_SETTING_BACKEND", None)
        if backend_type is None:
            raise ValueError("Weather setting backend not configured in settings")

        if backend_type == "redis":
            cls._instance = RedisWeatherSettingManager()
        else:
            raise ValueError(
                f"Unsupported weather setting backend type: {backend_type}"
            )

        return cls._instance
