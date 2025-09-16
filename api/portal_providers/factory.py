from typing import Optional
from django.conf import settings
from .dummy_portal_provider import DummyPortalProvider
from .base_portal_provider import BasePortalProvider


class PortalProviderNotConfigured(Exception):
    """Raised when portal provider is missing or misconfigured."""


class UnsupportedPortalProvider(Exception):
    """Raised when portal provider is unsupported."""


class PortalProviderFactory:
    _instance: Optional[BasePortalProvider] = None

    @classmethod
    def get_provider(cls) -> BasePortalProvider:
        if cls._instance is None:
            cls._instance = DummyPortalProvider()
        return cls._instance
