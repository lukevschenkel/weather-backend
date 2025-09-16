from abc import ABC, abstractmethod
from .types import WeatherSetting


class BaseWeatherSettingManager(ABC):
    """Abstract base class for weather settings manager."""

    @abstractmethod
    def get_settings(self) -> WeatherSetting:
        pass

    @abstractmethod
    def update_settings(self, data: dict) -> WeatherSetting:
        pass
