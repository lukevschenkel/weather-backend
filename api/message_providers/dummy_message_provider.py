from .base_message_provider import BaseMessageProvider

class DummyMessageProvider(BaseMessageProvider):
    def generate_message(self, weather_data: dict) -> str:
        return "dummy message"