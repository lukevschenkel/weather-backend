import redis
from django.conf import settings
from .base_weather_setting_manager import BaseWeatherSettingManager
from .types import WeatherSetting

REDIS_KEY = "weather_settings"


class RedisWeatherSettingManager(BaseWeatherSettingManager):
    """Weather settings manager using Redis for storage."""

    def __init__(self) -> None:
        self.r = redis.from_url(
            settings.REDIS_CACHE_URL,
            decode_responses=True,
        )
        

    def get_settings(self) -> WeatherSetting:
        stored = self.r.hgetall(REDIS_KEY)
        print('stored', stored)
        print('settings.DEFAULT_WEATHER_SETTINGS', settings.DEFAULT_WEATHER_SETTINGS)
        merged = {**settings.DEFAULT_WEATHER_SETTINGS, **stored}
        return WeatherSetting(**merged)

    def update_settings(self, data: dict) -> WeatherSetting:
        current = self.r.hgetall(REDIS_KEY)
        updated = {**current, **data}
        self.r.hset(REDIS_KEY, mapping=updated)
        return WeatherSetting(**updated)
