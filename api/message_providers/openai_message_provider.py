import openai
from django.conf import settings
import logging
from .base_message_provider import BaseMessageProvider

logger = logging.getLogger(__name__)

class OpenAIMessageProvider(BaseMessageProvider):
    def __init__(self):
        self.client = openai.OpenAI(
            api_key=getattr(settings, 'OPENAI_API_KEY', '')
        )
        self.model = getattr(settings, 'OPENAI_MODEL', 'gpt-3.5-turbo')
    
    def generate_message(self, weather_data: dict) -> str:
        try:
            # Extract relevant weather information
            current_weather = weather_data.get('current', {})
            location = weather_data.get('location', {})
            
            # Build context for the AI
            weather_context = self._build_weather_context(current_weather, location)
            
            # Create the prompt for OpenAI
            prompt = f"""
            Based on the following weather data, create a friendly, informative weather message that would be useful for someone checking the weather:

            Weather Data:
            {weather_context}

            Please create a concise, helpful message (max 200 characters) that includes:
            - Current temperature
            - Weather condition
            - Location
            - A brief, friendly tone

            Make it sound natural and conversational.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful weather assistant that creates friendly, informative weather messages."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.7
            )
            
            message = response.choices[0].message.content.strip()
            logger.info(f"Generated OpenAI message: {message}")
            return message
            
        except Exception as e:
            logger.error(f"Error generating OpenAI message: {e}")
            # Fallback to a simple message if OpenAI fails
            return self._create_fallback_message(weather_data)
    
    def _build_weather_context(self, current_weather: dict, location: dict) -> str:
        """Build a readable context string from weather data."""
        context_parts = []
        
        if location:
            context_parts.append(f"Location: {location.get('name', 'Unknown')}")
        
        if current_weather:
            temp_c = current_weather.get('temp_c')
            temp_f = current_weather.get('temp_f')
            condition = current_weather.get('condition', {}).get('text', 'Unknown')
            humidity = current_weather.get('humidity')
            wind_kph = current_weather.get('wind_kph')
            
            if temp_c is not None:
                context_parts.append(f"Temperature: {temp_c}°C ({temp_f}°F)")
            if condition:
                context_parts.append(f"Condition: {condition}")
            if humidity is not None:
                context_parts.append(f"Humidity: {humidity}%")
            if wind_kph is not None:
                context_parts.append(f"Wind: {wind_kph} km/h")
        
        return "\n".join(context_parts) if context_parts else "No weather data available"
    
    def _create_fallback_message(self, weather_data: dict) -> str:
        """Create a simple fallback message when OpenAI fails."""
        current_weather = weather_data.get('current', {})
        location = weather_data.get('location', {})
        
        location_name = location.get('name', 'Unknown location')
        temp_c = current_weather.get('temp_c')
        condition = current_weather.get('condition', {}).get('text', 'Unknown')
        
        if temp_c is not None:
            return f"Weather in {location_name}: {temp_c}°C, {condition}"
        else:
            return f"Weather update for {location_name}: {condition}"