from celery import shared_task
from .portal_providers.factory import PortalProviderFactory
from .weather_providers.factory import WeatherProviderFactory
from .message_providers.factory import MessageProviderFactory
import logging

logger = logging.getLogger(__name__)

@shared_task
def push_message_to_portal() -> None:
    portal_provider = PortalProviderFactory.get_provider()
    weather_provider = WeatherProviderFactory.get_provider()
    message_provider = MessageProviderFactory.get_provider()
    
    # Get weather data
    weather_data = weather_provider.get_from_settings()
    
    smart_message = message_provider.generate_message(weather_data)
    
    # Push to portal
    portal_response = portal_provider.push_message({"message": smart_message})
    logger.info(f"Portal response: {portal_response}")
  