from abc import ABC, abstractmethod
from django.conf import settings

from ..weather_setting_managers.factory import WeatherSettingManagerFactory


class BaseWeatherProvider(ABC):
    """Abstract base class for weather settings manager."""

    @abstractmethod
    def get_current(self, zip_code: str) -> dict:
        pass

    @abstractmethod
    def get_forecast(self, zip_code: str, days: int) -> dict:
        pass

    def get_from_settings(self) -> dict:
        settings_manager = WeatherSettingManagerFactory.get_manager()
        weather_setting = settings_manager.get_settings()
        zip_code = weather_setting.zip_code
        mode = weather_setting.mode
        forecast_days = weather_setting.forecast_days
        if mode == "current":
            return self.get_current(zip_code=zip_code)
        elif mode == "forecast":
            return self.get_forecast(zip_code=zip_code, days=forecast_days)
