from pydantic import BaseModel, Field
from typing import Literal


class WeatherSetting(BaseModel):
    zip_code: str = Field(..., pattern=r"^\d{5}$")
    mode: Literal["current", "forecast"] = "current"
    forecast_days: int = Field(default=5)
    weather_api: Literal["weatherapi", "dummy", "openweathermap"] = "weatherapi"
