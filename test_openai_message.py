#!/usr/bin/env python3
"""
Test script to demonstrate OpenAI smart message generation.
Run this script to test the message provider without running the full Celery task.
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append('/home/dev/Documents/weather_middleware/backend')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_middleware.settings')
django.setup()

from api.message_providers.factory import MessageProviderFactory
from api.weather_providers.factory import WeatherProviderFactory

def test_smart_message_generation():
    """Test the smart message generation with OpenAI."""
    
    print("🌤️  Testing Smart Message Generation with OpenAI")
    print("=" * 50)
    
    try:
        # Get weather data
        print("📡 Fetching weather data...")
        weather_provider = WeatherProviderFactory.get_provider()
        weather_data = weather_provider.get_from_settings()
        
        print(f"📍 Location: {weather_data.get('location', {}).get('name', 'Unknown')}")
        print(f"🌡️  Temperature: {weather_data.get('current', {}).get('temp_c', 'N/A')}°C")
        print(f"☁️  Condition: {weather_data.get('current', {}).get('condition', {}).get('text', 'Unknown')}")
        print()
        
        # Generate smart message
        print("🤖 Generating smart message with OpenAI...")
        message_provider = MessageProviderFactory.get_provider()
        smart_message = message_provider.generate_message(weather_data)
        
        print("✨ Generated Message:")
        print(f"   '{smart_message}'")
        print()
        
        print("✅ Test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Make sure to:")
        print("   1. Set OPENAI_API_KEY in your environment")
        print("   2. Set MESSAGE_PROVIDER=openai in your .env file")
        print("   3. Have valid weather API configuration")

if __name__ == "__main__":
    test_smart_message_generation()
