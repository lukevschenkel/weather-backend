from typing import Optional
from django.conf import settings
from .base_message_provider import BaseMessageProvider
from .dummy_message_provider import DummyMessageProvider
from .openai_message_provider import OpenAIMessageProvider


class UnsupportedMessageProvider(Exception):
    """Raised when message provider is unsupported."""


class MessageProviderFactory:
    _instance: Optional[BaseMessageProvider] = None

    @classmethod
    def get_provider(cls) -> BaseMessageProvider:
        if cls._instance is None:
            message_provider = getattr(settings, 'MESSAGE_PROVIDER', 'dummy')
            
            match message_provider:
                case "dummy":
                    cls._instance = DummyMessageProvider()
                case "openai":
                    cls._instance = OpenAIMessageProvider()
                case _:
                    raise UnsupportedMessageProvider(
                        f"Unsupported message provider: {message_provider}"
                    )

        return cls._instance
