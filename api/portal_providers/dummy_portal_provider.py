from .base_portal_provider import BasePortalProvider, MessagePayload
from datetime import datetime
import logging
from ..models import Message
logger = logging.getLogger(__name__)

class DummyPortalProvider(BasePortalProvider):

    def push_message(self, data: MessagePayload) -> Message:
        logger.info(f"DummyPortalProvider: Pushing message: {data}")
        message = Message.objects.create(
            text=data["message"],
            portal_response=data,
            created_at=datetime.now(),
            delivered=True
        )
        return message

